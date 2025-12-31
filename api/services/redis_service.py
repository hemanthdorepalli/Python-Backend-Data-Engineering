import redis
import json
import logging
from api.config.settings import REDIS_HOST, REDIS_PORT, REDIS_TTL

logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def get_cached_user(email: str):
    try:
        data = redis_client.get(email)
        return json.loads(data) if data else None
    except Exception as e:
        logger.error(f"Redis GET failed: {e}")
        return None


def cache_user(email: str, user_data: dict):
    try:
        redis_client.setex(
            email,
            REDIS_TTL,
            json.dumps(user_data)
        )
    except Exception as e:
        logger.error(f"Redis SET failed: {e}")
