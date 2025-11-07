"""Configuration settings for the Flask application."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg2://postgres:postgres@localhost:5432/flaskdb'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS configuration
    # Comma-separated list of allowed origins. Example:
    # CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://mi-dominio.com
    CORS_ORIGINS = [
        o.strip() for o in os.getenv(
            'CORS_ORIGINS',
            'http://localhost:3000,http://127.0.0.1:3000'
        ).split(',') if o.strip()
    ]
    # Allowed headers for CORS preflight
    CORS_ALLOW_HEADERS = [
        h.strip() for h in os.getenv(
            'CORS_ALLOW_HEADERS',
            'content-type,authorization'
        ).split(',') if h.strip()
    ]
    # Allowed methods for CORS
    CORS_METHODS = [
        m.strip().upper() for m in os.getenv(
            'CORS_METHODS',
            'GET,POST,PUT,DELETE,OPTIONS,PATCH'
        ).split(',') if m.strip()
    ]
    
    # Flask-Smorest configuration
    API_TITLE = "Flask API with Swagger"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
