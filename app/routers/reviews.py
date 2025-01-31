from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from sqlalchemy.orm import selectinload
from app.database import SessionLocal
from app.models import Review
from app.schemas import ReviewResponse

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/review/", response_model=list[ReviewResponse])
async def get_reviews(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Review).options(selectinload(Review.user)) 
        )
        
        reviews = result.scalars().all()

        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")
