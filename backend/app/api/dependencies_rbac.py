"""
RBAC dependencies for authentication and authorization
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.database.session import get_db
from app.core.security import decode_token
from app.services.auth_service import AuthService

# Security scheme for Swagger UI (compatible con el botón Authorize)
security = HTTPBearer(
    scheme_name="BearerAuth",
    description="Token JWT - usa el botón 'Authorize' para autenticarte",
    auto_error=True
)


async def get_current_user_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current user from Bearer token (compatible con Swagger Authorize button)
    
    Args:
        credentials: HTTP Bearer credentials from Authorization header
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: no contiene ID de usuario",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        service = AuthService(db)
        user = service.get_current_user(int(user_id))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}",
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
