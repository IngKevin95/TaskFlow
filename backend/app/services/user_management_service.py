"""
Servicio de gestión de usuarios
Solo accesible para administradores
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.enums import UserRole


class UserManagementService:
    """
    Servicio para gestión de usuarios (solo admin)
    """

    def __init__(self, db: Session):
        """
        Inicializar servicio
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.user_repo = UserRepository(db)
        self.db = db

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        role: str = UserRole.READ_WRITE.value,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> UserRead:
        """
        Crear nuevo usuario (solo admin)
        
        Args:
            username: Nombre de usuario
            email: Email
            password: Contraseña
            role: Rol del usuario (admin, read_write, read_only)
            first_name: Nombre
            last_name: Apellido
            
        Returns:
            Usuario creado
            
        Raises:
            UserAlreadyExistsError: Si el usuario o email ya existen
            ValueError: Si el rol es inválido
        """
        # Validar rol
        valid_roles = [r.value for r in UserRole]
        if role not in valid_roles:
            raise ValueError(f"Rol inválido. Roles válidos: {', '.join(valid_roles)}")

        # Verificar si el usuario ya existe
        if self.user_repo.get_by_username(username):
            raise UserAlreadyExistsError(f"Usuario {username} ya existe")

        if self.user_repo.get_by_email(email):
            raise UserAlreadyExistsError(f"El email {email} ya está registrado")

        # Crear nuevo usuario
        user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=role,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )

        user_created = self.user_repo.create(user)
        return UserRead.from_orm(user_created)

    def get_user(self, user_id: int) -> UserRead:
        """
        Obtener usuario por ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Usuario
            
        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")
        return UserRead.from_orm(user)

    def list_users(self, skip: int = 0, limit: int = 50) -> List[UserRead]:
        """
        Listar todos los usuarios
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de usuarios
        """
        users = self.user_repo.get_all(skip=skip, limit=limit)
        return [UserRead.from_orm(user) for user in users]

    def list_users_by_roles(self, roles: List[str], skip: int = 0, limit: int = 50) -> List[UserRead]:
        """
        Listar usuarios filtrados por rol
        
        Args:
            roles: Lista de roles a filtrar
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de usuarios con los roles especificados
        """
        users = self.db.query(User).filter(User.role.in_(roles)).offset(skip).limit(limit).all()
        return [UserRead.from_orm(user) for user in users]

    def update_user(self, user_id: int, **kwargs) -> UserRead:
        """
        Actualizar usuario - solo campos permitidos: email, first_name, last_name, role
        
        Args:
            user_id: ID del usuario
            **kwargs: Campos a actualizar (email, first_name, last_name, role)
            
        Returns:
            Usuario actualizado
            
        Raises:
            UserNotFoundError: Si el usuario no existe
            ValueError: Si se intenta actualizar un campo no permitido
        """
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        # Campos permitidos
        allowed_fields = ["email", "first_name", "last_name", "role"]
        
        # Validar que no se intenten actualizar campos no permitidos
        for key in kwargs:
            if key not in allowed_fields and kwargs[key] is not None:
                raise ValueError(f"Campo '{key}' no puede ser modificado. Campos permitidos: {', '.join(allowed_fields)}")

        # Preparar diccionario solo con campos permitidos y valores no nulos
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}
        
        # Validar rol si se proporciona
        if "role" in update_data:
            valid_roles = [r.value for r in UserRole]
            if update_data["role"] not in valid_roles:
                raise ValueError(f"Rol inválido. Roles válidos: {', '.join(valid_roles)}")

        # Actualizar solo los campos permitidos
        user_updated = self.user_repo.update(user_id, update_data)
        return UserRead.from_orm(user_updated)

    def delete_user(self, user_id: int) -> bool:
        """
        Eliminar usuario (marcar como inactivo en lugar de eliminar)
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        # No eliminar el usuario, solo marcarlo como inactivo
        self.user_repo.update(user_id, {"is_active": False})
        return True

    def activate_user(self, user_id: int) -> bool:
        """
        Activar usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si se activó exitosamente
            
        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        self.user_repo.update(user_id, {"is_active": True})
        return True

    def change_password(self, user_id: int, new_password: str) -> bool:
        """
        Cambiar contraseña de un usuario
        
        Args:
            user_id: ID del usuario
            new_password: Nueva contraseña
            
        Returns:
            True si se cambió exitosamente
            
        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        self.user_repo.update(user_id, {"hashed_password": hash_password(new_password)})
        return True
