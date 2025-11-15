"""
Centralized AI client initialization
Manages Mistral and Qdrant clients
"""

from mistralai import Mistral
from qdrant_client import QdrantClient
from backend.config import (
    MISTRAL_API_KEY, 
    QDRANT_URL, 
    QDRANT_API_KEY,
    QDRANT_IN_MEMORY
)
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# ============================================================================
# CLIENT INITIALIZATION
# ============================================================================

def init_mistral_client():
    """Initialize Mistral AI client"""
    if not MISTRAL_API_KEY:
        logger.warning("⚠️  MISTRAL_API_KEY not set in environment")
        return None
    
    try:
        client = Mistral(api_key=MISTRAL_API_KEY)
        logger.info("✅ Mistral AI client initialized")
        return client
    except Exception as e:
        logger.error(f"❌ Failed to initialize Mistral client: {e}")
        return None


def init_qdrant_client():
    """Initialize Qdrant vector database client"""
    try:
        if QDRANT_IN_MEMORY:
            client = QdrantClient(":memory:")
            logger.info("✅ Qdrant in-memory client initialized")
        else:
            client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY
            )
            logger.info(f"✅ Qdrant client initialized: {QDRANT_URL}")
        return client
    except Exception as e:
        logger.error(f"❌ Failed to initialize Qdrant client: {e}")
        return None


# Initialize global clients
mistral_client = init_mistral_client()
qdrant_client = init_qdrant_client()


def get_mistral_client():
    """Get Mistral client instance"""
    return mistral_client


def get_qdrant_client():
    """Get Qdrant client instance"""
    return qdrant_client
