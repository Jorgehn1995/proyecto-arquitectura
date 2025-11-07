"""Flask application factory."""
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from app.config import Config
from app.db import init_db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Avoid 308 redirects between routes with/without trailing slash (which can break CORS on POST)
    app.url_map.strict_slashes = False
    
    # Initialize database
    init_db(app)
    
    # Activate CORS
    CORS(
        app,
        resources={r"/*": {"origins": Config.CORS_ORIGINS}},
        supports_credentials=True,
        methods=Config.CORS_METHODS,
        allow_headers=Config.CORS_ALLOW_HEADERS
    )
    
    # Initialize Flask-Smorest API
    api = Api(app)
    
    # Register blueprints
    from app.api.users import blp as users_blp
    from app.api.reads import blp as reads_blp
    from app.api.access import blp as access_blp
    from app.api.tags import blp as tags_blp
    from app.api.thresholds import blp as thresholds_blp
    
    api.register_blueprint(users_blp)
    api.register_blueprint(reads_blp)
    api.register_blueprint(access_blp)
    api.register_blueprint(tags_blp)
    api.register_blueprint(thresholds_blp)
    
    @app.route('/')
    def index():
        """Root endpoint."""
        return {
            "message": "Flask API with Swagger",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return {"status": "ok"}
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
