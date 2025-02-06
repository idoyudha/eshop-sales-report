from http import HTTPStatus
from fastapi import HTTPException
from typing import Optional
from pydantic import BaseModel

class ErrorMessage(BaseModel):
    message: str
    causes: Optional[str] = None

class RestError(BaseModel):
    code: int
    error: ErrorMessage

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str, causes: Optional[str] = None):
        self.status_code = status_code
        self.error_message = ErrorMessage(message=message, causes=causes)
        super().__init__(status_code=status_code, detail=self.error_message.model_dump())

def unauthorized_error(message: str, causes: Optional[str] = None) -> CustomHTTPException:
    return CustomHTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        message=message,
        causes=causes
    )

def internal_error(message: str, causes: Optional[str] = None) -> CustomHTTPException:
    return CustomHTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=message,
        causes=causes
    )