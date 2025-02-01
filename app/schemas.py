from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id_user: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True  


class UserCreate(BaseModel):
    email: str
    password: str
    username: str
    role: str = "user"  


class ReviewResponse(BaseModel):
    id_review: int
    reviewname: str
    reviewDescription: str
    reviewRating: float
    imageUrl: str
    category: str
    createdAt: datetime  
    updatedAt: datetime  
    user: UserResponse  

    class Config:
        from_attributes = True  


class CreateReview(BaseModel):
    reviewname: str
    reviewDescription: str
    reviewRating: float
    imageUrl: str
    category: str  
    
    class Config:
        from_attributes = True
        

class LikeResponse(BaseModel):
    id_like: int
    id_review: int
    id_user: int
    createdAt: str

    class Config:
        from_attributes = True  


class LikeCreate(BaseModel):
    id_user: int
    id_review: int
    class Config:
        from_attributes = True  