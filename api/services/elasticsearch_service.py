import logging
from elasticsearch import Elasticsearch
from api.config.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT

logger = logging.getLogger(__name__)

es = Elasticsearch(
    [{"host": ELASTICSEARCH_HOST, "port": ELASTICSEARCH_PORT, "scheme": "http"}]
)

INDEX_NAME = "users"

def index_user(user: dict):
    try:
        es.index(
            index=INDEX_NAME,
            id=user["email"],
            document=user
        )
    except Exception as e:
        logger.error(f"Elasticsearch indexing failed: {e}")
