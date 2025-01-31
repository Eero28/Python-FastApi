from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    role = Column(String, default="user")
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())


    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = 'review'

    id_review = Column(Integer, primary_key=True, autoincrement=True)
    reviewname = Column(String, index=True)
    reviewDescription = Column(String)
    reviewRating = Column(Numeric(5, 2))
    imageUrl = Column(String)
    category = Column(String)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

    id_user = Column(Integer, ForeignKey('user.id_user', ondelete="CASCADE"))

    user = relationship("User", back_populates="reviews")
