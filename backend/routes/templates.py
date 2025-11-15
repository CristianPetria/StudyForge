"""
Template API routes
Endpoints for managing and retrieving study guide templates
"""

from flask import Blueprint, jsonify
from backend.config import STUDY_TEMPLATES
from backend.utils.logger import get_logger

logger = get_logger(__name__)

templates_bp = Blueprint('templates', __name__, url_prefix='/api/templates')


@templates_bp.route('', methods=['GET'])
def get_templates():
    """
    GET /api/templates
    Returns all available study guide templates
    """
    logger.info("📋 Fetching all templates")
    return jsonify({
        "status": "success",
        "templates": STUDY_TEMPLATES,
        "count": len(STUDY_TEMPLATES)
    }), 200


@templates_bp.route('/<template_id>', methods=['GET'])
def get_template(template_id):
    """
    GET /api/templates/<template_id>
    Returns a specific template by ID
    """
    template = next((t for t in STUDY_TEMPLATES if t['id'] == template_id), None)
    
    if not template:
        logger.warning(f"Template not found: {template_id}")
        return jsonify({
            "status": "error",
            "message": f"Template '{template_id}' not found"
        }), 404
    
    logger.info(f"📋 Fetching template: {template_id}")
    return jsonify({
        "status": "success",
        "template": template
    }), 200
