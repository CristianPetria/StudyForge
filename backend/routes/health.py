"""
Health check and utility API routes
"""

from flask import Blueprint, jsonify
from backend.utils.logger import get_logger

logger = get_logger(__name__)

health_bp = Blueprint('health', __name__, url_prefix='/api')


@health_bp.route('/health', methods=['GET'])
def health_check():
    """GET /api/health - Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({
        "status": "success",
        "message": "StudyForge API is running",
        "version": "2.0.0"
    }), 200


@health_bp.route('/status', methods=['GET'])
def status():
    """GET /api/status - Detailed status information"""
    from backend.utils.clients import get_mistral_client, get_qdrant_client
    
    mistral_ok = get_mistral_client() is not None
    qdrant_ok = get_qdrant_client() is not None
    
    logger.info("Status check requested")
    return jsonify({
        "status": "success",
        "services": {
            "mistral": "✅ Connected" if mistral_ok else "❌ Not Available",
            "qdrant": "✅ Connected" if qdrant_ok else "❌ Not Available"
        },
        "version": "2.0.0"
    }), 200
