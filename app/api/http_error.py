from fastapi.responses import JSONResponse
from http import HTTPStatus
from typing import Optional

class ErrorResponse:
    def __init__(self, code: int, message: str, causes: Optional[str] = None):
        self.code = code
        self.message = message
        self.causes = causes

    def to_response(self):
        return JSONResponse(
            status_code=self.code,
            content={
                "code": self.code,
                "error": {
                    "message": self.message,
                    "causes": self.causes
                }
            }
        )

def unauthorized_error(message: str, causes: Optional[str] = None) -> ErrorResponse:
    return ErrorResponse(
        code=HTTPStatus.UNAUTHORIZED.value,
        message=message,
        causes=causes
    )

def internal_error(message: str, causes: Optional[str] = None) -> ErrorResponse:
    return ErrorResponse(
        code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        message=message,
        causes=causes
    )