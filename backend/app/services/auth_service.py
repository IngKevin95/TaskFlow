"""
Authentication service
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.core.enums import UserRole


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None
    ) -> User:
        """
        Register a new user
        
        Args:
            username: Unique username
            email: Unique email
            password: Plain password
            first_name: User first name
            last_name: User last name
            
        Returns:
            Created user
            
        Raises:
            UserAlreadyExistsError: If username or email already exists
            ValueError: If input is invalid
        """
        # Validate inputs
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            raise UserAlreadyExistsError(f"User with username or email already exists")
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            first_name=first_name,
            last_name=last_name,
            role=UserRole.READ_WRITE.value,  # Default role
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user
    
    def login(self, username: str, password: str) -> dict:
        """
        Authenticate user and return access token
        
        Args:
            username: Username
            password: Plain password
            
        Returns:
            Dictionary with access_token and token_type
            
        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Find user
        user = self.db.query(User).filter(User.username == username).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid username or password")
        
        if not user.is_active:
            raise InvalidCredentialsError("User is not active")
        
        # Create access token
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "username": user.username,
                "role": user.role
            }
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }
    
    def get_current_user(self, user_id: int) -> User:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object
            
        Raises:
            ValueError: If user not found
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise ValueError("User not found")
        
        return user
