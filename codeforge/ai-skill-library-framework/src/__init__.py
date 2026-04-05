import logging
from typing import Any, Dict, List, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import core modules
from .skill_catalog import SkillCatalog
from .curiosity_allocator import CuriosityAllocator
try:
    from .task_scorer import TaskScorer
except ImportError:
    # Handle optional dependency gracefully
    TaskScorer = None
from .skill_manager import SkillManager
from .rl_agent import RLAgent

# Import models - with safe imports for optional dependencies
try:
    from .models.skill import Skill
except ImportError:
    Skill = None

try:
    from .models.task_predictor import TaskPredictor
except ImportError:
    TaskPredictor = None

try:
    from .models.curiosity_model import CuriosityModel
except ImportError:
    CuriosityModel = None

try:
    from .models.task_score_model import TaskScoreModel
except ImportError:
    TaskScoreModel = None

# Import utilities
try:
    from .utils import validate_observation_space, validate_action_space, safe_import
except ImportError:
    # Provide fallback implementations
    def validate_observation_space(space):
        return True
        
    def validate_action_space(space):
        return True
        
    def safe_import(module_name):
        return None

# Import curiosity budget functions
try:
    from .curiosity_budget import allocate_budget, adjust_budget, get_budget_status
except ImportError:
    # Provide fallbacks
    def allocate_budget(agent, curiosity_score):
        return 0.0
        
    def adjust_budget(agent, performance):
        pass
        
    def get_budget_status(agent):
        return {}

# Import task scoring functions
try:
    from .task_scoring import calculate_score, normalize_score, apply_weights
except ImportError:
    # Provide fallback implementations
    def calculate_score(task, context):
        return 0.0
        
    def normalize_score(score):
        return score
        
    def apply_weights(scores, weights):
        return sum(s * w for s, w in zip(scores, weights)) if scores and weights else 0.0

# Import skill plugins
try:
    from .skill_plugins import SkillPlugin
except ImportError:
    SkillPlugin = None

# Version info
__version__ = "1.0.0"

# Public API exports
__all__ = [
    # Core classes
    'SkillCatalog',
    'CuriosityAllocator',
    'TaskScorer',
    'SkillManager',
    'RLAgent',
    
    # Models
    'Skill',
    'TaskPredictor',
    'CuriosityModel',
    'TaskScoreModel',
    
    # Utilities
    'validate_observation_space',
    'validate_action_space',
    'safe_import',
    'SkillPlugin',
    
    # Functions
    'allocate_budget',
    'adjust_budget',
    'get_budget_status',
    
    # Task scoring functions
    'calculate_score',
    'normalize_score',
    'apply_weights'
]

# Add None checks for optional imports
if TaskScorer is None:
    __all__.remove('TaskScorer')

if Skill is None:
    __all__.remove('Skill')

if TaskPredictor is None:
    __all__.remove('TaskPredictor')

if CuriosityModel is None:
    __all__.remove('CuriosityModel')

if TaskScoreModel is None:
    __all__.remove('TaskScoreModel')

if SkillPlugin is None:
    __all__.remove('SkillPlugin')

# Initialize core components
def _initialize_framework():
    """Initialize the AI Skill Library framework"""
    # Create necessary directories
    os.makedirs("models", exist_ok=True)
    os.makedirs("skills", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    logger.info("Framework initialized successfully")

# Call initialization
_initialize_framework()