from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Response model for user without password (for security)
class UserResponse(BaseModel):
    id_user: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy models to be converted to Pydantic

# Request model for user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: str = "user"  # Default role is 'user'

# Response model for reviews
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
        from_attributes = True  # Allows SQLAlchemy models to be converted to Pydantic
