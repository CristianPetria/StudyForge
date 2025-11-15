"""
Study Guide API routes
Endpoints for analyzing content, matching templates, and generating guides
"""

from flask import Blueprint, request, jsonify
from backend.agents.coordinator import get_coordinator
from backend.agents.analysis_agent import get_analysis_agent
from backend.agents.template_matching_agent import get_template_matching_agent
from backend.agents.generation_agent import get_generation_agent
from backend.utils.logger import get_logger

logger = get_logger(__name__)

guides_bp = Blueprint('guides', __name__, url_prefix='/api')


@guides_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    POST /api/analyze
    Analyzes user-provided content and extracts key information
    
    Request body:
        {
            "content": "string",
            "content_type": "text|pdf|url" (optional)
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            logger.warning("Analyze: Missing 'content' field")
            return jsonify({
                "status": "error",
                "message": "Missing 'content' in request body"
            }), 400
        
        content = data['content']
        content_type = data.get('content_type', 'text')
        
        agent = get_analysis_agent()
        result = agent.analyze_content(content, content_type)
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "message": "Content analyzed successfully",
                "analysis": result['analysis']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/match-template', methods=['POST'])
def match_template():
    """
    POST /api/match-template
    Matches analyzed content to the most appropriate template
    
    Request body:
        {
            "analysis": {...},
            "selected_template_id": "optional"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Match-template: No request body")
            return jsonify({
                "status": "error",
                "message": "Request body required"
            }), 400
        
        analysis = data.get('analysis', {})
        selected_template_id = data.get('selected_template_id')
        
        agent = get_template_matching_agent()
        result = agent.match_template(analysis, selected_template_id)
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "matched_template": result['matched_template'],
                "match_score": result['match_score'],
                "method": result['method']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in match_template endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/generate-guide', methods=['POST'])
def generate_guide():
    """
    POST /api/generate-guide
    Generates the final study guide
    
    Request body:
        {
            "template_id": "string",
            "analysis": {...},
            "customization_options": {
                "length": "short|medium|long",
                "include_examples": boolean,
                "include_questions": boolean
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'template_id' not in data:
            logger.warning("Generate-guide: Missing 'template_id'")
            return jsonify({
                "status": "error",
                "message": "Missing required field: template_id"
            }), 400
        
        template_id = data['template_id']
        analysis = data.get('analysis', {})
        customization = data.get('customization_options', {})
        
        agent = get_generation_agent()
        result = agent.generate_guide(template_id, analysis, customization)
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "study_guide": result['study_guide']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in generate_guide endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/complete-workflow', methods=['POST'])
def complete_workflow():
    """
    POST /api/complete-workflow
    Orchestrates the complete workflow: analyze -> match -> generate
    
    Request body:
        {
            "content": "string",
            "content_type": "text|pdf|url",
            "template_id": "optional - if not provided, AI will match",
            "customization_options": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            logger.warning("Complete-workflow: Missing 'content'")
            return jsonify({
                "status": "error",
                "message": "Missing 'content' in request body"
            }), 400
        
        content = data['content']
        content_type = data.get('content_type', 'text')
        template_id = data.get('template_id')
        customization = data.get('customization_options', {})
        
        coordinator = get_coordinator()
        result = coordinator.process_study_request(
            content,
            content_type,
            template_id,
            customization
        )
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "message": "Study guide generated successfully",
                "workflow": result['workflow']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in complete_workflow endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
