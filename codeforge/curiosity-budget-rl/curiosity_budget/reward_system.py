import logging
import numpy as np
import torch
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple

class RewardSystem:
    def __init__(
        self,
        agent,
        budget_manager,
        skill_selector,
        exploration_strategy,
        skill_valuation,
        models
    ):
        """
        Initialize the RewardSystem with all necessary components.

        Args:
            agent: The curiosity agent instance
            budget_manager: The budget manager instance
            skill_selector: The skill selector instance
            exploration_strategy: The exploration strategy instance
            skill_valuation: The skill valuation instance
            models: Dictionary of model instances
        """
        self.agent = agent
        self.budget_manager = budget_manager
        self.skill_selector = skill_selector
        self.exploration_strategy = exploration_strategy
        self.skill_valuation = skill_valuation
        self.models = models
        self.rewards_history: List[float] = []
        self.intrinsic_rewards: List[float] = []
        self.extrinsic_rewards: List[float] = []

    def calculate_reward(
        self, 
        state: np.ndarray, 
        action: int, 
        next_state: np.ndarray, 
        skill_id: Optional[str] = None
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate the total reward based on intrinsic and extrinsic components.

        Args:
            state: Current state
            action: Action taken
            next_state: Next state
            skill_id: Optional skill identifier
        """
        if state is None or next_state is None:
            raise ValueError("State and next_state cannot be None")

        # Calculate intrinsic reward component
        intrinsic_reward = self._calculate_intrinsic_reward(state, next_state)
        
        # Calculate extrinsic reward component
        extrinsic_reward = self._calculate_extrinsic_reward(state, action, next_state)
        
        # Calculate skill bonus if skill_id provided
        skill_bonus = 0.0
        if skill_id is not None:
            skill_value = self.skill_valuation.get_value(skill_id)
            budget_factor = self.budget_manager.get_budget()
            # Ensure we're working with numeric values
            if isinstance(skill_value, (int, float)) and isinstance(budget_factor, (int, float)):
                skill_bonus = skill_value * budget_factor
            else:
                skill_bonus = 0.0
        
        # Calculate total reward
        total_reward = intrinsic_reward + extrinsic_reward + skill_bonus
        
        # Store reward components for tracking
        components = {
            'intrinsic': intrinsic_reward,
            'extrinsic': extrinsic_reward,
            'skill_bonus': skill_bonus
        }
        
        return total_reward, components

    def _calculate_intrinsic_reward(self, state: np.ndarray, next_state: np.ndarray) -> float:
        """Calculate intrinsic reward based on curiosity model prediction error."""
        if state is None or next_state is None or 'curiosity' not in self.models:
            return 0.0
            
        try:
            with torch.no_grad():
                # Convert numpy arrays to tensors
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
                
                # Get model prediction
                prediction = self.models['curiosity'](state_tensor, next_state_tensor)
                
                # Calculate prediction error as intrinsic reward
                error = F.mse_loss(prediction, next_state_tensor)
                return float(error.item())
        except Exception:
            return 0.0

    def _calculate_extrinsic_reward(self, state: np.ndarray, action: int, next_state: np.ndarray) -> float:
        """Calculate extrinsic reward based on state change."""
        if state is None or next_state is None:
            return 0.0
            
        # Simple distance-based reward
        distance = np.linalg.norm(next_state - state)
        # Normalize to [0,1] range
        reward = 1.0 - np.exp(-distance)
        return max(0.0, min(1.0, reward))

    def update_rewards(
        self, 
        reward: float, 
        state: np.ndarray, 
        action: int, 
        next_state: np.ndarray, 
        skill_id: str = "default"
    ) -> None:
        """
        Update all reward-related components after receiving a reward.

        Args:
            reward: The reward value
            state: Current state
            action: Action taken
            next_state: Next state
            skill_id: Skill identifier for budget updates
        """
        if reward is None:
            raise ValueError("Reward cannot be None")
            
        # Store rewards in history
        self.rewards_history.append(reward)
        # Note: intrinsic/extrinsic rewards are not stored separately in this implementation
        # as we're not tracking components over time, only the total reward
        
        # Update agent with experience
        self.agent.learn(state, action, reward, next_state, skill_id)
        
        # Update skill selector
        self.skill_selector.update_skills(skill_id, reward)
        
        # Update budget manager
        self.budget_manager.update_budget(skill_id, reward)

    def get_reward_statistics(self) -> Dict:
        """Get statistics about reward history."""
        if not self.rewards_history:
            return {
                'mean_total': 0.0,
                'mean_intrinsic': 0.0,
                'mean_extrinsic': 0.0,
                'total_rewards': 0
            }
            
        return {
            'mean_total': float(np.mean(self.rewards_history)) if self.rewards_history else 0.0,
            'mean_intrinsic': float(np.mean(self.intrinsic_rewards)) if self.intrinsic_rewards else 0.0,
            'mean_extrinsic': float(np.mean(self.extrinsic_rewards)) if self.extrinsic_rewards else 0.0,
            'total_rewards': len(self.rewards_history)
        }