from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Review
from sqlalchemy.future import select


async def get_review(id_review: int, db: AsyncSession):
    result = await db.execute(select(Review).filter(Review.id_review == id_review))
    return result.scalar_one_or_none()
