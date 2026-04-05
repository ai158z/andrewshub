import pytest
import tempfile
import os
import shutil
from pathlib import Path
from typing import Dict, Any
import numpy as np

# Create a temporary directory for test files
TEST_DATA_DIR = Path(tempfile.gettempdir()) / "ai_skill_library_test"
TEST_DATA_DIR.mkdir(exist_ok=True)

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = TEST_DATA_DIR / "test_run"
    temp_path.mkdir(exist_ok=True)
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def mock_skill_data() -> Dict[str, Any]:
    """Provide mock skill data for testing"""
    return {
        "name": "test_skill",
        "description": "A test skill for unit testing",
        "function_name": "test_function",
        "parameters": {
            "param1": {"type": "string", "description": "Test parameter"},
            "param2": {"type": "integer", "description": "Test integer parameter"}
        },
        "return_type": "string"
    }

@pytest.fixture
def mock_observation_space():
    """Create a mock observation space for testing"""
    return {
        "type": "Box",
        "shape": [10],
        "dtype": "float32",
        "low": -1.0,
        "high": 1.0
    }

@pytest.fixture
def mock_action_space():
    """Create a mock action space for testing"""
    return {
        "type": "Discrete",
        "n": 5
    }

@pytest.fixture
def mock_task_data():
    """Provide mock task data for testing"""
    return {
        "task_id": "test_task_001",
        "description": "Test task for unit testing",
        "required_capabilities": ["text_processing", "data_analysis"],
        "difficulty": 0.5,
        "priority": 1
    }

@pytest.fixture
def sample_skills():
    """Provide sample skills for testing"""
    return [
        {
            "name": "text_classifier",
            "description": "Classifies text into categories",
            "function_ref": "text_classifier_function",
            "parameters": {
                "text": {"type": "string"},
                "categories": {"type": "array", "items": {"type": "string"}}
            }
        },
        {
            "name": "data_analyzer",
            "description": "Analyzes data and extracts insights",
            "function_ref": "data_analyzer_function",
            "parameters": {
                "data": {"type": "array", "items": {"type": "number"}},
                "analysis_type": {"type": "string"}
            }
        }
    ]

@pytest.fixture
def mock_model_weights():
    """Provide mock model weights for testing"""
    return {
        "curiosity_weight": 0.7,
        "task_completion_weight": 0.3,
        "skill_proficiency_weight": 0.5
    }

@pytest.fixture
def mock_environment():
    """Create a mock environment for testing RL components"""
    return {
        "observation_space": {
            "type": "Box",
            "shape": [4],
            "low": -float('inf'),
            "high": float('inf')
        },
        "action_space": {
            "type": "Discrete",
            "n": 2
        }
    }

@pytest.fixture
def cleanup_test_files():
    """Clean up test files after tests"""
    yield
    # Clean up any test files created during testing
    if TEST_DATA_DIR.exists():
        for item in TEST_DATA_DIR.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)

@pytest.fixture
def mock_rl_state():
    """Provide mock RL state for testing"""
    return {
        "observation": np.array([0.1, 0.2, 0.3, 0.4]),
        "reward": 0.0,
        "done": False
    }

@pytest.fixture
def mock_task_outcome():
    """Provide mock task outcome for testing"""
    return {
        "success": True,
        "confidence": 0.95,
        "feedback": "Task completed successfully"
    }

@pytest.fixture
def mock_skill_execution_result():
    """Provide mock skill execution result for testing"""
    return {
        "status": "success",
        "output": "Skill executed successfully",
        "execution_time": 0.1,
        "resource_usage": 0.5
    }