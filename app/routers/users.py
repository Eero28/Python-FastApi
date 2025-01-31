from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserResponse, UserCreate
from passlib.context import CryptContext
from app.database import get_db  # Importing the get_db function
from app.helpers.user import get_user, hash_password

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get("/users/{id_user}", response_model=UserResponse)
async def get_one_user(id_user: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await get_user(id_user, db)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

@router.get("/users", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@router.delete("/users/{id_user}")
async def delete_user(id_user: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await get_user(id_user, db)
        if user:
            await db.delete(user)
            await db.commit()
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        hashed_password = hash_password(user.password)
        
        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password,
            role=user.role
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
