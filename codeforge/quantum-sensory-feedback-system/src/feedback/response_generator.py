import os
import logging
from typing import Dict, Any
import numpy as np
from redis import Redis
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseGenerator:
    def __init__(self):
        self.redis_client = Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))
        self.response_cache_key = "response_cache"
        
    def generate_feedback(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(processed_data, dict):
            raise ValueError("processed_data must be a dictionary")
            
        # Handle None values in processed_data
        quantum_state = self._handle_none_quantum_state(processed_data.get('quantum_state'))
        sensory_data = processed_data.get('sensory_data', [])
        color_data = processed_data.get('color_data', [])
        
        # Generate responses
        haptic_response = self._generate_haptic_response(quantum_state)
        auditory_response = self._generate_auditory_response(sensory_data)
        visual_response = self._generate_visual_response({'color_data': color_data})
        
        # Combine all responses
        response = {
            'haptic': haptic_response,
            'auditory': auditory_response,
            'visual': visual_response,
            'timestamp': processed_data.get('timestamp', None)
        }
        
        # Cache the response
        self._cache_response(response)
        
        return response

    def _handle_none_quantum_state(self, quantum_state) -> Dict[str, Any]:
        """Handle case when quantum_state is None"""
        if quantum_state is None:
            return {
                'intensity': 0.5,  # Default value
                'frequency': 440,    # Default to A4 note frequency
                'duration': 1000     # milliseconds
            }
        return quantum_state

    def _generate_haptic_response(self, quantum_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate haptic feedback based on quantum_state"""
        try:
            # Handle case when quantum_state is None
            if quantum_state is None:
                return {
                    'type': 'haptic',
                    'intensity': 50,  # Default value
                    'frequency': 440,    # Default to A4 note frequency
                    'duration': 1000    # milliseconds
                }
            
            intensity = quantum_state.get('intensity', 0.5)
            frequency = quantum_state.get('frequency', 440)
            duration = quantum_state.get('duration', 1000)
            
            # Normalize intensity to 0-100 range for haptic motors
            normalized_intensity = min(100, max(0, int(intensity * 100)))
            
            return {
                'type': 'haptic',
                'intensity': normalized_intensity,
                'frequency': frequency,
                'duration': duration
            }
        except Exception as e:
            logger.error(f"Error generating haptic response: {str(e)}")
            return {'type': 'haptic', 'error': 'Failed to generate haptic response'}
    
    def _generate_auditory_response(self, sensory_data: list) -> Dict[str, Any]:
        """Generate auditory response from sensory data"""
        try:
            # Handle empty sensory data
            if not sensory_data:
                mean_amplitude = 0.5
            else:
                # Calculate mean from sensory data
                data_array = np.array(sensory_data)
                if data_array.size > 0:
                    mean_amplitude = np.mean(np.abs(data_array))
                else:
                    mean_amplitude = 0.5
                    
            # Map amplitude to frequency (200Hz to 2000Hz)
            frequency = 200 + (mean_amplitude * 1800)
            
            return {
                'type': 'auditory',
                'frequency': float(frequency),
                'waveform': 'sine',
                'duration': 2000
            }
        except Exception as e:
            logger.error(f"Error generating auditory response: {str(e)}")
            return {'type': 'auditory', 'error': 'Failed to generate auditory response'}
            
    def _generate_visual_response(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual response from processed data"""
        try:
            # Extract color information from data
            color_data = processed_data.get('color_data', [])
            if color_data and len(color_data) > 0:
                # Calculate average color values
                avg_color = np.mean(color_data, axis=0).tolist()
            else:
                avg_color = [128, 128, 128]  # Default gray
            
            return {
                'type': 'visual',
                'color': avg_color,
                'pattern': 'solid',
                'intensity': 0.8
            }
        except Exception as e:
            logger.error(f"Error generating visual response: {str(e)}")
            return {'type': 'visual', 'error': 'Failed to generate visual response'}
    
    def _cache_response(self, response: Dict[str, Any]) -> None:
        """Cache the response in Redis"""
        try:
            # Serialize and store in Redis
            self.redis_client.setex(
                self.response_cache_key,
                300,  # 5 minutes expiration
                json.dumps(response)
            )
        except Exception as e:
            logger.error(f"Error caching response: {str(e)}")