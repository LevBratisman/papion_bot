from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database.models import Base
from app.config import settings


# Create async engine
engine = create_async_engine(settings.DB_URL, echo=True)
# Create async session maker
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Create DB
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Drop DB   
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)