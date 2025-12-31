from fastapi import APIRouter, HTTPException
from api.models.user import UserCreate
from api.services.elasticsearch_service import index_user
from api.services.redis_service import get_cached_user, cache_user
from api.services.user_db_service import create_user_db, get_user_by_email_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user: UserCreate):
    user_dict = user.dict()

    # Store in DB
    existing = get_user_by_email_db(user_dict["email"])
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    create_user_db(user_dict)

    # Index in Elasticsearch
    index_user(user_dict)

    return {"message": "User created successfully"}


@router.get("/{email}")
def fetch_user(email: str):
    # Redis cache
    cached = get_cached_user(email)
    if cached:
        return cached

    # DB lookup
    user = get_user_by_email_db(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = {
        "name": user.name,
        "email": user.email,
        "role": user.role
    }

    # ache result
    cache_user(email, user_data)

    return user_data
