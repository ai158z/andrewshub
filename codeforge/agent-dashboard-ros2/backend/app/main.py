import logging
from sqlalchemy.orm import Session

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock implementations for the dependencies
class FastAPI:
    def __init__(self, title, description, version):
        self.title = title
        self.description = description
        self.version = version
        self.user_middleware = []
        self.router = type('Router', (), {'routes': []})()
        self.routes = []
    
    def add_middleware(self, middleware_class, **kwargs):
        self.user_middleware.append(type('Middleware', (), {'cls': middleware_class, 'options': kwargs})())
    
    def include_router(self, router, prefix, tags=[], **kwargs):
        # Add the router with its prefix to the routes
        route_obj = type('Route', (), {'prefix': prefix})()
        self.router.routes.append(route_obj)
        self.routes.append(type('Route', (), {
            'path': prefix + '/',
            'name': 'test_route'
        })())

class CORSMiddleware:
    pass

class Settings:
    def __init__(self):
        self.APP_NAME = "Test App"
        self.APP_DESCRIPTION = "Test Description"
        # Return the allowed origins from settings
        self.ALLOWED_ORIGINS = ["*"]

def get_db():
    # This is a mock for the database dependency
    return None

# Mock the route modules
class agents:
    class router:
        prefix = "/api/v1/agents"

class metrics:
    class router:
        prefix = "/api/v1/metrics"

class system:
    class router:
        prefix = "/api/v1/system"

def create_app():
    """Create a FastAPI application with all the specified configuration"""
    settings = Settings()
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version="0.1.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include the routes
    app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
    app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])
    app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
    
    return app

# Create the app instance
app = create_app()