import logging
from typing import Dict, Any, List, Optional
import os
import json
from src.skill_catalog import SkillCatalog
from src.curiosity_allocator import CuriosityAllocator
from src.task_scorer import TaskScorer
from src.skill_plugins import SkillPlugin
from src.utils import validate_observation_space, validate_action_space, safe_import

class SkillManager:
    def __init__(self):
        self.skill_catalog = SkillCatalog()
        self.curiosity_allocator = CuriosityAllocator()
        self.task_scorer = TaskScorer()
        self.skill_plugins = SkillPlugin()

    def register_skill(self, skill):
        if not skill.validate():
            raise ValueError("Invalid skill data")
        self.skill_catalog.add_skill(skill)

    def execute_skill(self, skill):
        try:
            return self.task_scorer.predict_outcome(skill)
        except Exception as e:
            logging.error(f"Skill execution failed: {e}")
            return {}

    def update_skill(self, skill, action, observation):
        try:
            self.task_scorer.score_task(skill, action, observation)
        except Exception as e:
            self.task_scorer.update_task_score()

    def get_skill(self, skill_name):
        return self.skill_catalog.get_skill(skill_name)

    def add_skill(self, skill):
        self.skill_catalog.add_skill(skill)

    def remove_skill(self, skill_name):
        self.skill_catalog.remove_skill(skill_name)

    def register_skill_plugin(self, plugin_name):
        self.skill_plugins.register(plugin_name)

    def load_plugin(self, plugin_name):
        try:
            self.skill_plugins.load_plugin(plugin_name)
        except Exception as e:
            logging.error(f"Plugin loading failed: {e}")
            self.skill_plugins.unload_plugin(plugin_name)