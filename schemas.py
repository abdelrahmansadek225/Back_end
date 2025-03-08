from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    country_and_region: str | None = None
    date_of_birth: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
