"""
User repository for user data operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List

from app.models.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Repository for user operations"""
    
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        """Get user by username or email"""
        return self.db.query(User).filter(
            or_(User.username == username, User.email == email)
        ).first()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users"""
        return self.db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def get_by_role(self, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        return self.db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
