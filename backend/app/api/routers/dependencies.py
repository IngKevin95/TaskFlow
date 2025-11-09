"""
Dependencies for API endpoints
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.auth_service import AuthService

# Security scheme for Swagger UI
security = HTTPBearer(
    scheme_name="BearerAuth",
    description="Ingresa tu token JWT (sin el prefijo 'Bearer')",
    auto_error=True
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user from Bearer token
    
    Args:
        credentials: HTTP Bearer credentials from Authorization header
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If not authenticated or token is invalid
    """
    token = credentials.credentials
    
    try:
        from app.core.security import decode_token
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
