import os
from typing import List, Optional
from flask import Flask, request, Response, jsonify
from src.rate_limiter import is_rate_limited
from src.redis_client import connect_to_redis, increment_counter, get_counter
from src.utils.endpoint_scanner import scan_endpoints, register_endpoints
from src.config.rate_limit_config import RATE_LIMIT, WINDOW_SIZE, EXPIRATION

def rate_limit_middleware(app: Flask) -> None:
    """Apply rate limiting middleware to the Flask app."""
    # Initialize Redis connection
    redis_client = connect_to_redis()
    
    @app.before_request
    def before_request():
        return check_rate_limit(request)

def check_rate_limit(request) -> Optional[Response]:
    """Check if the incoming request exceeds rate limits."""
    try:
        client_ip = _get_client_ip(request)
        if not client_ip:
            return jsonify({"error": "Unable to determine client IP"}), 400
            
        # Check if rate limited
        if is_rate_limited(client_ip, RATE_LIMIT, WINDOW_SIZE):
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        # Increment request counter for this IP
        ip_key = f"rate_limit:{client_ip}"
        increment_counter(ip_key)
        
        # Set expiration if not already set
        # This is a simplified version - in production, you might want to use a more sophisticated approach
        # to handle expiration (like using Redis TTL)
        
    except Exception as e:
        # In case of Redis connection issues or other errors, we fail open
        # This ensures that rate limiting issues don't break the application
        print(f"Rate limiting error: {str(e)}")
        return None

def _get_client_ip(request) -> str:
    """Extract client IP from request."""
    # Check for forwarded headers first
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    elif request.environ.get('HTTP_X_REAL_IP'):
        ip = request.environ.get('HTTP_X_REAL_IP')
    else:
        ip = request.environ.get('REMOTE_ADDR')
    return ip if ip else ""