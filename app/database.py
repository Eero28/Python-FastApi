from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from app.models import Base

load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"


engine = create_async_engine(DATABASE_URL, echo=False)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Create tables when app starts
async def create_tables():
    async with engine.begin() as conn:
        try:
            print("Creating tables if they don't exist...")
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully.")
        except Exception as e:
            print(f"Failed to create tables: {e}")


async def get_db():
    async with SessionLocal() as db:
        yield db
