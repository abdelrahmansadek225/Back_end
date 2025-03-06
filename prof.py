from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import SessionLocal, User
from pydantic import BaseModel
from typing import Optional
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Profile Update Model
class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    date_of_birth: Optional[str] = None  # Expected in "YYYY-MM-DD" format

# Get Profile
@router.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user_db.username,
        "email": user_db.email,
        "country": user_db.country,
        "date_of_birth": user_db.date_of_birth,
        "profile_picture": user_db.profile_picture
    }

# Update Profile
@router.put("/profile/{user_id}")
def update_profile(user_id: int, user_update: ProfileUpdateRequest, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name:
        user_db.username = user_update.name
    if user_update.email:
        user_db.email = user_update.email
    if user_update.country:
        user_db.country = user_update.country
    if user_update.date_of_birth:
        user_db.date_of_birth = user_update.date_of_birth

    db.commit()
    return {"message": "Profile updated"}

# Upload Profile Picture
@router.post("/profile/{user_id}/upload_picture")
def upload_profile_picture(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    file_location = f"{UPLOAD_DIR}/{user_id}_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user_db.profile_picture = file_location
    db.commit()
    return {"message": "Profile picture uploaded", "file_path": file_location}
