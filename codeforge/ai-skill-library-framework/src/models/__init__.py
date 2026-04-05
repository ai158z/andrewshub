"""
AI Skill Library Framework - Models Package

This module provides the model implementations for the AI skill library framework,
including skill models, curiosity models, and task scoring models.
"""

from typing import Dict, Any, Optional, Union
import numpy as np
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Model package exports
__all__ = [
    'Skill',
    'TaskPredict/20240503
]

class Skill:
    """Represents a skill with validation and serialization capabilities."""
    
    def __init__(self, name: str, description: str = "", parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize a Skill instance.
        
        Args:
            name: Name of the skill
            description: Description of what the skill does
            parameters: Configuration parameters for the skill
        """
        self.name = name
        self.description = description
        self.parameters = parameters or {}
        self._validate()
        logger.info(f"Skill '{self.name}' initialized")

    def _validate(self) -> None:
        """Validate skill parameters."""
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Skill name must be a non-empty string")
        if not isinstance(self.description, str):
            raise ValueError("Skill description must be a string")
        if not isinstance(self.parameters, dict):
            raise ValueError("Skill parameters must be a dictionary")
        logger.debug(f"Skill '{self.name}' validated successfully")

    def validate(self) -> bool:
        """
        Public method to validate the skill configuration.
        
        Returns:
            bool: True if validation passes
        """
        try:
            self._validate()
            return True
        except ValueError as e:
            logger.error(f"Skill validation failed: {e}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert skill to dictionary representation.
        
        Returns:
            Dict containing skill data
        """
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters
        }

class TaskPredictor:
    """Model for predicting task outcomes."""
    
    def __init__(self, model_type: str = "neural_network"):
        """
        Initialize the task predictor.
        
        Args:
            model_type: Type of prediction model to use
        """
        self.model_type = model_type
        self.model = None
        self._initialize_model()
        logger.info(f"TaskPredictor initialized with model type: {model_type}")

    def _initialize_model(self) -> None:
        """Initialize the underlying prediction model."""
        # In a real implementation, this would initialize the actual model
        # For this framework, we're keeping it simple
        pass

    def predict(self, features: np.ndarray) -> float:
        """
        Predict outcome based on input features.
        
        Args:
            features: Input features for prediction
            
        Returns:
            float: Predicted outcome value
        """
        if not isinstance(features, np.ndarray):
            raise TypeError("Features must be a numpy array")
        
        # Simple mock prediction - in practice this would use a trained model
        prediction = float(np.mean(features)) if features.size > 0 else 0.0
        logger.debug(f"Prediction made: {prediction}")
        return prediction

    def train(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Train the prediction model.
        
        Args:
            X: Training features
            y: Training targets
            
        Returns:
            Training metrics
        """
        if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
            raise TypeError("Training data must be numpy arrays")
        
        # Mock training - in practice this would train a model
        metrics = {
            'samples': len(X),
            'loss': float(np.mean((y - np.random.random(len(y))) ** 2)
        }
        logger.info(f"Model trained with {metrics['samples']} samples")
        return metrics

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluate the model performance.
        
        Args:
            X_test: Test features
            y_test: Test targets
            
        Returns:
            Evaluation metrics
        """
        if not isinstance(X_test, np.ndarray) or not isinstance(y_test, np.ndarray):
            raise TypeError("Test data must be numpy arrays")
        
        # Mock evaluation
        predictions = np.random.random(len(y_test))  # In practice, use actual model predictions
        mse = float(np.mean((y_test - predictions)) ** 2)
        
        metrics = {
            'mse': mse,
            'accuracy': float(np.mean(np.abs(y_test - predictions) < 0.1))
        }
        logger.info(f"Model evaluated with MSE: {metrics['mse']}")
        return metrics

class CuriosityModel:
    """Model for computing curiosity-driven exploration bonuses."""
    
    def __init__(self, initial_value: float = 1.0):
        """
        Initialize the curiosity model.
        
        Args:
            initial_value: Starting curiosity value
        """
        self.curiosity_value = initial_value
        self.visit_counts = {}
        logger.info("CuriosityModel initialized")

    def compute_curiosity(self, state: Any) -> float:
        """
        Compute curiosity value for a given state.
        
        Args:
            state: Current state representation
            
        Returns:
            float: Computed curiosity value
        """
        # Simple count-based curiosity model
        state_key = str(state)  # Simplified state representation
        if state_key not in self.visit_counts:
            self.visit_counts[state_key] = 0
        
        # Inverse count-based curiosity: less visited = more curious
        curiosity = 1.0 / (1.0 + self.visit_counts[state_key])
        self.visit_counts[state_key] = curiosity
        logger.debug(f"Curiosity computed: {curiosity} for state {state_key}")
        return curiosity

    def update_curiosity(self, state: Any, reward: float) -> None:
        """
        Update curiosity model based on experience.
        
        Args:
            state: State that was visited
            reward: Reward received
        """
        state_key = str(state)
        current_count = self.visit_counts.get(state_key, 0)
        self.visit_counts[state_key] = current_count + 1
        logger.debug(f"Curiosity model updated for state {state_key}")

class TaskScoreModel:
    """Model for calculating task scores based on multiple factors."""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize the task scoring model.
        
        Args:
            weights: Weights for different scoring components
        """
        self.weights = weights or {
            'complexity': 0.3,
            'priority': 0.4,
            'resource_cost': 0.2,
            'skill_match': 0.1
        }
        self._validate_weights()
        logger.info("TaskScoreModel initialized")

    def _validate_weights(self) -> None:
        """Validate that weights sum to 1.0."""
        total_weight = sum(self.weights.values()
        if not np.isclose(total_weight, 1.0, atol=1e-6):
            raise ValueError(f"TaskScoreModel weights must sum to 1.0, got {total_weight}")

    def calculate_score(self, task_features: Dict[str, Any]) -> float:
        """
        Calculate task score based on features and weights.
        
        Args:
            task_features: Dictionary of task features
            
        Returns:
            float: Calculated task score
        """
        if not isinstance(task_features, dict):
            raise TypeError("Task features must be a dictionary")
        
        score = 0.0
        for feature_name, weight in self.weights:
            feature_value = task_features.get(feature_name, 0.0)
            # Normalize feature values to 0-100 scale for demonstration
            normalized_value = max(0.0, min(1.0, feature_value / 100.0))
            score += weight * normalized_value
        
        logger.debug(f"Task score calculated: {score}")
        return score

    def get_weights(self) -> Dict[str, float]:
        """
        Get current weight configuration.
        
        Returns:
            Current weights dictionary
        """
        return self.weights.copy()