import os
from flask import Flask
from src.middleware import rate_limit_middleware
from src.utils.endpoint_scanner import register_endpoints
from src.redis_client import connect_to_redis

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Initialize Redis connection
    redis_client = connect_to_redis()
    if redis_client is None:
        raise Exception("Failed to connect to Redis")
    
    # Register endpoints for scanning
    register_endpoints(app)
    
    # Apply rate limiting middleware
    rate_limit_middleware(app)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app

def run_app():
    app = create_app()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_app()