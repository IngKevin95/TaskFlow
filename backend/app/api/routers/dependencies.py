"""
Dependencies for API endpoints
"""
from fastapi import HTTPException, status, Header, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.auth_service import AuthService


async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user from Authorization header
    
    Args:
        authorization: Authorization header value
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If not authenticated
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
