import os
from typing import List
from flask import Flask
from src.middleware import rate_limit_middleware, check_rate_limit


def scan_endpoints(app: Flask) -> List[str]:
    """
    Automatically discover all API endpoints registered in the Flask application.
    
    Args:
        app: Flask application instance
        
    Returns:
        List of endpoint URLs
    """
    endpoints = []
    
    for rule in app.url_map.iter_rules():
        endpoints.append(rule.rule)
        
    return list(dict.fromkeys(endpoints))  # Remove duplicates while preserving order


def register_endpoints(app: Flask) -> None:
    """
    Register all discovered endpoints with rate limiting middleware.
    
    Args:
        app: Flask application instance
    """
    # Apply rate limiting middleware to the app
    rate_limit_middleware(app)
    
    # Scan all endpoints
    endpoints = scan_endpoints(app)
    
    # Log registered endpoints
    app.logger.info(f"Registered {len(endpoints)} endpoints for rate limiting")