from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings

# async engine
# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(settings.BASE.metadata.create_all)