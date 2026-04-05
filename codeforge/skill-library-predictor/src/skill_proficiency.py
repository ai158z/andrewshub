import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

class SkillProficiencyTracker:
    def __init__(self):
        self.proficiency_data: Dict[str, List[Dict]] = {}
        self.skill_history: Dict[str, List[Dict]] = defaultdict(list)
        self.logger = logging.getLogger(__name__)
        
    def update_proficiency(self, skill_id: str, proficiency_data: Dict, timestamp: datetime) -> None:
        """
        Updates the proficiency of a skill with given data.
        
        Args:
            skill_id: Unique identifier for the skill
            proficiency_data: Dictionary containing proficiency metrics
            timestamp: When the proficiency was recorded
        """
        if not isinstance(skill_id, str):
            raise ValueError("skill_id must be a string")
            
        if not isinstance(proficiency_data, dict):
            raise ValueError("proficiency_data must be a dictionary")
            
        if not isinstance(timestamp, datetime):
            raise ValueError("timestamp must be a datetime object")
            
        entry = {
            "timestamp": timestamp,
            "proficiency_data": proficiency_data
        }
        
        if skill_id in self.proficiency_data:
            self.proficiency_data[skill_id].append(entry)
        else:
            self.proficiency_data[skill_id] = [entry]
            
        self.logger.info(f"Updated proficiency for skill {skill_id} at {timestamp}")
        
    def get_proficiency_history(self, skill_id: str) -> List[Dict]:
        """
        Retrieves the history of proficiency for a given skill.
        
        Args:
            skill_id: Unique identifier for the skill
            
        Returns:
            List of proficiency records with timestamps and metrics
        """
        if not isinstance(skill_id, str):
            raise ValueError("skill_id must be a string")
            
        return self.proficiency_data.get(skill_id, [])
        
    def get_skill_trend(self, skill_id: str, days: int = 30) -> Dict[str, float]:
        """
        Analyzes the trend of a skill's proficiency over time.
        
        Args:
            skill_id: Unique identifier for the skill
            days: Analysis period in days (default: 30)
            
        Returns:
            Dictionary with trend analysis
        """
        if not isinstance(skill_id, str):
            raise ValueError("skill_id must be a string")
            
        history = self.get_proficiency_history(skill_id)
        if not history:
            return {}
            
        # Filter history for the specified time period
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_data = [
            entry for entry in history 
            if entry["timestamp"] >= cutoff_date
        ]
        
        if not recent_data:
            return {}
        
        # Calculate trend based on recent data
        trend = {}
        for entry in recent_data:
            for metric, value in entry["proficiency_data"].items():
                if metric not in trend:
                    trend[metric] = []
                trend[metric].append(value)
                
        # Calculate average proficiency for each metric
        for metric, values in trend.items():
            if values:
                trend[metric] = sum(values) / len(values)
            else:
                trend[metric] = 0.0
                
        return trend

    def get_skill_mastery(self, skill_id: str) -> float:
        """
        Calculates a mastery score for a skill based on recent performance.
        
        Args:
            skill_id: Unique identifier for the skill
            
        Returns:
            Mastery score between 0 and 1
        """
        if not isinstance(skill_id, str):
            raise ValueError("skill_id must be a string")
            
        history = self.get_proficiency_history(skill_id)
        if not history:
            return 0.0
        
        # Get the most recent entry
        latest_entry = max(history, key=lambda x: x["timestamp"])
        # Simple average of all proficiency metrics
        prof_data = latest_entry.get("proficiency_data", {})
        if not prof_data:
            return 0.0
        
        return sum(prof_data.values()) / len(prof_data) if prof_data else 0.0

    def get_declining_skills(self, threshold: float = 0.1, days: int = 30) -> List[str]:
        """
        Identifies skills with declining proficiency over time.
        
        Args:
            threshold: Minimum change to consider a decline
            days: Analysis period in days (default: 30)
            
        Returns:
            List of skill IDs that are declining
        """
        declining_skills = []
        for skill_id in self.proficiency_data:
            trend = self.get_skill_trend(skill_id, days)
            if not trend:
                continue
            decline_detected = False
            for metric, avg_value in trend.items():
                if avg_value < threshold:
                    decline_detected = True
                    break
            if decline_detected:
                declining_skills.append(skill_id)
        return declining_skills