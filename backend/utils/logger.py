"""
Logging utility for StudyForge
Provides centralized logging configuration
"""

import logging
from backend.config import LOG_LEVEL, LOG_FORMAT

def get_logger(name):
    """Get a configured logger instance"""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
