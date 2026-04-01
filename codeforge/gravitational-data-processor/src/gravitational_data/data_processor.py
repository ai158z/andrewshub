import pandas as pd
import numpy as np
import logging
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

class DataProcessor:
    """Processes gravitational data and performs statistical computations."""
    
    def process_gravitational_data(self, data: dict) -> pd.DataFrame:
        """
        Process gravitational data from dictionary to pandas DataFrame.
        
        Args:
            data: Dictionary containing gravitational data
            
        Returns:
            pd.DataFrame: Processed data in DataFrame format
        """
        try:
            # Validate input data
            if not isinstance(data, dict):
                raise TypeError("Data must be a dictionary")
            
            if not data:
                raise ValueError("Data dictionary is empty")
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            return df
            
        except Exception as e:
            logger.error(f"Error processing gravitational data: {e}")
            raise
    
    def calculate_statistics(self, data: pd.DataFrame) -> dict:
        """
        Calculate statistical measures from gravitational data.
        
        Args:
            data: DataFrame containing gravitational measurements
            
        Returns:
            dict: Statistical summary including mean, std, min, max, and other metrics
        """
        try:
            if not isinstance(data, pd.DataFrame):
                raise TypeError("Data must be a pandas DataFrame")
            
            if data.empty:
                return {}
            
            # Calculate statistics for each numeric column
            stats = {}
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            
            for col in numeric_columns:
                col_data = data[col].dropna()
                if len(col_data) > 0:
                    stats[col] = {
                        'mean': col_data.mean(),
                        'std': col_data.std(),
                        'min': col_data.min(),
                        'max': col_data.max(),
                        'median': col_data.median(),
                        'count': len(col_data),
                        'missing_values': data[col].isna().sum()
                    }
                else:
                    stats[col] = {
                        'mean': 0.0,
                        'std': 0.0,
                        'min': 0.0,
                        'max': 0.0,
                        'median': 0.0,
                        'count': 0,
                        'missing_values': data[col].isna().sum()
                    }
            
            # Add overall statistics
            stats['data_info'] = {
                'total_rows': len(data),
                'total_columns': len(data.columns),
                'missing_data': data.isna().sum().sum()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            raise
    
    def _validate_input_data(self, data: dict) -> None:
        """Validate the input data structure."""
        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary")
        
        if not data:
            raise ValueError("Input data is empty")
        
        required_fields = ['gravity_measurements']
        if 'gravity_measurements' not in data:
            raise ValueError(f"Missing required fields in data: {required_fields}")
    
    def _validate_dataframe(self, df: pd.DataFrame) -> bool:
        """Validate that the DataFrame has required structure."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
        
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        return True