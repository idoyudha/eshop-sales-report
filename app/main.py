import asyncio
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db
from app.event.consumer import KafkaConsumer
from app.api.middleware import create_auth_middleware

# initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    await init_db()
    logger.info("Database initialized.")

    kafka_consumer = KafkaConsumer()
    asyncio.create_task(kafka_consumer.start())
    logger.info("Kafka consumer started.")

    yield

    logger.info("Shutting down the application...")

# create fastapu app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# set all cors enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

auth_middleware = create_auth_middleware(auth_base_url=settings.AUTH_BASE_URL)
app.middleware("http")(auth_middleware)

app.include_router(api_router, prefix=settings.API_V1_STR)
