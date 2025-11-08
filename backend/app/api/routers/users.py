"""
Router para gestión de usuarios (solo administradores)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead, UserUpdate, UserCreateAdmin, ChangePasswordRequest
from app.services.user_management_service import UserManagementService
from app.database.session import get_db
from app.api.dependencies_rbac import get_current_user_from_header, require_admin
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError, TaskFlowException
from app.core.enums import UserRole

router = APIRouter(prefix="/api/users", tags=["users-admin"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateAdmin,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_header)
):
    """
    Crear nuevo usuario
    
    Reglas según rol del usuario actual:
    - ADMIN: Puede asignar cualquier rol (admin, read_write, read_only)
    - READ_WRITE: Solo puede crear usuarios con rol read_only
    - READ_ONLY: No puede crear usuarios
    
    Args:
        user_data: Datos del usuario a crear (incluye rol deseado)
        db: Sesión de base de datos
        current_user: Usuario actual (debe ser ADMIN o READ_WRITE)
        
    Returns:
        Usuario creado con su rol
        
    Raises:
        HTTPException: Si no tiene permisos o el usuario ya existe
    """
    try:
        # Validar permisos según rol
        if current_user.role == UserRole.READ_ONLY.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users with READ_ONLY role cannot create new users"
            )
        
        # Si es READ_WRITE, solo puede crear READ_ONLY
        role_to_create = user_data.role
        if current_user.role == UserRole.READ_WRITE.value:
            if user_data.role != UserRole.READ_ONLY.value:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"READ_WRITE users can only create READ_ONLY users. Requested: {user_data.role}"
                )
            role_to_create = UserRole.READ_ONLY.value
        
        service = UserManagementService(db)
        new_user = service.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            role=role_to_create,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        return new_user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except TaskFlowException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=list[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_header)
):
    """
    Listar usuarios según rol:
    - ADMIN: ve todos los usuarios
    - READ_WRITE: ve solo READ_WRITE y READ_ONLY
    - READ_ONLY: ve solo READ_ONLY (solo a sí mismo)
    
    Args:
        skip: Número de registros a saltar
        limit: Número máximo de registros
        db: Sesión de base de datos
        current_user: Usuario actual
        
    Returns:
        Lista de usuarios filtrada por rol
    """
    service = UserManagementService(db)
    
    if current_user.role == UserRole.ADMIN.value:
        # ADMIN ve todos
        users = service.list_users(skip=skip, limit=limit)
    elif current_user.role == UserRole.READ_WRITE.value:
        # READ_WRITE ve solo READ_WRITE y READ_ONLY
        users = service.list_users_by_roles(
            roles=[UserRole.READ_WRITE.value, UserRole.READ_ONLY.value],
            skip=skip,
            limit=limit
        )
    else:  # READ_ONLY
        # READ_ONLY ve solo READ_ONLY
        users = service.list_users_by_roles(
            roles=[UserRole.READ_ONLY.value],
            skip=skip,
            limit=limit
        )
    
    return users


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_header)
):
    """
    Obtener usuario por ID según rol:
    - ADMIN: ve cualquier usuario
    - READ_WRITE: ve READ_WRITE y READ_ONLY
    - READ_ONLY: ve solo READ_ONLY (solo a sí mismo o a otros READ_ONLY)
    
    Args:
        user_id: ID del usuario
        db: Sesión de base de datos
        current_user: Usuario actual
        
    Returns:
        Usuario solicitado
    """
    try:
        service = UserManagementService(db)
        user = service.get_user(user_id)
        
        # Validar que el usuario tenga permiso de ver este usuario
        if current_user.role == UserRole.ADMIN.value:
            # ADMIN ve todos
            return user
        elif current_user.role == UserRole.READ_WRITE.value:
            # READ_WRITE ve solo READ_WRITE y READ_ONLY
            if user.role not in [UserRole.READ_WRITE.value, UserRole.READ_ONLY.value]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="READ_WRITE users can only view READ_WRITE and READ_ONLY users"
                )
            return user
        else:  # READ_ONLY
            # READ_ONLY ve solo READ_ONLY
            if user.role != UserRole.READ_ONLY.value:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="READ_ONLY users can only view other READ_ONLY users"
                )
            return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_header)
):
    """
    Actualizar usuario - solo campos permitidos: email, first_name, last_name, role
    
    Reglas según rol del usuario actual:
    - ADMIN: Puede cambiar cualquier rol
    - READ_WRITE: Solo puede cambiar a READ_ONLY
    - READ_ONLY: No puede actualizar usuarios
    
    Args:
        user_id: ID del usuario
        user_update: Datos a actualizar (email, first_name, last_name, role)
        db: Sesión de base de datos
        current_user: Usuario actual (debe ser ADMIN o READ_WRITE)
        
    Returns:
        Usuario actualizado
        
    Raises:
        ValueError: Si ningún campo se proporciona
    """
    if current_user.role == UserRole.READ_ONLY.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="READ_ONLY users cannot update users"
        )
    
    try:
        # Si READ_WRITE intenta cambiar a un rol que no sea READ_ONLY, rechazar
        if current_user.role == UserRole.READ_WRITE.value and user_update.role:
            if user_update.role != UserRole.READ_ONLY.value:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"READ_WRITE users can only set READ_ONLY role. Requested: {user_update.role}"
                )
        
        service = UserManagementService(db)
        updated_user = service.update_user(
            user_id,
            email=user_update.email,
            role=user_update.role,
            first_name=user_update.first_name,
            last_name=user_update.last_name
        )
        return updated_user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_header)
):
    """
    Desactivar usuario (solo ADMIN) - Solo marca como inactivo
    
    Args:
        user_id: ID del usuario
        db: Sesión de base de datos
        current_user: Usuario actual (debe ser ADMIN)
        
    Returns:
        Mensaje de confirmación
    """
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN users can delete users"
        )
    
    try:
        service = UserManagementService(db)
        service.delete_user(user_id)
        return {"message": f"Usuario {user_id} desactivado exitosamente"}
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{user_id}/activate", status_code=status.HTTP_200_OK)
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_header)
):
    """
    Activar usuario (solo ADMIN)
    
    Args:
        user_id: ID del usuario
        db: Sesión de base de datos
        current_user: Usuario actual (debe ser ADMIN)
        
    Returns:
        Mensaje de confirmación
    """
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN users can activate users"
        )
    
    try:
        service = UserManagementService(db)
        service.activate_user(user_id)
        return {"message": f"Usuario {user_id} activado exitosamente"}
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{user_id}/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    user_id: int,
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_header)
):
    """
    Cambiar contraseña de un usuario (solo ADMIN)
    
    Args:
        user_id: ID del usuario
        request: Objeto con la nueva contraseña
        db: Sesión de base de datos
        current_user: Usuario actual (debe ser ADMIN)
        
    Returns:
        Mensaje de confirmación
    """
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN users can change passwords"
        )
    
    try:
        service = UserManagementService(db)
        service.change_password(user_id, request.new_password)
        return {"message": f"Contraseña del usuario {user_id} actualizada exitosamente"}
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
