from sqlalchemy import Column, String
from api.config.database import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str
