"""
Configuration module for StudyForge backend
Centralizes all configuration, API keys, and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# API KEYS & CREDENTIALS
# ============================================================================

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================

FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
PORT = int(os.getenv('PORT', 5001))
HOST = os.getenv('HOST', '0.0.0.0')

# ============================================================================
# AI MODELS
# ============================================================================

MISTRAL_CHAT_MODEL = "mistral-large-latest"
MISTRAL_EMBED_MODEL = "mistral-embed"
EMBEDDING_DIMENSION = 1024

# ============================================================================
# QDRANT DATABASE
# ============================================================================

QDRANT_IN_MEMORY = os.getenv('QDRANT_IN_MEMORY', 'True') == 'True'
QDRANT_TEMPLATE_COLLECTION = "learning_templates"
QDRANT_ANALYSIS_COLLECTION = "content_analysis"

# ============================================================================
# STUDY TEMPLATES - Load from template_definitions.py
# ============================================================================

from backend.template_definitions import get_all_templates

STUDY_TEMPLATES = get_all_templates()

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
