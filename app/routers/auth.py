from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel
from app.database import get_db
from app.helpers.user import verify_password
from app.models import User
from app.schemas import UserResponse
from dotenv import load_dotenv 
import os
load_dotenv()
router = APIRouter(prefix='/auth', tags=['auth'])


JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
JWT_EXPIRES = os.getenv('JWT_EXPIRES')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

class LoginRequest(BaseModel):
    email: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=int(JWT_EXPIRES))):
    data.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(data, JWT_SECRET, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload  
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token") 


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_current_user(token: str = Depends(oauth2_bearer), db: AsyncSession = Depends(get_db)):
    payload = verify_token(token)
    id_user = payload.get("sub")

    if not id_user or not id_user.isdigit():
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

    user = await db.get(User, int(id_user))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user




@router.post("/token")
async def login_for_access_token(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    # Get user by email
    user = await get_user_by_email(db, form_data.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found") 
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")  

    access_token = create_access_token({"sub": str(user.id_user)})  
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route
@router.get("/protected", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
