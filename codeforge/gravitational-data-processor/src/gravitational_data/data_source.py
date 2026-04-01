import requests
import json
import logging
from typing import Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)

class DataSource:
    """Handles data retrieval from real-time APIs and static files."""
    
    def fetch_real_time_data(self, url: str) -> Dict[str, Any]:
        """
        Fetch data from a real-time API endpoint.
        
        Args:
            url (str): The URL of the API endpoint to fetch data from
            
        Returns:
            dict: Parsed JSON data from the API
            
        Raises:
            ValueError: If URL is invalid or data cannot be fetched
            ConnectionError: If the API request fails
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")
        
        try:
            logger.info(f"Fetching data from {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            try:
                data = response.json()
                logger.info("Data successfully fetched and parsed")
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON response: {str(e)}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data from {url}: {str(e)}")
            raise ConnectionError(f"Failed to fetch data from {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching data: {str(e)}")
            raise
    
    def load_static_dataset(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from a static file (JSON or CSV).
        
        Args:
            file_path (str): Path to the file to load
            
        Returns:
            dict: Loaded data from the file
            
        Raises:
            ValueError: If file path is invalid or file cannot be read
        """
        if not file_path or not isinstance(file_path, str):
            raise ValueError("File path must be a non-empty string")
        
        try:
            logger.info(f"Loading data from {file_path}")
            
            # Check file extension and load accordingly
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            elif file_path.endswith('.csv'):
                # For CSV, convert to dict format
                df = pd.read_csv(file_path)
                return df.to_dict(orient='records')
            else:
                raise ValueError("Unsupported file format. Only JSON and CSV files are supported.")
                
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
            raise ValueError(f"Invalid JSON in file {file_path}: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            raise ValueError(f"Error loading file {file_path}: {str(e)}")