from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Correct Database URL (with port)
DATABASE_URL = "postgresql://postgres:calm_sphere@localhost:5432/chatbot_db"

# ✅ Correct SQLAlchemy 2.0 import
Base = declarative_base()

# ✅ Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ✅ User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    country = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    profile_picture = Column(String, nullable=True)  # Store image file path

# ✅ Initialize DB Function
def init_db():
    Base.metadata.create_all(bind=engine)
