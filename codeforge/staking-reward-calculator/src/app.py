import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    try:
        from src.routes import api, web
        app.register_blueprint(api.bp)
        app.register_blueprint(web.bp)
    except ImportError:
        # Handle case where routes module might not be available
        pass
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
    app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)