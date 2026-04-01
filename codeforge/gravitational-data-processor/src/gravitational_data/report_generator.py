import pandas as pd
import logging
from typing import Dict, Any
import json
import os

class ReportGenerator:
    def generate_report(self, data: pd.DataFrame) -> str:
        """
        Generate a statistical report from a DataFrame.
        
        Args:
            data (pd.DataFrame): The input data to generate report from
            
        Returns:
            str: JSON formatted statistical report
        """
        if data is None:
            raise ValueError("Data is not a valid DataFrame")
        
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Invalid data type for report generation")
        
        try:
            # Calculate basic statistics
            total_records = len(data)
            columns = list(data.columns)
            
            stats = {
                'total_records': total_records,
                'columns': columns,
                'data': {
                    'type': 'dataframe',
                    'shape': data.shape
                }
            }
            
            return json.dumps(stats, indent=2)
        except Exception as e:
            logging.error("Error generating report", exc_info=e)
            raise

    def export_to_csv(self, data: pd.DataFrame, filename: str) -> None:
        """
        Export data to a CSV file.
        
        Args:
            data: The DataFrame to export
            filename: The filename to export to
        """
        if data is None:
            raise ValueError("Data is not a valid DataFrame")
            
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Invalid data type for export_to_csv")
        
        if not filename.endswith('.csv'):
            raise ValueError("Filename must be a CSV file")
        
        data.to_csv(filename, index=False)