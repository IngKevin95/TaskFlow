"""
Router for authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Form, Header
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead, RegisterRequest
from app.services.auth_service import AuthService
from app.database.session import get_db
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.api.routers.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If user already exists or input is invalid
    """
    try:
        service = AuthService(db)
        new_user = service.register(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        return new_user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Login user and return access token
    
    Args:
        username: Username
        password: Password
        db: Database session
        
    Returns:
        Access token and token type
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        service = AuthService(db)
        token_data = service.login(username=username, password=password)
        return token_data
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserRead)
async def get_me(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user
    
    Args:
        authorization: Authorization header
        db: Database session
        
    Returns:
        Current user
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>"
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    
    try:
        from app.core.security import decode_token
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        service = AuthService(db)
        user = service.get_current_user(int(user_id))
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
