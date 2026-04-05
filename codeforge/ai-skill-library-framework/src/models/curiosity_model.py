import numpy as np
import logging
from typing import Dict, Any, Optional, Tuple
from src.models.skill import Skill
from src.models.task_predictor import TaskPredictor
from src.models.task_score_model import TaskScoreModel

logger = logging.getLogger(__name__)


class CuriosityModel:
    def __init__(self, 
                 task_predictor: TaskPredictor,
                 task_score_model: TaskScoreModel,
                 curiosity_weight: float = 1.0,
                 novelty_weight: float = 0.5):
        """
        Initialize the CuriosityModel with required dependencies.
        
        Args:
            task_predictor: Instance of TaskPredictor for outcome predictions
            task_score_model: Instance of TaskScoreModel for task scoring
            curiosity_weight: Weight factor for curiosity component
            novelty_weight: Weight factor for novelty component
        """
        self.task_predictor = task_predictor
        self.task_score_model = task_score_model
        self.curiosity_weight = curiosity_weight
        self.novelty_weight = novelty_weight
        self.state_visitation_count: Dict[Tuple, int] = {}
        self.state_action_visitation_count: Dict[Tuple, int] = {}
        
    def compute_curiosity(self,
                          state: np.ndarray,
                          action: Optional[np.ndarray] = None,
                          next_state: Optional[np.ndarray] = None) -> float:
        """
        Compute curiosity score based on state and transition information.
        
        Args:
            state: Current state representation
            action: Action taken (optional)
            next_state: Resulting state (optional)
            
        Returns:
            float: Computed curiosity score
        """
        if state is None:
            raise ValueError("State cannot be None")
            
        # Compute intrinsic reward based on state and transition information
        if next_state is not None and action is not None:
            predicted_next_state = self.task_predictor.predict(state, action)
            prediction_error = np.mean((next_state - predicted_next_state) ** 2)
        else:
            prediction_error = 0.0
            
        # Compute novelty component based on state visitation count
        state_key = tuple(state.flatten()) if hasattr(state, 'flatten') else tuple(state)
        visitation_count = self.state_visitation_count.get(state_key, 0)
        novelty = 1.0 / (1.0 + visitation_count)
        
        # Combine curiosity and novelty components
        curiosity_score = (
            self.curiosity_weight * prediction_error + 
            self.novelty_weight * novelty
        )
        
        logger.debug(f"Computed curiosity score: {curiosity_score}")
        return curiosity_score
        
    def update_curiosity(self, 
                        state: np.ndarray, 
                        action: Optional[np.ndarray] = None,
                        next_state: Optional[np.ndarray] = None) -> None:
        """
        Update curiosity model with new state and transition data.
        
        Args:
            state: Current state representation
            action: Action taken (optional)
            next_state: Resulting state (optional)
        """
        if state is None:
            raise ValueError("State cannot be None")
            
        # Update state visitation count
        state_key = tuple(state.flatten()) if hasattr(state, 'flatten') else tuple(state)
        self.state_visitation_count[state_key] = self.state_visitation_count.get(state_key, 0) + 1
            
        # Update state-action visitation count if action is provided
        if action is not None:
            sa_key = tuple(list(state.flatten()) + list(action.flatten())) if hasattr(state, 'flatten') and hasattr(action, 'flatten') else tuple(list(state) + list(action))
            self.state_action_visitation_count[sa_key] = self.state_action_visitation_count.get(sa_key, 0) + 1
            
        # Update predictor with new data
        if next_state is not None and action is not None:
            try:
                self.task_predictor.train(state, action, next_state)
            except Exception as e:
                logger.error(f"Failed to update curiosity model: {str(e)}")
                raise RuntimeError(f"Failed to update curiosity model: {str(e)}") from e

    def get_state_visitation_count(self, state: np.ndarray) -> int:
        """
        Get the number of times a state has been visited.
        
        Args:
            state: State representation
            
        Returns:
            int: Visitation count for the state
        """
        if state is None:
            raise ValueError("State cannot be None")
            
        state_key = tuple(state.flatten()) if hasattr(state, 'flatten') else tuple(state)
        return self.state_visitation_count.get(state_key, 0)
        
    def get_state_action_visitation_count(self, state: np.ndarray, action: np.ndarray) -> int:
        """
        Get the number of times a state-action pair has been visited.
        
        Args:
            state: State representation
            action: Action taken
            
        Returns:
            int: Visitation count for the state-action pair
        """
        if state is None or action is None:
            raise ValueError("State and action cannot be None")
            
        sa_key = tuple(list(state.flatten()) + list(action.flatten())) if hasattr(state, 'flatten') and hasattr(action, 'flatten') else tuple(list(state) + list(action))
        return self.state_action_visitation_count.get(sa_key, 0)
        
    def reset_counts(self) -> None:
        """Reset all visitation counts."""
        self.state_visitation_count.clear()
        self.state_action_visitation_count.clear()
        
    def get_curiosity_parameters(self) -> Dict[str, float]:
        """
        Get current curiosity model parameters.
        
        Returns:
            Dict[str, float]: Current parameter values
        """
        return {
            'curiosity_weight': self.curiosity_weight,
            'novelty_weight': self.novelty_weight
        }
        
    def set_curiosity_parameters(self, curiosity_weight: float = None, novelty_weight: float = None) -> None:
        """
        Update curiosity model parameters.
        
        Args:
            curiosity_weight: New curiosity weight value
            novelty_weight: New novelty weight value
        """
        if curiosity_weight is not None:
            self.curiosity_weight = curiosity_weight
        if novelty_weight is not None:
            self.novelty_weight = novelty_weight