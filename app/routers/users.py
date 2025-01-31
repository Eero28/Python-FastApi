from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserResponse, UserCreate
from passlib.context import CryptContext
from app.database import get_db

router = APIRouter()


async def get_user(id_user: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id_user == id_user))
    return result.scalar_one_or_none()  



@router.get("/users/{id_user}", response_model=UserResponse)
async def get_one_user(id_user: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await get_user(id_user,db)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

@router.get("/users/", response_model=list[UserResponse])
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

# Route to create a new user
@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(user.password)
        
        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password,  
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
