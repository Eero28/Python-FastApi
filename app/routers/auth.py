from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.database import get_db
from app.models import User
from app.schemas import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from pydantic import BaseModel


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "your-secret-key"
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


class LoginRequest(BaseModel):
    email: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    data["exp"] = datetime.utcnow() + expires_delta 
    data["sub"] = str(data["sub"])  # ensure the subject (user_id) is a string
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        exp = payload.get("exp")
        if exp:
            exp_time = datetime.utcfromtimestamp(exp)
            print(f"Token expiration time: {exp_time}") 
            if exp_time < datetime.utcnow():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        
        return payload
    
    except JWTError as e:
        print(f"JWT error: {str(e)}")  
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first() 


async def get_current_user(token: str = Depends(oauth2_bearer), db: AsyncSession = Depends(get_db)):
    payload = verify_token(token)  # This will raise HTTPException if token is invalid or expired
    id_user_str = payload.get("sub")  # "sub" holds the user ID
    
    if not id_user_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID in token")
  
    try:
        id_user = int(id_user_str)  # Convert "sub" to integer (user ID)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID format")

    result = await db.execute(select(User).filter(User.id_user == id_user))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/token")
async def login_for_access_token(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.email)
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )

    token_data = {"sub": user.id_user} 
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
