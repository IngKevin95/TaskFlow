"""
Schemas de validación para Usuario usando Pydantic
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, SecretStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    """Schema base de usuario"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str = Field(..., min_length=6, max_length=50)


class RegisterRequest(UserBase):
    """Schema para registro de usuario"""
    password: str = Field(..., min_length=6, max_length=50)


class LoginRequest(BaseModel):
    """Schema para login - password aparece oculto en Swagger"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: SecretStr = Field(..., min_length=6, max_length=50, description="Password")


class UserCreateAdmin(UserBase):
    """Schema para crear usuario (admin)"""
    password: str = Field(..., min_length=8, max_length=50)
    role: str = Field(default="read_write", pattern="^(admin|read_write|read_only)$")


class UserUpdate(BaseModel):
    """Schema para actualizar usuario - solo permite campos específicos"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, pattern="^(admin|read_write|read_only)$")

    model_config = {
        "extra": "forbid"  # Rechazar campos no definidos
    }

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is not None:
            valid_roles = ["admin", "read_write", "read_only"]
            if v not in valid_roles:
                raise ValueError(f"Rol inválido. Roles válidos: {', '.join(valid_roles)}")
        return v

    def __init__(self, **data):
        super().__init__(**data)
        # Validar que al menos un campo esté presente
        if all(v is None for v in [self.email, self.first_name, self.last_name, self.role]):
            raise ValueError("Al menos uno de estos campos es requerido: email, first_name, last_name, role")


class ChangePasswordRequest(BaseModel):
    """Schema para cambiar contraseña"""
    new_password: str = Field(..., min_length=8, max_length=50)


class UserRead(UserBase):
    """Schema para leer usuario"""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserReadWithProjects(UserRead):
    """Schema de usuario con sus proyectos"""
    projects_owned: List['ProjectRead'] = []
    
    class Config:
        from_attributes = True


# Para evitar circular imports, se define al final
from .project import ProjectRead  # noqa: E402, F401
