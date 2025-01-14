from fastapi import APIRouter

from app.api.routes import sales

api_router = APIRouter()
api_router.include_router(sales.router)