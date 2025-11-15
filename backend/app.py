"""
StudyForge - AI-Powered Study Guide Generator
Main Flask application entry point

Architecture:
- Backend: API server with modular agents
- Frontend: Web interface
- Agents: Specialized AI modules for different tasks
  - Analysis Agent: Content analysis
  - Template Matching Agent: Template selection
  - Generation Agent: Study guide creation
  - Coordinator: Orchestrates agent workflow
"""

from flask import Flask, render_template
from flask_cors import CORS
from backend.config import DEBUG, HOST, PORT
from backend.routes import register_routes
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def create_app():
    """Factory function to create and configure Flask app"""
    import os
    from pathlib import Path
    
    # Get absolute paths from project root
    project_root = Path(__file__).parent.parent
    template_folder = project_root / 'frontend' / 'templates'
    static_folder = project_root / 'frontend' / 'static'
    
    app = Flask(
        __name__,
        template_folder=str(template_folder),
        static_folder=str(static_folder),
        static_url_path='/static'
    )

    # Disable template caching in development
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register all API routes
    register_routes(app)
    
    # Serve frontend
    @app.route('/', methods=['GET'])
    def home():
        """Serve the main landing page"""
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"status": "error", "message": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"status": "error", "message": "Internal server error"}, 500
    
    logger.info("✅ Flask app created successfully")
    return app


def main():
    """Application entry point"""
    logger.info("="*80)
    logger.info("🚀 Starting StudyForge API Server")
    logger.info("="*80)
    logger.info(f"Environment: {'Development' if DEBUG else 'Production'}")
    logger.info(f"Server: {HOST}:{PORT}")
    
    app = create_app()
    
    try:
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise


if __name__ == '__main__':
    main()
