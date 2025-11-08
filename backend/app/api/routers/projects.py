"""
API Router for Projects
Endpoints: POST, GET, PATCH, DELETE para gestión de proyectos
Autenticación requerida para todas las operaciones
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from sqlalchemy.orm import Session

from app.schemas.project import (
    ProjectCreate,
    ProjectRead,
    ProjectReadWithDetails,
    ProjectUpdate,
)
from app.schemas.common import MessageResponse, ErrorResponse
from app.services.project_service import ProjectService
from app.services.auth_service import AuthService
from app.models.models import User
from app.database.session import get_db
from app.api.routers.dependencies import get_current_user
from app.core.exceptions import (
    ProjectNotFoundError,
    PermissionDeniedError,
    InvalidInputError,
)

router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
    responses={401: {"description": "Unauthorized"}, 404: {"description": "Not Found"}},
)


# CREATE - POST /api/projects
@router.post(
    "",
    response_model=ProjectReadWithDetails,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo proyecto",
    description="Crea un nuevo proyecto. El usuario autenticado es el propietario.",
)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo proyecto.
    
    - **name**: Nombre del proyecto (requerido)
    - **description**: Descripción del proyecto (opcional)
    
    El usuario autenticado es automáticamente el propietario del proyecto.
    
    Solo ADMIN y READ_WRITE pueden crear proyectos.
    """
    # Validar que el usuario no sea READ_ONLY
    if current_user.role == "read_only":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="READ_ONLY users cannot create projects"
        )
    
    try:
        service = ProjectService(db)
        project = service.create_project(
            project_data=project_data,
            owner_id=current_user.id,
        )
        return project
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# READ - GET /api/projects (lista de proyectos del usuario)
@router.get(
    "",
    response_model=List[ProjectRead],
    status_code=status.HTTP_200_OK,
    summary="Listar proyectos del usuario",
    description="Obtiene todos los proyectos donde el usuario es propietario o miembro.",
)
async def list_projects(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene la lista de proyectos del usuario autenticado.
    
    - **skip**: Offset para paginación (default: 0)
    - **limit**: Número máximo de resultados (default: 10, máximo: 100)
    
    Retorna proyectos donde el usuario es propietario o miembro.
    """
    try:
        service = ProjectService(db)
        projects = service.get_user_projects(
            user_id=current_user.id, skip=skip, limit=limit
        )
        return projects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# READ - GET /api/projects/{project_id}
@router.get(
    "/{project_id}",
    response_model=ProjectReadWithDetails,
    status_code=status.HTTP_200_OK,
    summary="Obtener detalles de un proyecto",
    description="Obtiene los detalles completos de un proyecto con miembros y tareas.",
)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene los detalles completos de un proyecto.
    
    Incluye:
    - Información del proyecto
    - Propietario
    - Lista de miembros
    - Lista de tareas
    
    Solo propietarios y miembros pueden ver el proyecto. Los administradores pueden ver cualquier proyecto.
    """
    try:
        service = ProjectService(db)
        
        # Administradores pueden ver cualquier proyecto
        if current_user.role != "admin":
            # Verificar que el usuario es propietario o miembro
            if not service.is_member(project_id=project_id, user_id=current_user.id):
                raise PermissionDeniedError(
                    "No tienes permisos para acceder a este proyecto"
                )
        
        project = service.get_project(project_id=project_id)
        if not project:
            raise ProjectNotFoundError(f"Proyecto con ID {project_id} no encontrado")
        
        return project
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# UPDATE - PATCH /api/projects/{project_id}
@router.patch(
    "/{project_id}",
    response_model=ProjectReadWithDetails,
    status_code=status.HTTP_200_OK,
    summary="Actualizar proyecto",
    description="Actualiza los detalles de un proyecto. Solo el propietario puede actualizar.",
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza un proyecto existente.
    
    Solo el propietario puede actualizar:
    - **name**: Nuevo nombre (opcional)
    - **description**: Nueva descripción (opcional)
    
    Campos no incluidos en la solicitud no serán modificados.
    """
    # Validar que el usuario no sea READ_ONLY
    if current_user.role == "read_only":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="READ_ONLY users cannot update projects"
        )
    
    try:
        service = ProjectService(db)
        
        # Verificar que el usuario es propietario
        if not service.is_owner(project_id=project_id, user_id=current_user.id):
            raise PermissionDeniedError(
                "Solo el propietario puede actualizar este proyecto"
            )
        
        project = service.update_project(
            project_id=project_id, 
            project_update=project_data,
            current_user_id=current_user.id
        )
        
        if not project:
            raise ProjectNotFoundError(f"Proyecto con ID {project_id} no encontrado")
        
        return project
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE - DELETE /api/projects/{project_id}
@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Eliminar proyecto",
    description="Elimina un proyecto. Solo el propietario puede eliminar.",
)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Elimina un proyecto completamente.
    
    ⚠️ Esta acción es irreversible. Se eliminarán:
    - El proyecto
    - Todas sus tareas
    - Todas las asignaciones
    
    Solo el propietario puede eliminar el proyecto.
    """
    # Validar que el usuario no sea READ_ONLY
    if current_user.role == "read_only":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="READ_ONLY users cannot delete projects"
        )
    
    try:
        service = ProjectService(db)
        
        # Verificar que el usuario es propietario
        if not service.is_owner(project_id=project_id, user_id=current_user.id):
            raise PermissionDeniedError(
                "Solo el propietario puede eliminar este proyecto"
            )
        
        success = service.delete_project(project_id=project_id, current_user_id=current_user.id)
        
        if not success:
            raise ProjectNotFoundError(f"Proyecto con ID {project_id} no encontrado")
        
        return MessageResponse(message="Proyecto eliminado exitosamente")
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# MEMBERS - POST /api/projects/{project_id}/members
@router.post(
    "/{project_id}/members",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar miembro al proyecto",
    description="Agrega un usuario como miembro del proyecto. Solo el propietario puede agregar.",
)
async def add_member(
    project_id: int,
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Agrega un usuario como miembro del proyecto.
    
    - **project_id**: ID del proyecto
    - **member_id**: ID del usuario a agregar
    
    Solo el propietario puede agregar miembros.
    """
    # Validar que el usuario no sea READ_ONLY
    if current_user.role == "read_only":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="READ_ONLY users cannot add members to projects"
        )
    
    try:
        service = ProjectService(db)
        
        # Verificar que el usuario es propietario
        if not service.is_owner(project_id=project_id, user_id=current_user.id):
            raise PermissionDeniedError(
                "Solo el propietario puede agregar miembros"
            )
        
        # Verificar que el miembro no es el mismo propietario
        if member_id == current_user.id:
            raise InvalidInputError(
                "El propietario ya es miembro del proyecto"
            )
        
        # Verificar que el miembro no está ya en el proyecto
        if service.is_member(project_id=project_id, user_id=member_id):
            raise InvalidInputError(
                "El usuario ya es miembro del proyecto"
            )
        
        service.add_member(
            project_id=project_id,
            user_id=member_id,
            current_user_id=current_user.id
        )
        
        return MessageResponse(message="Miembro agregado exitosamente")
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# MEMBERS - DELETE /api/projects/{project_id}/members/{member_id}
@router.delete(
    "/{project_id}/members/{member_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Remover miembro del proyecto",
    description="Remueve un usuario del proyecto. Solo el propietario puede remover.",
)
async def remove_member(
    project_id: int,
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Remueve un usuario del proyecto.
    
    - **project_id**: ID del proyecto
    - **member_id**: ID del usuario a remover
    
    Solo el propietario puede remover miembros.
    """
    # Validar que el usuario no sea READ_ONLY
    if current_user.role == "read_only":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="READ_ONLY users cannot remove members from projects"
        )
    
    try:
        service = ProjectService(db)
        
        # Verificar que el usuario es propietario
        if not service.is_owner(project_id=project_id, user_id=current_user.id):
            raise PermissionDeniedError(
                "Solo el propietario puede remover miembros"
            )
        
        # Verificar que no intenta remover al propietario
        project = service.get_project(project_id=project_id)
        if project and project.owner_id == member_id:
            raise InvalidInputError(
                "No puedes remover al propietario del proyecto"
            )
        
        service.remove_member(
            project_id=project_id,
            user_id=member_id,
            current_user_id=current_user.id
        )
        
        return MessageResponse(message="Miembro removido exitosamente")
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
