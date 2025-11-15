"""
Backend routes package
Initializes all API blueprints
"""

from backend.routes.health import health_bp
from backend.routes.templates import templates_bp
from backend.routes.guides import guides_bp

def register_routes(app):
    """Register all route blueprints with the Flask app"""
    app.register_blueprint(health_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(guides_bp)
