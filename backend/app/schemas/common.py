"""
Common schemas used across the application
"""
from pydantic import BaseModel
from typing import Optional, Any


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Generic error response"""
    detail: str
    status_code: Optional[int] = None


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool
    message: str
    data: Optional[Any] = None
