from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from http import HTTPStatus
from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
import httpx

from app.api.http_error import unauthorized_error, internal_error

class AuthResponse(BaseModel):
    user_id: UUID

class AuthSuccessResponse(BaseModel):
    code: int
    data: AuthResponse
    message: str

class AuthMiddleware:
    def __init__(self, auth_base_url: str):
        self.auth_base_url = auth_base_url
        self.security = HTTPBearer()

    async def __call__(self, request: Request) -> Optional[Dict[str, Any]]:
        credentials: HTTPAuthorizationCredentials = await self.security(request)

        if not credentials:
            raise unauthorized_error("unauthorized")
        
        token = credentials.credentials

        auth_url = f"{self.auth_base_url}/v1/auth/{token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(auth_url)
                if response.status_code != HTTPStatus.OK:
                    raise unauthorized_error("unauthorized")
                
                auth_response = AuthResponse.model_validate(response.content)
                if response.data.role != "admin":
                    raise unauthorized_error("unauthrorized, you are not admin")

                request.state.user_id = auth_response.data.user_id

                return {
                    "user_id": auth_response.data.user_id
                }
            except httpx.RequestError as exc:
                raise internal_error(message="request error", causes=str(exc))
            except ValueError as exc:
                raise internal_error(message="invalid response from auth service", causes=str(exc))
    
def create_auth_middleware(auth_base_url: str):
    return AuthMiddleware(auth_base_url)

def requires_auth():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            if not hasattr(request.state, "user_id"):
                raise unauthorized_error("authentication required")
            return await func(*args, request, **kwargs)
        return wrapper
    return decorator