"""
Router for authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.user import UserCreate, UserRead, LoginRequest
from app.services.auth_service import AuthService
from app.database.session import get_db
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.api.routers.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", tags=["auth"], summary="Iniciar sesión y obtener token JWT")
async def login(
    username: str = Form(..., description="Nombre de usuario", min_length=3),
    password: str = Form(..., description="Contraseña del usuario", min_length=6, media_type="password"),
    db: Session = Depends(get_db)
):
    """
    **Endpoint de autenticación** - Inicia sesión y obtiene un token JWT para usar en el botón "Authorize".
    
    ## 📋 Pasos para autenticarte en Swagger:
    
    1. **Ejecuta este endpoint** con tus credenciales (username y password)
    2. **Copia el valor de `access_token`** de la respuesta (solo el token, sin comillas)
    3. **Haz clic en el botón "Authorize" 🔓** en la parte superior derecha de Swagger UI
    4. **Pega el token** en el campo "Value" (sin agregar "Bearer", solo el token)
    5. **Haz clic en "Authorize"** y luego en "Close"
    6. Ahora todos los endpoints protegidos usarán automáticamente tu token
    
    ## 📤 Respuesta:
    - `access_token`: Token JWT para autenticación (copia este valor)
    - `token_type`: Tipo de token (bearer)
    - `user`: Información del usuario autenticado
    
    ## ⚠️ Errores posibles:
    - **401**: Credenciales inválidas o usuario inactivo
    
    Args:
        username: Nombre de usuario (mínimo 3 caracteres)
        password: Contraseña (mínimo 6 caracteres)
        
    Returns:
        Token JWT, tipo de token e información del usuario
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


@router.get("/validate-token", tags=["auth"], summary="✅ Validar token JWT")
async def validate_token(
    current_user = Depends(get_current_user),
):
    """
    **🔍 Valida si el token JWT es válido y está activo**
    
    ## 🎯 Propósito
    
    Este endpoint te permite **probar inmediatamente** si el token que ingresaste en el botón 
    "Authorize" es válido, sin tener que realizar otras operaciones.
    
    ## 🔐 Cómo usarlo:
    
    1. Haz clic en el botón **"Authorize" 🔓** (arriba a la derecha)
    2. Pega tu token JWT
    3. Haz clic en "Authorize" y "Close"
    4. **Ejecuta este endpoint** (Try it out → Execute)
    
    ## ✅ Respuestas posibles:
    
    - **200 OK**: ✅ Token válido - Devuelve información del usuario y confirmación
    - **401 Unauthorized**: ❌ Token inválido, expirado o faltante
      - "Token inválido: no contiene ID de usuario"
      - "Usuario no encontrado"
      - "Token inválido o expirado"
    
    ## 💡 Consejo:
    
    Usa este endpoint después de hacer login para confirmar que tu token fue guardado 
    correctamente en el botón "Authorize" de Swagger.
    
    Returns:
        Mensaje de validación exitosa con información del usuario
    """
    return {
        "valid": True,
        "message": "✅ Token JWT válido y activo",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active
        }
    }


@router.get("/me", response_model=UserRead, tags=["auth"], summary="Obtener usuario autenticado actual")
async def get_me(
    current_user = Depends(get_current_user),
):
    """
    **Obtiene la información del usuario autenticado** mediante el token JWT.
    
    ## 🔐 Requiere Autenticación
    
    Este endpoint valida el token JWT proporcionado en el header `Authorization: Bearer <token>`.
    
    - Si no has iniciado sesión, usa el endpoint `/api/auth/login` primero
    - Si ya tienes un token, haz clic en "Authorize" 🔓 y pégalo
    - Si el token es inválido o ha expirado, recibirás un error 401
    
    ## 📤 Respuesta:
    Devuelve los datos del usuario actual:
    - `id`: ID del usuario
    - `username`: Nombre de usuario
    - `email`: Correo electrónico
    - `first_name`: Nombre
    - `last_name`: Apellido
    - `role`: Rol del usuario (ADMIN, MANAGER, USER)
    - `is_active`: Estado del usuario
    - `created_at`: Fecha de creación
    - `updated_at`: Fecha de última actualización
    
    ## ⚠️ Errores posibles:
    - **401**: Token faltante, inválido o expirado
    
    Returns:
        Información completa del usuario autenticado
    """
    return current_user



