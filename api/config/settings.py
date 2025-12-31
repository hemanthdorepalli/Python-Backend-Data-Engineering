import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ---------- Database ----------
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# ---------- Elasticsearch ----------
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
ELASTICSEARCH_PORT = int(os.getenv("ELASTICSEARCH_PORT", 9200))

# ---------- Redis ----------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_TTL = int(os.getenv("REDIS_TTL", 60))
