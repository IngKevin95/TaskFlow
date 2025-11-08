"""
Schemas de validación para Proyecto usando Pydantic
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


class UserReadSimple(BaseModel):
    """Schema simple de usuario para lectura"""
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TaskRead(BaseModel):
    """Schema para leer tarea (referencia)"""
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    """Schema base de proyecto"""
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(populate_by_name=True)


class ProjectCreate(ProjectBase):
    """Schema para crear proyecto"""
    pass


class ProjectUpdate(BaseModel):
    """Schema para actualizar proyecto"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(populate_by_name=True)


class ProjectRead(ProjectBase):
    """Schema para leer proyecto"""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectReadWithDetails(ProjectRead):
    """Schema de proyecto con miembros y tareas"""
    members: List[UserReadSimple] = []
    tasks: List[TaskRead] = []
    
    model_config = ConfigDict(from_attributes=True)
