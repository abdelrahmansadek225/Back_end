from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    """User model representing the users table in the database."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    country = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    profile_picture = Column(String, nullable=True)  # Stores image file path
