"""
Servicio de gestión de proyectos
Maneja operaciones relacionadas con proyectos
"""

from sqlalchemy.orm import Session
from app.models.models import Project, User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead, ProjectReadWithDetails
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.core.exceptions import (
    ProjectNotFoundError,
    UserNotFoundError,
    PermissionDeniedError,
    InvalidInputError
)
from typing import List, Optional


class ProjectService:
    """
    Servicio de gestión de proyectos
    Maneja operaciones CRUD y lógica de negocio de proyectos
    """

    def __init__(self, db: Session):
        """
        Inicializar servicio de proyecto
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.project_repo = ProjectRepository(db)
        self.user_repo = UserRepository(db)

    def create_project(self, project_data: ProjectCreate, owner_id: int) -> ProjectRead:
        """
        Crear nuevo proyecto
        
        Args:
            project_data: Datos del proyecto
            owner_id: ID del propietario
            
        Returns:
            Proyecto creado
            
        Raises:
            UserNotFoundError: Si el propietario no existe
        """
        # Verificar que el usuario existe
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise UserNotFoundError(f"Usuario propietario {owner_id} no encontrado")

        project = Project(
            nombre=project_data.nombre,
            descripcion=project_data.descripcion,
            owner_id=owner_id,
        )

        created_project = self.project_repo.create_from_obj(project)
        return ProjectRead.from_orm(created_project)

    def get_project(self, project_id: int) -> ProjectReadWithDetails:
        """
        Obtener detalles del proyecto
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Detalles del proyecto con miembros y tareas
            
        Raises:
            ProjectNotFoundError: Si el proyecto no existe
        """
        project = self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Proyecto {project_id} no encontrado")

        return ProjectReadWithDetails.from_orm(project)

    def get_user_projects(self, user_id: int, skip: int = 0, limit: int = 10) -> List[ProjectRead]:
        """
        Obtener proyectos del usuario
        
        Args:
            user_id: ID del usuario
            skip: Registros a saltar
            limit: Límite de registros
            
        Returns:
            Lista de proyectos
        """
        # Verificar que el usuario existe
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario {user_id} no encontrado")

        projects = self.project_repo.get_user_projects(user_id, skip, limit)
        return [ProjectRead.from_orm(project) for project in projects]

    def update_project(self, project_id: int, project_update: ProjectUpdate, 
                      current_user_id: int) -> ProjectRead:
        """
        Actualizar proyecto
        
        Args:
            project_id: ID del proyecto
            project_update: Datos a actualizar
            current_user_id: ID del usuario actual
            
        Returns:
            Proyecto actualizado
            
        Raises:
            ProjectNotFoundError: Si el proyecto no existe
            PermissionDeniedError: Si no es propietario
        """
        # Verificar que es propietario
        if not self.project_repo.is_owner(project_id, current_user_id):
            raise PermissionDeniedError("Solo el propietario puede actualizar el proyecto")

        update_data = project_update.dict(exclude_unset=True)
        updated_project = self.project_repo.update(project_id, **update_data)

        return ProjectRead.from_orm(updated_project)

    def delete_project(self, project_id: int, current_user_id: int) -> bool:
        """
        Eliminar proyecto
        
        Args:
            project_id: ID del proyecto
            current_user_id: ID del usuario actual
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            ProjectNotFoundError: Si el proyecto no existe
            PermissionDeniedError: Si no es propietario
        """
        # Verificar que es propietario
        if not self.project_repo.is_owner(project_id, current_user_id):
            raise PermissionDeniedError("Solo el propietario puede eliminar el proyecto")

        return self.project_repo.delete(project_id)

    def add_member(self, project_id: int, user_id: int, current_user_id: int) -> bool:
        """
        Agregar miembro al proyecto
        
        Args:
            project_id: ID del proyecto
            user_id: ID del usuario a agregar
            current_user_id: ID del usuario actual
            
        Returns:
            True si se agregó exitosamente
            
        Raises:
            ProjectNotFoundError: Si el proyecto no existe
            UserNotFoundError: Si el usuario no existe
            PermissionDeniedError: Si no es propietario
        """
        # Verificar permisos
        if not self.project_repo.is_owner(project_id, current_user_id):
            raise PermissionDeniedError("Solo el propietario puede agregar miembros")

        # Verificar que ambos existen
        project = self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Proyecto {project_id} no encontrado")

        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario {user_id} no encontrado")

        return self.project_repo.add_member(project_id, user_id)

    def remove_member(self, project_id: int, user_id: int, current_user_id: int) -> bool:
        """
        Remover miembro del proyecto
        
        Args:
            project_id: ID del proyecto
            user_id: ID del usuario a remover
            current_user_id: ID del usuario actual
            
        Returns:
            True si se removió exitosamente
            
        Raises:
            PermissionDeniedError: Si no es propietario
        """
        # Verificar permisos
        if not self.project_repo.is_owner(project_id, current_user_id):
            raise PermissionDeniedError("Solo el propietario puede remover miembros")

        return self.project_repo.remove_member(project_id, user_id)

    def is_member(self, project_id: int, user_id: int) -> bool:
        """
        Verificar si es miembro del proyecto
        
        Args:
            project_id: ID del proyecto
            user_id: ID del usuario
            
        Returns:
            True si es miembro o propietario
        """
        return self.project_repo.is_member(project_id, user_id)

    def is_owner(self, project_id: int, user_id: int) -> bool:
        """
        Verificar si es propietario del proyecto
        
        Args:
            project_id: ID del proyecto
            user_id: ID del usuario
            
        Returns:
            True si es propietario
        """
        return self.project_repo.is_owner(project_id, user_id)
