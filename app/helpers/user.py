from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from sqlalchemy.future import select
from passlib.context import CryptContext

async def get_user(id_user: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id_user == id_user))
    return result.scalar_one_or_none()  

def hash_password(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)