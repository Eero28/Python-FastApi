from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from sqlalchemy.orm import selectinload
from app.models import Review
from app.schemas import ReviewResponse
from app.database import get_db
from app.helpers.user import get_user
from app.schemas import CreateReview
from typing import List

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)



@router.get("/review/{id_user}", response_model=List[ReviewResponse])
async def get_reviews_with_user(id_user: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await get_user(id_user, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        result = await db.execute(
            select(Review)
            .where(Review.id_user == id_user)  
            .options(selectinload(Review.user))
        )
        reviews_with_user = result.scalars().all() 

        return reviews_with_user  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving reviews: {str(e)}")
    

@router.post("/review/{id_user}", response_model=ReviewResponse)
async def create_review(
    review: CreateReview, 
    id_user: int, 
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await get_user(id_user, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_review = Review(
            reviewname=review.reviewname,
            reviewDescription=review.reviewDescription,
            reviewRating=review.reviewRating,
            imageUrl=review.imageUrl,
            category=review.category,
            id_user=id_user
        )

        db.add(new_review)
        await db.commit()
        await db.refresh(new_review)

        # load relationship
        result = await db.execute(
            select(Review).options(selectinload(Review.user)).filter(Review.id_review == new_review.id_review)
        )
        review_with_user = result.scalars().first()

        return review_with_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating review: {str(e)}")

@router.get("/review", response_model=list[ReviewResponse])
async def get_reviews(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Review).options(selectinload(Review.user)) 
        )
        
        reviews = result.scalars().all()

        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")
