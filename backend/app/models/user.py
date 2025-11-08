"""
User model
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.core.enums import UserRole


class User(Base):
    """
    User model representing application users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    hashed_password = Column(String(300), nullable=False)  # Aumentado a 300 para bcrypt
    role = Column(String(20), nullable=False, default=UserRole.READ_WRITE.value)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    owned_projects = relationship(
        "Project",
        back_populates="owner",
        foreign_keys="Project.owner_id",
        cascade="all, delete-orphan"
    )
    
    member_projects = relationship(
        "Project",
        secondary="project_members",
        back_populates="members"
    )
    
    created_tasks = relationship(
        "Task",
        back_populates="creator",
        foreign_keys="Task.creator_id",
        cascade="all, delete-orphan"
    )
    
    assigned_tasks = relationship(
        "Task",
        back_populates="assigned_to_user",
        foreign_keys="Task.assigned_to_id"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
