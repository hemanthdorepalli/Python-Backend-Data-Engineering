from sqlalchemy.orm import Session
from api.config.database import SessionLocal
from api.models.user import User

def create_user_db(user_data: dict):
    db: Session = SessionLocal()
    try:
        user = User(**user_data)
        db.add(user)
        db.commit()
    finally:
        db.close()

def get_user_by_email_db(email: str):
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()
