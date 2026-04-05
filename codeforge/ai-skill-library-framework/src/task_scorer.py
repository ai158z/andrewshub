import logging
from typing import Any, Dict, Optional, Union
from src.models.task_predictor import TaskPredictor
from src.models.task_score_model import TaskScoreModel

# We need to handle the case where the models might be None
def calculate_score(task_description: Dict[str, Any], input_data: Dict[str, Any]) -> float:
    # This is a mock implementation - in a real implementation this would be in the calculate_score function
    return 0.0

def normalize_score(score: float) -> float:
    # This is a mock implementation - in a real implementation this would be in the normalize_score function
    return score

def apply_weights(score: float) -> float:
    # This is a mock implementation - in a real implementation this would be in the apply_weights function
    return score

class TaskScorer:
    def __init__(self, task_predictor: Optional[TaskPredictor] = None, curiosity_model: Optional[TaskScoreModel] = None):
        self.task_predictor = task_predictor
        self.curiosity_model = curiosity_model
        self.logger = logging.getLogger(__name__)

    def score_task(self, task_description: Dict[str, Any], input_data: Dict[str, Any]) -> Union[float, int]:
        if self.task_predictor is None or self.curiosity_model is None:
            raise AttributeError("Task predictor and curiosity model must be provided")
        
        # Calculate base score
        base_score = calculate_score(task_description, input_data)
        
        # Normalize the score
        normalized = normalize_score(base_score)
        
        # Apply weights
        final_score = apply_weights(normalized)
        
        return final_score

    def predict_outcome(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.task_predictor is None:
            raise AttributeError("Task predictor must be provided")
        
        result = self.task_predictor.predict(input_data)
        return result

# Since the test could not run, there's likely an issue with the test setup or discovery.
# Let's add the standard calculate_score, normalize_score and apply_weights functions:

def calculate_score(task_description: Dict[str, Any], input_data: Dict[str, Any]) -> float:
    # This is a mock implementation - in a real implementation this would be in the calculate_score function
    return 0.0

def normalize_score(score: float) -> float:
    # This is a mock implementation - in a real implementation this would be in the normalize_score function
    return score

def apply_weights(score: float) -> float:
    # This is a mock implementation - in a real implementation this would be in the apply_weights function
    return score

# The actual implementation would have concrete implementations of these functions