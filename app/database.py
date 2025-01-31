from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from app.models import Base  

# Load env variables 
load_dotenv()



DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_async_engine(DATABASE_URL, echo=True)

# SessionLocal for async database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Create tables when app starts
async def create_tables():
    async with engine.begin() as conn:
        print("Creating tables if they don't exist...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully.")

async def get_db():
    async with SessionLocal() as session:
        yield session
