"""
Custom exceptions for the application
"""


class TaskFlowException(Exception):
    """Base exception for TaskFlow"""
    pass


class UserAlreadyExistsError(TaskFlowException):
    """Raised when trying to create a user that already exists"""
    pass


class UserNotFoundError(TaskFlowException):
    """Raised when a user is not found"""
    pass


class ProjectNotFoundError(TaskFlowException):
    """Raised when a project is not found"""
    pass


class TaskNotFoundError(TaskFlowException):
    """Raised when a task is not found"""
    pass


class PermissionDeniedError(TaskFlowException):
    """Raised when user doesn't have permission"""
    pass


class InvalidInputError(TaskFlowException):
    """Raised when input is invalid"""
    pass


class InvalidCredentialsError(TaskFlowException):
    """Raised when credentials are invalid"""
    pass


class InvalidTokenError(TaskFlowException):
    """Raised when token is invalid or expired"""
    pass
