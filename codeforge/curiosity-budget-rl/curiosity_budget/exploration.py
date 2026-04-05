import torch
import numpy as np
import logging
from typing import Any, Dict, Optional, Tuple

class BaseModel:
    """Base model class to avoid import issues"""
    def predict(self, state):
        # Dummy implementation
        return torch.tensor([0.25, 0.25, 0.25, 0.25])

class ExplorationStrategy:
    """Base class for exploration strategies"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def explore(self) -> Any:
        """Main exploration method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement explore method")
    
    def reset(self) -> None:
        """Reset exploration state"""
        raise NotImplementedError("Subclasses must implement reset method")


class EpsilonGreedy(ExplorationStrategy):
    """Epsilon-greedy exploration strategy"""
    
    def __init__(self, epsilon_start: float = 1.0, epsilon_end: float = 0.01, 
                 epsilon_decay: float = 0.995):
        super().__init__()
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.epsilon = epsilon_start
        self.step_count = 0
        
    def explore(self, q_values: torch.Tensor) -> int:
        """
        Epsilon-greedy action selection
        
        Args:
            q_values: Q-values from the model
            
        Returns:
            Selected action index
        """
        if np.random.random() < self.epsilon:
            action = np.random.randint(0, len(q_values))
        else:
            with torch.no_grad():
                action = q_values.argmax().item()
                
        # Decay epsilon
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
        self.step_count += 1
        
        return action
    
    def reset(self) -> None:
        """Reset epsilon to initial value"""
        self.epsilon = self.epsilon_start
        self.step_count = 0


class CuriosityDrivenExploration(ExplorationStrategy):
    """Curiosity-driven exploration using intrinsic rewards"""
    
    def __init__(self, model: BaseModel):
        super().__init__()
        self.model = model
        self.intrinsic_reward_weight = 0.1
        self.exploration_bonus = 0.0
        self.state_visitation_count: Dict[Tuple, int] = {}
        
    def explore(self, state: np.ndarray) -> int:
        """
        Curiosity-driven exploration action selection
        
        Args:
            state: Current environment state
            
        Returns:
            Selected action index
        """
        # Get base policy from model
        action_probs = self.model.predict(state)
        
        # Calculate state novelty bonus
        state_key = tuple(state.flatten()) if isinstance(state, np.ndarray) else state
        visitation_count = self.state_visitation_count.get(state_key, 0)
        novelty_bonus = 1.0 / (visitation_count + 1)
        
        # Update visitation count
        self.state_visitation_count[state_key] = visitation_count + 1
        
        # Combine policy with curiosity bonus
        action = self._select_action_with_bonus(action_probs, novelty_bonus)
        
        return action
    
    def _select_action_with_bonus(self, action_probs: torch.Tensor, 
                                 novelty_bonus: float) -> int:
        """
        Select action with added curiosity bonus
        
        Args:
            action_probs: Action probabilities from policy
            novelty_bonus: Bonus for novel states
            
        Returns:
            Selected action index
        """
        # Add curiosity bonus to action probabilities
        adjusted_probs = action_probs.clone()
        adjusted_probs = adjusted_probs + self.intrinsic_reward_weight * novelty_bonus
        
        # Ensure probabilities are valid
        adjusted_probs = torch.clamp(adjusted_probs, min=1e-10)
        # Normalize probabilities
        adjusted_probs = adjusted_probs / adjusted_probs.sum()
        
        # Sample action according to adjusted probabilities
        with torch.no_grad():
            action = torch.distributions.Categorical(adjusted_probs).sample().item()
            
        return action
    
    def reset(self) -> None:
        """Reset exploration state"""
        self.state_visitation_count.clear()
        self.exploration_bonus = 0.0


class CountBasedExploration(ExplorationStrategy):
    """Count-based exploration strategy"""
    
    def __init__(self, bonus_coefficient: float = 0.01):
        super().__init__()
        self.bonus_coefficient = bonus_coefficient
        self.state_counts: Dict[Tuple, int] = {}
        
    def explore(self, state: np.ndarray) -> int:
        """
        Count-based exploration action selection
        
        Args:
            state: Current environment state
            
        Returns:
            Selected action (random)
        """
        # Get state visitation count
        state_key = tuple(state.flatten()) if isinstance(state, np.ndarray) else state
        count = self.state_counts.get(state_key, 0)
        
        # Update count
        self.state_counts[state_key] = count + 1
        
        # For this simple implementation, we return a random action
        # In a more sophisticated implementation, this would be combined with a policy
        action = np.random.randint(0, 10)  # Assuming 10 possible actions
        
        return action
    
    def reset(self) -> None:
        """Reset exploration counts"""
        self.state_counts.clear()


class ThompsonSamplingExploration(ExplorationStrategy):
    """Thompson sampling exploration strategy"""
    
    def __init__(self, n_arms: int = 10, beta_params: Optional[Tuple[float, float]] = None):
        super().__init__()
        self.n_arms = n_arms
        self.alpha_beta = beta_params or (1.0, 1.0)
        self.successes = np.ones(n_arms)
        self.failures = np.ones(n_arms)
        
    def explore(self) -> int:
        """
        Thompson sampling action selection
        
        Returns:
            Selected arm index
        """
        # Sample from beta distribution for each arm
        samples = np.random.beta(self.successes, self.failures)
        
        # Select arm with highest sample
        action = np.argmax(samples)
        
        return int(action)
    
    def update(self, action: int, reward: float, success_threshold: float = 0.5) -> None:
        """
        Update Thompson sampling statistics
        
        Args:
            action: The action that was taken
            reward: Reward received
            success_threshold: Threshold to determine success/failure
        """
        if reward >= success_threshold:
            self.successes[action] += 1
        else:
            self.failures[action] += 1
    
    def reset(self) -> None:
        """Reset Thompson sampling parameters"""
        self.successes = np.ones(self.n_arms)
        self.failures = np.ones(self.n_arms)


class UCBExploration(ExplorationStrategy):
    """Upper Confidence Bound (UCB) exploration strategy"""
    
    def __init__(self, n_arms: int = 10, c_param: float = 2.0):
        super().__init__()
        self.n_arms = n_arms
        self.c_param = c_param
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)
        self.total_count = 0
        
    def explore(self) -> int:
        """
        UCB action selection
        
        Returns:
            Selected arm index
        """
        # Find arms that have not been pulled yet
        if np.any(self.counts == 0):
            # Return first unpulled arm
            return int(np.argmin(self.counts + (self.counts > 0) * np.inf))
        
        # UCB calculation
        ucb_values = self.values + self.c_param * np.sqrt(
            2 * np.log(self.total_count + 1) / (self.counts + 1e-8)
        )
        
        # Select arm with highest UCB value
        action = int(np.argmax(ucb_values))
        return action
    
    def update(self, arm: int, reward: float) -> None:
        """
        Update UCB statistics
        
        Args:
            arm: The arm that was pulled
            reward: Reward received
        """
        self.counts[arm] += 1
        self.total_count += 1
        self.values[arm] = (self.values[arm] * (self.counts[arm] - 1) + reward) / self.counts[arm]
    
    def reset(self) -> None:
        """Reset UCB parameters"""
        self.counts = np.zeros(self.n_arms)
        self.values = np.zeros(self.n_arms)
        self.total_count = 0


def create_exploration_strategy(strategy_type: str, **kwargs) -> ExplorationStrategy:
    """
    Factory function to create exploration strategies
    
    Args:
        strategy_type: Type of exploration strategy to create
        **kwargs: Strategy-specific parameters
        
    Returns:
        Initialized exploration strategy
    """
    if strategy_type == "epsilon_greedy":
        return EpsilonGreedy(
            epsilon_start=kwargs.get("epsilon_start", 1.0),
            epsilon_end=kwargs.get("epsilon_end", 0.01),
            epsilon_decay=kwargs.get("epsilon_decay", 0.995)
        )
    elif strategy_type == "curiosity_driven":
        return CuriosityDrivenExploration(
            kwargs.get("model")
        )
    elif strategy_type == "count_based":
        return CountBasedExploration(
            bonus_coefficient=kwargs.get("bonus_coefficient", 0.01)
        )
    elif strategy_type == "thompson_sampling":
        return ThompsonSamplingExploration(
            n_arms=kwargs.get("n_arms", 10),
            beta_params=kwargs.get("beta_params")
        )
    elif strategy_type == "ucb":
        return UCBExploration(
            n_arms=kwargs.get("n_arms", 10),
            c_param=kwargs.get("c_param", 2.0)
        )
    else:
        raise ValueError(f"Unknown exploration strategy: {strategy_type}")