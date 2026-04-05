import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.task_outcome_predictor import TaskOutcomePredictor
from src.models import Task, Prediction
from src.skill_library import SkillLibrary
from src.curiosity_budget import CuriosityBudget
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from src.models import Skill, User
from src.utils import calculate_success_rate, normalize_data, format_response
import os

# Remove circular import by not importing SkillProficiencyTracker at module level
# Instead, import it locally when needed

class TaskPredictor:
    def __init__(self):
        self.model = None
        self.feature_importance = None
        self._load_model()
        
    def _load_model(self):
        """Load the trained model from disk or create a new one if it doesn't exist"""
        try:
            if os.path.exists('task_predictor_model.joblib'):
                self.model = joblib.load('task_predictor_model.joblib')
            else:
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                # Create some dummy training to initialize the model
                X = np.random.random((100, 5))
                y = np.random.randint(2, size=100)
                self.model.fit(X, y)
        except Exception as e:
            # Fallback if model loading fails
            logging.error(f"Error loading model: {e}")
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            # Create some dummy training to initialize the model
            X = np.random.random((100, 5))
            y = np.random.randint(2, size=100)
            self.model.fit(X, y)
        return self.model

    def predict_task_outcome(self, task: Task) -> Dict[str, Any]:
        """Predicts task outcome using historical data and ML"""
        try:
            # Extract features from the task
            features = self._extract_features(task)
            
            # Make prediction
            prediction_result = self.model.predict([list(features.values())])[0]
            prediction_probability = self.model.predict_proba([list(features.values())])[0].max()
            
            return {
                "task": task,
                "prediction": prediction_result,
                "confidence": float(prediction_probability)
            }
        except Exception as e:
            logging.error(f"Error in predict_task_outcome: {e}")
            # Return a default prediction if model fails
            return {
                "task": task,
                "prediction": "success",
                "confidence": 0.5
            }

    def _extract_features(self, task: Task) -> Dict[str, Any]:
        """Extract features from task data"""
        features = {}
        # Example features - in a real implementation, this would be more comprehensive
        features['complexity'] = getattr(task, 'complexity', 1) or 1
        features['priority'] = getattr(task, 'priority', 1) or 1
        features['estimated_duration'] = getattr(task, 'estimated_duration', 1) or 1
        return features

    def update_model(self, training_data: List[Dict]) -> bool:
        """Update the model with new training data"""
        try:
            # Convert training data to features and labels
            X = []
            y = []
            
            for data in training_data:
                features = [
                    data.get('complexity', 0),
                    data.get('priority', 1),
                    data.get('estimated_duration', 1)
                ]
                X.append(features)
                y.append(data.get('success', 0))
            
            # Update model with new data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Retrain model
            self.model.fit(X_train, y_train)
            
            # Save model
            joblib.dump(self.model, 'task_predictor_model.joblib')
            
            # Calculate accuracy
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            return True
        except Exception as e:
            logging.error(f"Error updating model: {e}")
            return False

    def get_model_features(self) -> Optional[np.ndarray]:
        """Get the feature importances from the model"""
        try:
            return self.model.feature_importances_
        except:
            return None

    def get_proficiency(self, min_rating: float = 0.0) -> List[Dict]:
        """Get skills with proficiency above minimum rating"""
        try:
            from src.skill_proficiency import SkillProficiencyTracker
            skill_tracker = SkillProficiencyTracker()
            return skill_tracker.get_proficiency(min_rating)
        except Exception as e:
            logging.error(f"Error getting proficiency: {e}")
            return []

    def get_skills(self) -> List[Dict]:
        """Get all skills from library"""
        try:
            skill_library = SkillLibrary()
            return skill_library.get_skills()
        except Exception as e:
            logging.error(f"Error getting skills: {e}")
            return []

    def get_users(self) -> List[User]:
        """Get all users"""
        try:
            # This is a mock implementation - in practice would fetch from user database
            return []
        except Exception as e:
            logging.error(f"Error getting users: {e}")
            return []

    def get_budget(self) -> float:
        """Get curiosity budget"""
        try:
            budget_manager = CuriosityBudget()
            return budget_manager.get_budget()
        except Exception as e:
            logging.error(f"Error getting budget: {e}")
            return 0.0

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            # This is a mock implementation
            return None
        except Exception as e:
            logging.error(f"Error getting user by ID: {e}")
            return None

    def calculate_success_rate(self) -> float:
        """Calculate success rate"""
        try:
            return calculate_success_rate()
        except:
            return 0.0

    def format_response(self) -> Dict:
        """Format response"""
        try:
            return format_response()
        except:
            return {}

    def normalize_data(self) -> float:
        """Normalize data"""
        try:
            return normalize_data()
        except:
            return 0.0

    def get_proficiency_history(self) -> List:
        """Get proficiency history"""
        try:
            from src.skill_proficiency import SkillProficiencyTracker
            tracker = SkillProficiencyTracker()
            return tracker.get_proficiency_history()
        except Exception as e:
            logging.error(f"Error getting proficiency history: {e}")
            return []

    def adjust_budget(self, success_rate: float) -> None:
        """Adjust curiosity budget based on success rate"""
        try:
            budget_manager = CuriosityBudget()
            budget_manager.adjust_budget(success_rate)
        except Exception as e:
            logging.error(f"Error adjusting budget: {e}")