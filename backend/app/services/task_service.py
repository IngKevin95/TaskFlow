"""
Servicio de gestión de tareas
Maneja operaciones relacionadas con tareas
"""

from sqlalchemy.orm import Session
from app.models.models import Task, Project, User
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskReadWithAssignee
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.core.enums import TaskStatus
from app.core.exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    UserNotFoundError,
    PermissionDeniedError,
    InvalidInputError
)
from typing import List, Optional


class TaskService:
    """
    Servicio de gestión de tareas
    Maneja operaciones CRUD y lógica de negocio de tareas
    """

    def __init__(self, db: Session):
        """
        Inicializar servicio de tarea
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.user_repo = UserRepository(db)

    def create_task(self, project_id: int, task_data: TaskCreate, 
                   creator_id: int, creator_role: str = None) -> TaskRead:
        """
        Crear nueva tarea en un proyecto
        
        Args:
            project_id: ID del proyecto
            task_data: Datos de la tarea
            creator_id: ID del usuario creador
            creator_role: Rol del usuario creador (admin, read_write, read_only)
            
        Returns:
            Tarea creada
            
        Raises:
            ProjectNotFoundError: Si el proyecto no existe
            PermissionDeniedError: Si no es miembro del proyecto ni admin
        """
        # Verificar que el proyecto existe y es miembro (o es admin)
        project = self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Proyecto {project_id} no encontrado")

        is_admin = creator_role == "admin"
        is_member = self.project_repo.is_member(project_id, creator_id)
        
        if not (is_admin or is_member):
            raise PermissionDeniedError("No eres miembro de este proyecto")

        # Verificar que el usuario asignado existe (si se especifica)
        if task_data.assigned_to_id:
            assigned_user = self.user_repo.get(task_data.assigned_to_id)
            if not assigned_user:
                raise UserNotFoundError(f"Usuario {task_data.assigned_to_id} no encontrado")

        task = Task(
            title=task_data.title,
            description=task_data.description,
            project_id=project_id,
            creator_id=creator_id,
            assigned_to_id=task_data.assigned_to_id,
            priority=task_data.priority,
            due_date=task_data.due_date,
        )

        created_task = self.task_repo.create_from_obj(task)
        return TaskRead.from_orm(created_task)

    def get_task(self, task_id: int) -> TaskReadWithAssignee:
        """
        Obtener detalles de una tarea
        
        Args:
            task_id: ID de la tarea
            
        Returns:
            Detalles de la tarea
            
        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        task = self.task_repo.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Tarea {task_id} no encontrada")

        return TaskReadWithAssignee.from_orm(task)

    def get_project_tasks(self, project_id: int, skip: int = 0, 
                         limit: int = 50, status_filter: Optional[str] = None,
                         priority_filter: Optional[str] = None,
                         assigned_to_id: Optional[int] = None,
                         creator_id: Optional[int] = None) -> List[TaskRead]:
        """
        Obtener todas las tareas de un proyecto con filtros opcionales
        
        Args:
            project_id: ID del proyecto
            skip: Registros a saltar
            limit: Límite de registros
            status_filter: Filtrar por estado (opcional)
            priority_filter: Filtrar por prioridad (opcional)
            assigned_to_id: Filtrar por usuario asignado (opcional)
            creator_id: Filtrar por creador (opcional)
            
        Returns:
            Lista de tareas
            
        Raises:
            ProjectNotFoundError: Si el proyecto no existe
        """
        project = self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Proyecto {project_id} no encontrado")

        tasks = self.task_repo.get_project_tasks(project_id, skip, limit)
        
        # Filtrar por estado si se especifica
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]
        
        # Filtrar por prioridad si se especifica
        if priority_filter:
            tasks = [t for t in tasks if t.priority == priority_filter]
        
        # Filtrar por usuario asignado si se especifica
        if assigned_to_id is not None:
            tasks = [t for t in tasks if t.assigned_to_id == assigned_to_id]
        
        # Filtrar por creador si se especifica
        if creator_id is not None:
            tasks = [t for t in tasks if t.creator_id == creator_id]
        
        return [TaskRead.from_orm(task) for task in tasks]

    def get_user_assigned_tasks(self, user_id: int, skip: int = 0, 
                               limit: int = 50, status_filter: Optional[str] = None,
                               priority_filter: Optional[str] = None,
                               project_id: Optional[int] = None) -> List[TaskRead]:
        """
        Obtener tareas asignadas al usuario con filtros opcionales
        
        Args:
            user_id: ID del usuario
            skip: Registros a saltar
            limit: Límite de registros
            status_filter: Filtrar por estado (opcional)
            priority_filter: Filtrar por prioridad (opcional)
            project_id: Filtrar por proyecto (opcional)
            
        Returns:
            Lista de tareas asignadas
            
        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario {user_id} no encontrado")

        tasks = self.task_repo.get_user_assigned_tasks(user_id, skip, limit)
        
        # Filtrar por estado si se especifica
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]
        
        # Filtrar por prioridad si se especifica
        if priority_filter:
            tasks = [t for t in tasks if t.priority == priority_filter]
        
        # Filtrar por proyecto si se especifica
        if project_id is not None:
            tasks = [t for t in tasks if t.project_id == project_id]
        
        return [TaskRead.from_orm(task) for task in tasks]

    def update_task(self, task_id: int, update_data: dict) -> TaskRead:
        """
        Actualizar una tarea
        
        Args:
            task_id: ID de la tarea
            update_data: Datos a actualizar (diccionario)
            
        Returns:
            Tarea actualizada
            
        Raises:
            TaskNotFoundError: Si la tarea no existe
            UserNotFoundError: Si el usuario asignado no existe
        """
        task = self.task_repo.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Tarea {task_id} no encontrada")

        # Verificar que el usuario asignado existe (si se especifica)
        if 'assigned_to_id' in update_data and update_data['assigned_to_id']:
            assigned_user = self.user_repo.get(update_data['assigned_to_id'])
            if not assigned_user:
                raise UserNotFoundError(f"Usuario {update_data['assigned_to_id']} no encontrado")

        updated_task = self.task_repo.update(task_id, **update_data)

        return TaskRead.from_orm(updated_task)

    def delete_task(self, task_id: int) -> bool:
        """
        Eliminar una tarea
        
        Args:
            task_id: ID de la tarea
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        task = self.task_repo.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Tarea {task_id} no encontrada")

        return self.task_repo.delete(task_id)

    def update_status(self, task_id: int, new_status: str) -> TaskRead:
        """
        Actualizar estado de una tarea
        
        Args:
            task_id: ID de la tarea
            new_status: Nuevo estado (string)
            
        Returns:
            Tarea actualizada
            
        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        task = self.task_repo.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Tarea {task_id} no encontrada")

        updated_task = self.task_repo.update_status(task_id, new_status)
        return TaskRead.from_orm(updated_task)
