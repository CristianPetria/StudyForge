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
# STUDY TEMPLATES
# ============================================================================

STUDY_TEMPLATES = [
    {
        "id": "lecture-digest",
        "name": "Lecture Digest",
        "description": "Transform lengthy university lectures into concise, structured summaries with key concepts, definitions, and examples.",
        "icon_emoji": "📋",
        "example_use_case": "Converting 2-hour economics lecture notes into a 2-page study guide",
        "sections": ["Key Concepts", "Definitions", "Important Examples", "Summary Points"]
    },
    {
        "id": "case-study-analyzer",
        "name": "Case Study Analyzer",
        "description": "Break down business cases into problem statements, stakeholder analysis, solutions, and key takeaways.",
        "icon_emoji": "🔍",
        "example_use_case": "Analyzing Harvard Business School cases for strategic management courses",
        "sections": ["Problem Statement", "Stakeholders", "Analysis Framework", "Recommendations", "Key Learnings"]
    },
    {
        "id": "concept-mapper",
        "name": "Concept Mapper",
        "description": "Extract and organize technical concepts with their relationships, dependencies, and practical applications.",
        "icon_emoji": "🗺️",
        "example_use_case": "Creating study guides for programming documentation or technical papers",
        "sections": ["Core Concepts", "Relationships", "Code Examples", "Use Cases", "Best Practices"]
    },
    {
        "id": "exam-prep-sprint",
        "name": "Exam Prep Sprint",
        "description": "Generate focused exam preparation materials with practice questions, key formulas, and critical review points.",
        "icon_emoji": "⚡",
        "example_use_case": "Last-minute review guide for final exams with practice problems",
        "sections": ["Must-Know Topics", "Key Formulas", "Practice Questions", "Common Mistakes", "Quick Review"]
    }
]

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
