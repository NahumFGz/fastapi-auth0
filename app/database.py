import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('FAST_API_DB_USERNAME')}:{os.getenv('FAST_API_DB_PASSWORD')}@"
    f"{os.getenv('FAST_API_DB_HOST')}:{os.getenv('FAST_API_DB_PORT')}/{os.getenv('FAST_API_DB_NAME')}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
