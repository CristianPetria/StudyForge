"""
Template API routes
Endpoints for managing and retrieving study guide templates
"""

from flask import Blueprint, jsonify, request
from backend.config import STUDY_TEMPLATES
from backend.utils.logger import get_logger
from backend.agents.template_matching_agent import TemplateMatchingAgent

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


@templates_bp.route('/suggest', methods=['POST'])
def suggest_template():
    """
    POST /api/suggest-template
    Suggests the best study guide template based on user preferences and description
    {
        "age_group": "university",
        "learning_style": "visual",
        "course_type": "business",
        "description": "I need to study marketing frameworks with examples"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body is required"
            }), 400
        
        # Extract user input
        age_group = data.get('age_group', '')
        learning_style = data.get('learning_style', '')
        course_type = data.get('course_type', '')
        description = data.get('description', '')
        
        # Validation
        if not all([age_group, learning_style, course_type, description]):
            return jsonify({
                "status": "error",
                "message": "All fields (age_group, learning_style, course_type, description) are required"
            }), 400
        
        logger.info(f"🎯 Suggesting templates for: age={age_group}, style={learning_style}, course={course_type}")
        
        # Use the template matching agent to find the best template
        matcher = TemplateMatchingAgent()
        
        # Create a combined search query from user input
        search_query = f"{description} {learning_style} {course_type} {age_group}"
        
        # Get template suggestions using Qdrant semantic search with user preferences
        user_preferences = {
            'age_group': age_group,
            'learning_style': learning_style,
            'course_type': course_type
        }
        suggested_templates = matcher.find_best_templates(search_query, top_k=3, user_preferences=user_preferences)
        
        logger.info(f"✅ Found {len(suggested_templates)} template suggestions")
        
        return jsonify({
            "status": "success",
            "suggested_templates": suggested_templates,
            "user_preferences": {
                "age_group": age_group,
                "learning_style": learning_style,
                "course_type": course_type
            }
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error suggesting templates: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to suggest templates: {str(e)}"
        }), 500
