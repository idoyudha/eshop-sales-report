from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from http import HTTPStatus
from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
import httpx

from app.api.http_error import unauthorized_error, internal_error

class Data(BaseModel):
    user_id: UUID
    role: str

class AuthResponse(BaseModel):
    code: int
    data: Data
    message: str

class AuthMiddleware:
    def __init__(self, auth_base_url: str):
        self.auth_base_url = auth_base_url
        self.security = HTTPBearer()

    async def __call__(self, request: Request, call_next) -> Any:
        try:
            credentials: HTTPAuthorizationCredentials = await self.security(request)

            if not credentials:
                return unauthorized_error("unauthorized").to_response()
            
            token = credentials.credentials
            auth_url = f"{self.auth_base_url}/v1/auth/{token}"

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(auth_url)
                    if response.status_code != HTTPStatus.OK:
                        return unauthorized_error("unauthorized").to_response()
                    
                    auth_response = AuthResponse.model_validate_json(response.content)
                    if auth_response.data.role != "admin":
                        return unauthorized_error("unauthorized, you are not admin").to_response()

                    request.state.user_id = auth_response.data.user_id
                    return await call_next(request)

                except httpx.RequestError as exc:
                    return internal_error(
                        message="request error", 
                        causes=str(exc)
                    ).to_response()
                except ValueError as exc:
                    return internal_error(
                        message="invalid response from auth service", 
                        causes=str(exc)
                    ).to_response()

        except Exception as exc:
            return internal_error(
                message="Internal server error", 
                causes=str(exc)
            ).to_response()
        try:
            credentials: HTTPAuthorizationCredentials = await self.security(request)

            if not credentials:
                raise unauthorized_error("unauthorized").to_response()
            
            token = credentials.credentials

            auth_url = f"{self.auth_base_url}/v1/auth/{token}"

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(auth_url)
                    if response.status_code != HTTPStatus.OK:
                        raise unauthorized_error("unauthorized").to_response()
                    
                    auth_response = AuthResponse.model_validate(response.content)
                    if response.data.role != "admin":
                        raise unauthorized_error("unauthrorized, you are not admin").to_response()

                    request.state.user_id = auth_response.data.user_id
                    return await call_next(request)

                except httpx.RequestError as exc:
                    raise internal_error(message="request error", causes=str(exc)).to_response()
                except ValueError as exc:
                    raise internal_error(message="invalid response from auth service", causes=str(exc)).to_response()

        except Exception as exc:
            raise internal_error(message="Internal server error", causes=str(exc)).to_response()
    
def create_auth_middleware(auth_base_url: str):
    return AuthMiddleware(auth_base_url)

def requires_auth():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            if not hasattr(request.state, "user_id"):
                raise unauthorized_error("authentication required").to_response()
            return await func(*args, request, **kwargs)
        return wrapper
    return decorator