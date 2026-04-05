import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from curiosity_budget.budget_manager import BudgetManager
from curiosity_budget.budget_allocator import BudgetAllocator
from curiosity_budget.skill_selector import SkillSelector
from curiosity_budget.reward_system import RewardSystem
from curiosity_budget.exploration import ExplorationModule
from curiosity_budget.skill_valuation import SkillValuation
from curiosity_budget.models import ModelManager
from curiosity_budget.utils import Utils
import logging

class CuriosityAgent:
    def __init__(self, config):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.budget_manager = BudgetManager()
        self.budget_allocator = BudgetAllocator()
        self.skill_selector = SkillSelector()
        self.reward_system = RewardSystem()
        self.exploration_module = ExplorationModule()
        self.skill_valuation = SkillValuation()
        self.model_manager = ModelManager()
        self.utils = Utils()
        
        self.budget_manager.update_budget(config)
        self.budget_allocator.update_budget(config)
        self.skill_selector.update_skills(config)
        self.reward_system.update_rewards(config)
        self.exploration_module.reset(config)
        self.skill_valuation.get_value(config)
        
        # Initialize model attribute for learning
        self.model = None
        
    def act(self, state):
        if self.exploration_module and self.exploration_module.should_explore(state):
            return self.skill_selector.select_skill(state)
        else:
            return self.baseline_policy(state)
            
    def baseline_policy(self, state):
        # Simple baseline policy that returns a default action
        return 0

    def learn(self, state, action, reward, next_state, done):
        if done:
            if self.model is not None:
                self.update(state, action, reward, next_state)
            else:
                if self.model_manager:
                    self.model = self.model_manager.model(state) if self.model_manager else None
                    if self.model:
                        self.model.learn(state, action, reward, next_state)
                else:
                    self.model_manager.update(state, action, reward, next_state)
        else:
            if self.exploration_module:
                self.exploration_module.reset()
            
    def load(self, filepath):
        model = self.utils.load_model(filepath)
        return model is not None

    def save(self, filepath):
        result = self.utils.save_model(filepath)
        return result

    def update(self, state, action, reward, next_state):
        if self.model is not None:
            self.model.update(state, action, reward, next_state)
        elif self.model_manager:
            self.model_manager.update(state, action, reward, next_state)