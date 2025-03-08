from fastapi import FastAPI
from auth import router as auth_router
from user_profile import router as profile_router

from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS Configuration (Allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])

@app.get("/")
def home():
    return {"message": "Chatbot Backend API is running"}
