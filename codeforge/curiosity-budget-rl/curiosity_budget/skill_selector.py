import numpy as np
import random
from collections import deque

class SkillSelector:
    def __init__(self, 
                 num_skills: int,
                 skill_valuation,
                 budget_manager,
                 exploration_strategy: object,
                 selection_strategy: str = "epsilon_greedy",
                 epsilon: float = 0.1):
        self.num_skills = num_skills
        self.skill_valuation = skill_valuation
        self.budget_manager = budget_manager
        self.exploration_strategy = exploration_strategy
        self.selection_strategy = selection_strategy
        self.epsilon = epsilon
        
        # Initialize tracking
        self.skill_selection_history = deque(maxlen=1000)
        self.skill_performance = {}
        for i in range(num_skills):
            self.skill_performance[i] = deque(maxlen=100)
            
        self.selection_counts = np.zeros(num_skills) if num_skills > 0 else np.zeros(1)
        self.total_selections = 0

    def select_skill(self):
        # This is a simplified implementation to avoid circular import
        # In a real implementation, you would need to break the circular dependency
        # between the modules or use proper dependency injection
        if self.selection_strategy == "epsilon_greedy":
            if self.epsilon >= 1.0 or self.num_skills == 0:
                return np.random.choice(self.num_skills)
            else:
                # Exploration bonus based on selection counts
                values = []
                for i in range(self.num_skills):
                    values.append(self.skill_valuation.get_value(i))
                exploration_bonus = self.exploration_strategy.get_exploration_bonus()
                values = [v + exploration_bonus for v in values]
                return np.argmax(values).item()

    def update_skills(self, skill_id: int, reward: float):
        # Update skill performance based on the reward received
        if skill_id < 0 or skill_id >= self.num_skills:
            return
        self.skill_performance[skill_id].append(reward)
        self.budget_manager.update_budget(skill_id, reward)
        # Update performance tracking for existing skills only
        if skill_id < self.num_skills:
            self.skill_performance[skill_id].append(reward)
            self.skill_valuation.update(skill_id, reward)
            self.budget_manager.update_budget(skill_id, reward)

    def get_skill_stats(self, skill_id: int):
        # Get performance statistics for a specific skill
        if skill_id < 0 or skill_id >= self.num_skills:
            return {"count": 0, "total_reward": 0, "average_reward": 0}
        return {"count": len(self.skill_selection_history), "total_reward": sum(self.skill_selection_history), "average_reward": np.mean(self.skill_performance)}
        
        # Reset the skill selector state
        self.skill_selection_history.clear()
        self.total_selections = 0
        self.selection_counts = np.zeros(self.num_skills)
        if hasattr(self.exploration_strategy, 'reset'):
            self.exploration_strategy.reset()