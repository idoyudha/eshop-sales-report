import asyncio
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db
from app.event.consumer import KafkaConsumer

logger = logging.getLogger(__name__)

# store consumer task globally
kafka_consumer_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    global kafka_consumer_task

    # initialize database
    logger.info("Initializing database...")
    await init_db()

    # initialize and start kafka consumer
    logger.info("Initializing kafka consumer...")
    consumer = KafkaConsumer()
    kafka_consumer_task = asyncio.create_task(consumer.start())

    try:
        yield
    finally:
        # shutdown
        if kafka_consumer_task:
            consumer.running = False
            try:
                await asyncio.wait_for(kafka_consumer_task, timeout=10.0)
            except asyncio.TimeoutError:
                kafka_consumer_task.cancel()    
                try:
                    await kafka_consumer_task
                except asyncio.CancelledError:
                    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
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

app.include_router(api_router, prefix=settings.API_V1_STR)