import logging
from typing import Dict, Any, List
import numpy as np

class SkillCatalog:
    pass

class TaskScoreModel:
    def __init__(self):
        self.weights = {
            'complexity': 0.3,
            'relevance': 0.4, 
            'novelty': 0.2,
            'impact': 0.1
        }

    def calculate_score(self, task):
        base_score = 0.0
        for factor, weight in self.weights.items():
            if factor in task:
                base_score += task[factor] * weight
        return self.normalize_score(base_score, 0, 100)

    def normalize_score(self, score, min_value=0.0, max_value=100.0):
        if min_value == max_value:
            return 0.0
        if score > max_value:
            return 1.0
        return (score - min_value) / (max_value - min_value)

class TaskScorer:
    def __init__(self, skill_catalog, task_score_model):
        self.skill_catalog = skill_catalog
        self.task_score_model = task_score_model
        self.scores_history = []

    def score_task(self, task):
        score = self.task_score_model.calculate_score(task)
        self.scores_history.append(score)
        return score

class CuriosityAllocator:
    def __init__(self):
        self.budget = 1.0
        self.policy = {}

    def allocate_budget(self):
        return self.budget

    def update_policy(self, new_policy):
        self.policy.update(new_policy)

def apply_weights(scores, weights):
    total_weight = sum(weights.values())
    if total_weight == 0:
        raise ValueError("Sum of weights must be greater than zero")
    weighted_score = 0.0
    for key, value in scores.items():
        weight = weights.get(key, 0.0)
        weighted_score += value * weight
    return weighted_score

def calculate_score(raw_score, min_value=0.0, max_value=100.0):
    if min_value == max_value:
        return 0.0
    if raw_score > max_value:
        return 1.0
    return (raw_score - min_value) / (max_value - min_value)