from fastapi import FastAPI
from auth import router as auth_router
from profile import router as profile_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])

@app.get("/")
def home():
    return {"message": "Chatbot Backend API is running"}
