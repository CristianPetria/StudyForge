"""
Backend utils package
Common utilities and clients
"""

from backend.utils.logger import get_logger
from backend.utils.clients import get_mistral_client, get_qdrant_client

__all__ = [
    'get_logger',
    'get_mistral_client',
    'get_qdrant_client'
]
