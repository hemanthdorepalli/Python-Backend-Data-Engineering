from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/status")
def get_status():
    return {
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
