from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlmodel.ext.asyncio.session import AsyncSession
from config import config

db_connection_str = config.db_async_connection_str
Base: DeclarativeMeta = declarative_base()

async_engine = create_async_engine(
    db_connection_str,
    echo=True,
    future=True
)

async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)