from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id_user: int
    username: str
    email: str

    class Config:
        from_attributes = True

class ReviewResponse(BaseModel):
    id_review: int
    reviewname: str
    reviewDescription: Optional[str] = None
    reviewRating: Optional[float] = None
    imageUrl: Optional[str] = None
    category: Optional[str] = None
    createdAt: datetime  
    updatedAt: datetime  
    user: UserResponse
    
    class Config:
        from_attributes = True
