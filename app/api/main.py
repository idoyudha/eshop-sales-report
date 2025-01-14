from fastapi import APIRouter

from app.api.routes import sale

api_router = APIRouter()
api_router.include_router(sale.router)