"""
API Router for Tasks
Endpoints: POST, GET, PATCH, DELETE para gestión de tareas
Autenticación requerida para todas las operaciones
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from sqlalchemy.orm import Session

from app.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskReadWithAssignee,
    TaskUpdate,
)
from app.schemas.common import MessageResponse
from app.services.task_service import TaskService
from app.services.project_service import ProjectService
from app.models.models import User
from app.database.session import get_db
from app.api.routers.dependencies import get_current_user
from app.core.enums import TaskStatus
from app.core.exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    PermissionDeniedError,
    InvalidInputError,
)

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={401: {"description": "Unauthorized"}, 404: {"description": "Not Found"}},
)


# CREATE - POST /api/tasks
@router.post(
    "",
    response_model=TaskReadWithAssignee,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva tarea",
    description="Crea una nueva tarea en un proyecto.",
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Crea una nueva tarea en un proyecto.
    
    - **title**: Título de la tarea (requerido)
    - **description**: Descripción (opcional)
    - **project_id**: ID del proyecto (requerido)
    - **priority**: Prioridad (low/medium/high/critical)
    - **assigned_to_id**: ID del usuario asignado (opcional)
    - **due_date**: Fecha de vencimiento (opcional)
    
    El usuario autenticado es automáticamente el creador de la tarea.
    """
    # Validar que el usuario no sea READ_ONLY
    if current_user.role == "read_only":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="READ_ONLY users cannot create tasks"
        )
    
    try:
        project_service = ProjectService(db)
        
        # Verificar que el usuario es miembro del proyecto (o es admin)
        is_admin = current_user.role == "admin"
        is_member = project_service.is_member(
            project_id=task_data.project_id, user_id=current_user.id
        )
        
        if not (is_admin or is_member):
            raise PermissionDeniedError(
                "No tienes permisos para crear tareas en este proyecto"
            )
        
        # Si se asigna a alguien, verificar que ese usuario también es miembro
        if task_data.assigned_to_id:
            if not project_service.is_member(
                project_id=task_data.project_id, user_id=task_data.assigned_to_id
            ):
                raise InvalidInputError(
                    "El usuario asignado no es miembro del proyecto"
                )
        
        task_service = TaskService(db)
        task = task_service.create_task(
            project_id=task_data.project_id,
            task_data=task_data,
            creator_id=current_user.id,
            creator_role=current_user.role,
        )
        return task
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


# READ - GET /api/tasks/project/{project_id}
@router.get(
    "/project/{project_id}",
    response_model=List[TaskReadWithAssignee],
    status_code=status.HTTP_200_OK,
    summary="Listar tareas de un proyecto",
    description="Obtiene todas las tareas de un proyecto específico.",
)
async def get_project_tasks(
    project_id: int,
    status_filter: Optional[str] = Query(
        None, description="Filtrar por estado (pending/in_progress/review/completed)"
    ),
    priority_filter: Optional[str] = Query(
        None, description="Filtrar por prioridad (low/medium/high/critical)"
    ),
    assigned_to_id: Optional[int] = Query(
        None, description="Filtrar por usuario asignado (ID del usuario)"
    ),
    creator_id: Optional[int] = Query(
        None, description="Filtrar por creador de la tarea (ID del usuario)"
    ),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=200, description="Número de registros a retornar"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene la lista de tareas de un proyecto con filtros opcionales.
    
    - **project_id**: ID del proyecto
    - **status_filter**: Filtrar por estado (pending/in_progress/review/completed) - opcional
    - **priority_filter**: Filtrar por prioridad (low/medium/high/critical) - opcional
    - **assigned_to_id**: Filtrar por usuario asignado - opcional
    - **creator_id**: Filtrar por creador de la tarea - opcional
    - **skip**: Offset para paginación (default: 0)
    - **limit**: Número máximo de resultados (default: 50)
    
    Solo miembros del proyecto pueden ver sus tareas.
    """
    try:
        project_service = ProjectService(db)
        
        # Verificar que el usuario es miembro del proyecto (o es admin)
        is_admin = current_user.role == "admin"
        is_member = project_service.is_member(
            project_id=project_id, user_id=current_user.id
        )
        
        if not (is_admin or is_member):
            raise PermissionDeniedError(
                "No tienes permisos para acceder a las tareas de este proyecto"
            )
        
        task_service = TaskService(db)
        tasks = task_service.get_project_tasks(
            project_id=project_id,
            status_filter=status_filter,
            priority_filter=priority_filter,
            assigned_to_id=assigned_to_id,
            creator_id=creator_id,
            skip=skip,
            limit=limit,
        )
        return tasks
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# READ - GET /api/tasks/my-tasks
@router.get(
    "/my-tasks",
    response_model=List[TaskReadWithAssignee],
    status_code=status.HTTP_200_OK,
    summary="Obtener mis tareas",
    description="Obtiene todas las tareas asignadas al usuario autenticado.",
)
async def get_my_tasks(
    status_filter: Optional[str] = Query(
        None, description="Filtrar por estado (pending/in_progress/review/completed)"
    ),
    priority_filter: Optional[str] = Query(
        None, description="Filtrar por prioridad (low/medium/high/critical)"
    ),
    project_id: Optional[int] = Query(
        None, description="Filtrar por proyecto (ID del proyecto)"
    ),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=200, description="Número de registros a retornar"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene todas las tareas asignadas al usuario autenticado con filtros opcionales.
    
    - **status_filter**: Filtrar por estado - opcional
    - **priority_filter**: Filtrar por prioridad - opcional
    - **project_id**: Filtrar por proyecto - opcional
    - **skip**: Offset para paginación (default: 0)
    - **limit**: Número máximo de resultados (default: 50)
    """
    try:
        task_service = TaskService(db)
        tasks = task_service.get_user_assigned_tasks(
            user_id=current_user.id,
            status_filter=status_filter,
            priority_filter=priority_filter,
            project_id=project_id,
            skip=skip,
            limit=limit,
        )
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# READ - GET /api/tasks/user/{user_id}
@router.get(
    "/user/{user_id}",
    response_model=List[TaskReadWithAssignee],
    status_code=status.HTTP_200_OK,
    summary="Obtener tareas asignadas a un usuario",
    description="Obtiene todas las tareas asignadas a un usuario específico, sin importar el proyecto.",
)
async def get_user_assigned_tasks(
    user_id: int,
    status_filter: Optional[str] = Query(
        None, description="Filtrar por estado (pending/in_progress/review/completed)"
    ),
    priority_filter: Optional[str] = Query(
        None, description="Filtrar por prioridad (low/medium/high/critical)"
    ),
    project_id: Optional[int] = Query(
        None, description="Filtrar por proyecto (ID del proyecto)"
    ),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=200, description="Número de registros a retornar"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene todas las tareas asignadas a un usuario específico con filtros opcionales.
    
    - **user_id**: ID del usuario
    - **status_filter**: Filtrar por estado - opcional
    - **priority_filter**: Filtrar por prioridad - opcional
    - **project_id**: Filtrar por proyecto - opcional
    - **skip**: Offset para paginación (default: 0)
    - **limit**: Número máximo de resultados (default: 50)
    
    Solo admin puede ver tareas de otros usuarios. Los demás solo ven sus propias tareas.
    """
    # Validar permisos: solo admin puede ver tareas de otros usuarios
    is_admin = current_user.role == "admin"
    is_same_user = current_user.id == user_id
    
    if not (is_admin or is_same_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver tareas de otros usuarios"
        )
    
    try:
        task_service = TaskService(db)
        tasks = task_service.get_user_assigned_tasks(
            user_id=user_id,
            status_filter=status_filter,
            priority_filter=priority_filter,
            project_id=project_id,
            skip=skip,
            limit=limit,
        )
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# READ - GET /api/tasks/{task_id}
@router.get(
    "/{task_id}",
    response_model=TaskReadWithAssignee,
    status_code=status.HTTP_200_OK,
    summary="Obtener detalle de una tarea",
    description="Obtiene los detalles completos de una tarea.",
)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene los detalles completos de una tarea.
    
    - **task_id**: ID de la tarea
    
    El usuario debe ser miembro del proyecto que contiene la tarea.
    """
    try:
        task_service = TaskService(db)
        task = task_service.get_task(task_id=task_id)
        
        if not task:
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
        
        # Verificar permisos: usuario debe ser miembro del proyecto (o admin)
        project_service = ProjectService(db)
        is_admin = current_user.role == "admin"
        is_member = project_service.is_member(
            project_id=task.project_id, user_id=current_user.id
        )
        
        if not (is_admin or is_member):
            raise PermissionDeniedError(
                "No tienes permisos para acceder a esta tarea"
            )
        
        return task
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# UPDATE - PATCH /api/tasks/{task_id}
@router.patch(
    "/{task_id}",
    response_model=TaskReadWithAssignee,
    status_code=status.HTTP_200_OK,
    summary="Actualizar tarea",
    description="Actualiza los detalles de una tarea.",
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza una tarea existente.
    
    - **title**: Nuevo título (opcional)
    - **description**: Nueva descripción (opcional)
    - **priority**: Nueva prioridad (opcional)
    - **assigned_to_id**: Nuevo usuario asignado (opcional)
    - **status**: Nuevo estado (opcional)
    - **due_date**: Nueva fecha de vencimiento (opcional)
    
    Cualquier miembro del proyecto puede actualizar la tarea, excepto usuarios READ_ONLY.
    Campos no incluidos en la solicitud no serán modificados.
    """
    try:
        # Validar que el usuario no sea READ_ONLY
        if current_user.role == "read_only":
            raise PermissionDeniedError(
                "READ_ONLY users cannot update tasks"
            )
        
        task_service = TaskService(db)
        task = task_service.get_task(task_id=task_id)
        
        if not task:
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
        
        # Verificar que el usuario es miembro del proyecto (o es admin)
        project_service = ProjectService(db)
        is_admin = current_user.role == "admin"
        is_member = project_service.is_member(
            project_id=task.project_id, user_id=current_user.id
        )
        
        if not (is_admin or is_member):
            raise PermissionDeniedError(
                "No eres miembro del proyecto que contiene esta tarea"
            )
        
        # Si se asigna a alguien, verificar que es miembro del proyecto
        if task_data.assigned_to_id:
            if not project_service.is_member(
                project_id=task.project_id, user_id=task_data.assigned_to_id
            ):
                raise InvalidInputError(
                    "El usuario asignado no es miembro del proyecto"
                )
        
        # Preparar datos para actualizar
        update_data = task_data.dict(exclude_unset=True)
        
        updated_task = task_service.update_task(
            task_id=task_id, update_data=update_data
        )
        
        return updated_task
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE - DELETE /api/tasks/{task_id}
@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Eliminar tarea",
    description="Elimina una tarea.",
)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Elimina una tarea.
    
    - **task_id**: ID de la tarea
    
    Solo el creador (propietario) de la tarea puede eliminarla.
    Los usuarios READ_ONLY nunca pueden eliminar tareas.
    """
    try:
        # Validar que el usuario no sea READ_ONLY
        if current_user.role == "read_only":
            raise PermissionDeniedError(
                "READ_ONLY users cannot delete tasks"
            )
        
        task_service = TaskService(db)
        task = task_service.get_task(task_id=task_id)
        
        if not task:
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
        
        # Verificar permisos: solo creador o admin puede eliminar
        is_admin = current_user.role == "admin"
        is_creator = task.creator_id == current_user.id
        
        if not (is_admin or is_creator):
            raise PermissionDeniedError(
                "Solo el creador o un administrador puede eliminar la tarea"
            )
        
        success = task_service.delete_task(task_id=task_id)
        
        if not success:
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
        
        return MessageResponse(message="Tarea eliminada exitosamente")
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# UPDATE STATUS - PATCH /api/tasks/{task_id}/status
@router.patch(
    "/{task_id}/status",
    response_model=TaskReadWithAssignee,
    status_code=status.HTTP_200_OK,
    summary="Actualizar estado de la tarea",
    description="Cambia el estado de una tarea (pending/in_progress/review/completed).",
)
async def update_task_status(
    task_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza el estado de una tarea.
    
    Estados válidos: pending, in_progress, review, completed
    
    - **task_id**: ID de la tarea
    - **new_status**: Nuevo estado
    
    Cualquier miembro del proyecto puede cambiar el estado.
    """
    try:
        # Validar que el estado es válido
        valid_statuses = [s.value for s in TaskStatus]
        if new_status not in valid_statuses:
            raise InvalidInputError(
                f"Estado inválido. Estados válidos: {', '.join(valid_statuses)}"
            )
        
        task_service = TaskService(db)
        task = task_service.get_task(task_id=task_id)
        
        if not task:
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
        
        # Verificar permisos: usuario debe ser miembro del proyecto (o admin)
        project_service = ProjectService(db)
        is_admin = current_user.role == "admin"
        is_member = project_service.is_member(
            project_id=task.project_id, user_id=current_user.id
        )
        
        if not (is_admin or is_member):
            raise PermissionDeniedError(
                "No tienes permisos para actualizar esta tarea"
            )
        
        updated_task = task_service.update_status(
            task_id=task_id, new_status=new_status
        )
        
        return updated_task
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
