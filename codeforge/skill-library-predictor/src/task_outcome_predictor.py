import logging
from typing import List, Dict, Any
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

from src.models import Task, Prediction

logger = logging.getLogger(__name__)

class TaskOutcomePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.feature_columns = []
        
    def train_model(self, training_data: List[Dict[str, Any]]) -> bool:
        """
        Train the model with provided training data.
        
        Args:
            training_data: List of dictionaries containing training examples with features and labels
            
        Returns:
            bool: True if training was successful, False otherwise
        """
        try:
            if not training_data:
                logger.warning("No training data provided")
                return False
            
            # Convert to DataFrame for easier handling
            df = pd.DataFrame(training_data)
            
            # Identify feature columns (all except the target 'outcome' column)
            self.feature_columns = [col for col in df.columns if col != 'outcome']
            
            # Prepare features and labels
            X = df[self.feature_columns]
            y = df['outcome'] if 'outcome' in df.columns else None
            
            if y is None:
                logger.error("No 'outcome' column found in training data")
                return False
                
            # Split data for training and validation
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train the model
            self.model.fit(X_train, y_train)
            
            # Validate model performance
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"Model trained with accuracy: {accuracy:.4f}")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def predict_outcome(self, task: Task) -> Prediction:
        """
        Predict the outcome of a task based on its features.
        
        Args:
            task: Task object containing task details
            
        Returns:
            Prediction: Prediction object with outcome and confidence score
        """
        try:
            if not self.is_trained:
                logger.warning("Model is not trained yet")
                return Prediction(
                    task_id=task.id,
                    predicted_outcome=False,
                    confidence=0.0,
                    explanation="Model not trained"
                )
            
            # Prepare feature vector from task
            feature_vector = self._task_to_features(task)
            
            # Make prediction
            prediction_proba = self.model.predict_proba([feature_vector])[0]
            predicted_outcome = bool(self.model.predict([feature_vector])[0])
            confidence = float(np.max(prediction_proba))
            
            return Prediction(
                task_id=task.id,
                predicted_outcome=predicted_outcome,
                confidence=confidence,
                explanation="Prediction based on trained model"
            )
            
        except Exception as e:
            logger.error(f"Error predicting outcome: {str(e)}")
            return Prediction(
                task_id=task.id,
                predicted_outcome=False,
                confidence=0.0,
                explanation="Prediction error occurred"
            )
    
    def _task_to_features(self, task: Task) -> List[float]:
        """Convert task object to feature vector for prediction."""
        # This is a simplified feature extraction
        # In a real implementation, this would be more sophisticated
        features = []
        
        # Example features (to be customized based on actual task data)
        features.append(len(task.description) if task.description else 0)  # Description length
        features.append(task.estimated_duration if task.estimated_duration else 0)  # Estimated duration
        features.append(len(task.required_skills) if task.required_skills else 0)  # Number of required skills
        
        # Pad or trim features to expected length
        while len(features) < len(self.feature_columns):
            features.append(0.0)
            
        return features[:len(self.feature_columns)]