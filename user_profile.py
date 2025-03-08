from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import User
from pydantic import BaseModel

router = APIRouter()

# ✅ Pydantic Schema for Profile Response
class ProfileResponse(BaseModel):
    username: str
    email: str
    country: str | None
    date_of_birth: str | None
    profile_picture: str | None

    class Config:
        from_attributes = True  # ✅ Allows returning SQLAlchemy models as Pydantic

# ✅ Get User Profile by ID
@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user  # ✅ Pydantic will automatically format response
#thank you