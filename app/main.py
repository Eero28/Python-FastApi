from fastapi import FastAPI
from app.routers import users, reviews
from app.database import create_tables
from contextlib import asynccontextmanager



 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await create_tables()  
    yield  
    print("Shutting down...")

# Routers
app = FastAPI(lifespan=lifespan)
app.include_router(users.router)  
app.include_router(reviews.router) 


@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}