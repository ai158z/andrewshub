import logging
from typing import Dict, Tuple, Union
import math

logger = logging.getLogger(__name__)

def validate_data(data: Dict) -> bool:
    """
    Validates if the provided data dictionary contains required gravitational data fields
    and conforms to expected structure.
    
    Args:
        data: Dictionary containing gravitational data to validate
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    try:
        if not isinstance(data, dict):
            logger.error("Data validation failed: input is not a dictionary")
            return False
            
        required_fields = ['latitude', 'longitude', 'gravity_value']
        
        # Check if all required fields exist
        for field in required_fields:
            if field not in data:
                logger.warning(f"Data validation failed: missing required field '{field}'")
                return False
                
        # Validate data types
        if not isinstance(data['latitude'], (int, float)) or not -90 <= data['latitude'] <= 90:
            logger.warning("Invalid latitude value")
            return False
            
        if not isinstance(data['longitude'], (int, float)) or not -180 <= data['longitude'] <= 180:
            logger.warning("Invalid longitude value")
            return False
            
        if not isinstance(data['gravity_value'], (int, float)):
            logger.warning("Invalid gravity_value type")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Data validation error: {str(e)}")
        return False


def transform_coordinates(lat: float, lon: float) -> Tuple[float, float]:
    """
    Transform coordinates from degrees to radians for gravitational calculations.
    
    Args:
        lat: Latitude in degrees
        lon: Longitude in degrees
        
    Returns:
        Tuple of transformed coordinates (lat_rad, lon_rad) in radians
    """
    try:
        # Validate inputs
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            raise TypeError("Latitude and longitude must be numeric values")
            
        if not -90 <= lat <= 90:
            raise ValueError(f"Latitude {lat} is outside valid range [-90, 90]")
            
        if not -180 <= lon <= 180:
            raise ValueError(f"Longitude {lon} is outside valid range [-180, 180]")
            
        # Convert degrees to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        return (lat_rad, lon_rad)
        
    except (TypeError, ValueError) as e:
        logger.error(f"Coordinate transformation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in coordinate transformation: {str(e)}")
        raise e