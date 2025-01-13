from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import sales
from app.db.session import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize database
    await init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(
    sales.router,
    prefix=f"{settings.API_V1_STR}/sales",
    tags=["sales"],
)



# TODO: set all CORS enabled origins