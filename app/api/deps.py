from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session_factory

# def get_db() -> Generator[Session, None, None]:
#     with Session(engine) as session:
#         yield session

# SessionDep = Annotated[Session, Depends(get_db)]

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]