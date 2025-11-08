"""
Enumerations for the application
"""
from enum import Enum


class UserRole(str, Enum):
    """User role levels"""
    ADMIN = "admin"
    READ_WRITE = "read_write"
    READ_ONLY = "read_only"


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task status states"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
