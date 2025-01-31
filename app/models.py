from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    role = Column(String, default="user")


    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = 'review'

    id_review = Column(Integer, primary_key=True, index=True)
    reviewname = Column(String, index=True)
    reviewDescription = Column(String)
    reviewRating = Column(Numeric(5, 2))
    imageUrl = Column(String)
    category = Column(String)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

    id_user = Column(Integer, ForeignKey('user.id_user', ondelete="CASCADE"))

    user = relationship("User", back_populates="reviews")
