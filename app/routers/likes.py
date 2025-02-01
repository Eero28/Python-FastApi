from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.helpers.user import get_user
from app.helpers.reviews import get_review
from app.models import Like, Review, User
from app.schemas import LikeResponse, LikeCreate
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


router = APIRouter(
    prefix='/likes',
    tags=['likes']
)


@router.post('/')
async def add_like(like: LikeCreate, db: AsyncSession = Depends(get_db)):
    try:
        review = await get_review(like.id_review,db)
        
        if not review:
            raise HTTPException(status_code=404, detail='Error retrieving review')
        
        user =  await get_user(like.id_user,db)

        if not user:
            raise HTTPException(status_code=404, detail='Error retrieving user')

        new_like = Like(
            id_user = like.id_user,
            id_review = like.id_review
        )
        
       
        db.add(new_like)
        await db.commit()

        return {'message': 'Like Added', 'like_id': new_like.id_like}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding like: {str(e)}")

@router.get('/')
async def get_likes(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Like)
            .options(selectinload(Like.review), selectinload(Like.user))  
        )

        likes = result.scalars().all()  

        return likes 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving likes: {str(e)}")
    
    
