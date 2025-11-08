"""
Schemas de validación para Tarea usando Pydantic
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.core.enums import TaskPriority, TaskStatus


class UserReadMinimal(BaseModel):
    """Schema mínimal de usuario"""
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """Schema base de tarea"""
    title: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema para crear tarea"""
    project_id: int
    assigned_to_id: Optional[int] = None


class TaskUpdate(BaseModel):
    """Schema para actualizar tarea"""
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    assigned_to_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    """Schema para leer tarea"""
    id: int
    project_id: int
    creator_id: Optional[int] = None
    assigned_to_id: Optional[int] = None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskReadWithAssignee(TaskRead):
    """Schema de tarea con información del asignado"""
    assigned_to: Optional[UserReadMinimal] = None
    creator: Optional[UserReadMinimal] = None

    class Config:
        from_attributes = True
