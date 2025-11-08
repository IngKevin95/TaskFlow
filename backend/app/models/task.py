"""
Task model
"""
from datetime import datetime, timezone, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.core.enums import TaskPriority, TaskStatus


class Task(Base):
    """
    Task model representing project tasks
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    due_date = Column(Date, nullable=True)
    
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    project = relationship(
        "Project",
        back_populates="tasks"
    )
    
    creator = relationship(
        "User",
        back_populates="created_tasks",
        foreign_keys=[creator_id]
    )
    
    assigned_to_user = relationship(
        "User",
        back_populates="assigned_tasks",
        foreign_keys=[assigned_to_id]
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"
