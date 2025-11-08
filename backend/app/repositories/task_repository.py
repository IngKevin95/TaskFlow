"""
Repositorio para operaciones de Tarea
Implementa métodos específicos de tarea además de CRUD base
"""

from sqlalchemy.orm import Session
from app.models.models import Task
from app.repositories.base import BaseRepository
from app.core.enums import TaskStatus, TaskPriority
from typing import Optional, List


class TaskRepository(BaseRepository[Task]):
    """
    Repositorio especializado para Tarea
    Hereda operaciones CRUD de BaseRepository
    """

    def __init__(self, db: Session):
        """Inicializar repositorio de tarea"""
        super().__init__(db, Task)

    def get_project_tasks(self, project_id: int, skip: int = 0, limit: int = 50) -> List[Task]:
        """
        Obtener todas las tareas de un proyecto
        
        Args:
            project_id: ID del proyecto
            skip: Registros a saltar
            limit: Límite de registros
            
        Returns:
            Lista de tareas del proyecto
        """
        return self.db.query(Task).filter(
            Task.project_id == project_id
        ).offset(skip).limit(limit).all()

    def get_user_assigned_tasks(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Task]:
        """
        Obtener tareas asignadas a un usuario
        
        Args:
            user_id: ID del usuario
            skip: Registros a saltar
            limit: Límite de registros
            
        Returns:
            Lista de tareas asignadas
        """
        return self.db.query(Task).filter(
            Task.assigned_to_id == user_id
        ).offset(skip).limit(limit).all()

    def get_tasks_by_status(self, project_id: int, status: TaskStatus, 
                           skip: int = 0, limit: int = 50) -> List[Task]:
        """
        Obtener tareas de un proyecto filtradas por estado
        
        Args:
            project_id: ID del proyecto
            status: Estado de la tarea
            skip: Registros a saltar
            limit: Límite de registros
            
        Returns:
            Lista de tareas filtradas
        """
        return self.db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == status
        ).offset(skip).limit(limit).all()

    def get_tasks_by_priority(self, project_id: int, priority: TaskPriority,
                             skip: int = 0, limit: int = 50) -> List[Task]:
        """
        Obtener tareas de un proyecto filtradas por prioridad
        
        Args:
            project_id: ID del proyecto
            priority: Prioridad de la tarea
            skip: Registros a saltar
            limit: Límite de registros
            
        Returns:
            Lista de tareas filtradas
        """
        return self.db.query(Task).filter(
            Task.project_id == project_id,
            Task.priority == priority
        ).offset(skip).limit(limit).all()

    def update_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        """
        Actualizar estado de una tarea
        
        Args:
            task_id: ID de la tarea
            status: Nuevo estado
            
        Returns:
            Tarea actualizada o None
        """
        task = self.get(task_id)
        if task:
            task.status = status
            self.db.commit()
            self.db.refresh(task)
        return task

    def count_by_status(self, project_id: int, status: TaskStatus) -> int:
        """
        Contar tareas por estado en un proyecto
        
        Args:
            project_id: ID del proyecto
            status: Estado de la tarea
            
        Returns:
            Número de tareas
        """
        return self.db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == status
        ).count()
