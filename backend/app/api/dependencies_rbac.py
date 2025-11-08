"""
RBAC dependencies for authentication and authorization
"""
from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.orm import Session
from jose import JWTError

from app.database.session import get_db
from app.core.security import decode_token
from app.services.auth_service import AuthService


async def get_current_user_from_header(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Get current user from Authorization header
    
    Args:
        authorization: Authorization header value
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If token is missing or invalid
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
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_admin(current_user = Depends(get_current_user_from_header)):
    """
    Dependency to require ADMIN role
    
    Args:
        current_user: Current user
        
    Returns:
        Current user if ADMIN
        
    Raises:
        HTTPException: If user is not ADMIN
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
