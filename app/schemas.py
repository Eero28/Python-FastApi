from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id_user: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True  

# Request model for user creation
class UserCreate(BaseModel):
    email: str
    password: str
    username: str
    role: str = "user"  

# Response model for reviews
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