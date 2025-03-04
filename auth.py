from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, User
from pydantic import BaseModel, EmailStr
import bcrypt
import jwt

SECRET_KEY = "Men_In_Black"

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Models
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Password Hashing
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# JWT Token Generation
def create_jwt_token(user_id: int):
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")

# Register Endpoint
@router.post("/register")
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# Login Endpoint
@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user_db.id)
    return {"token": token}
