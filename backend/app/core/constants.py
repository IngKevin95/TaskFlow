"""
Application constants
"""
from enum import Enum


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


# Priority levels for sorting
PRIORITY_LEVELS = {
    TaskPriority.CRITICAL: 4,
    TaskPriority.HIGH: 3,
    TaskPriority.MEDIUM: 2,
    TaskPriority.LOW: 1,
}

# Status order for display
STATUS_ORDER = {
    TaskStatus.PENDING: 1,
    TaskStatus.IN_PROGRESS: 2,
    TaskStatus.REVIEW: 3,
    TaskStatus.COMPLETED: 4,
}
