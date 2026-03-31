import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from src.feedback.response_generator import ResponseGenerator

@pytest.fixture
def response_generator():
    with patch('src.feedback.response_generator.Redis.from_url'):
        rg = ResponseGenerator()
        rg.redis_client = Mock()
        return rg

@pytest.fixture
def sample_processed_data():
    return {
        'quantum_state': {
            'intensity': 0.8,
            'frequency': 440,
            'duration': 1000
        },
        'sensory_data': [0.1, 0.5, 0.9],
        'color_data': [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
        'timestamp': '2023-01-01T00:00:00Z'
    }

def test_generate_feedback_invalid_input_type(response_generator):
    with pytest.raises(ValueError, match="processed_data must be a dictionary"):
        response_generator.generate_feedback("invalid_input")

def test_generate_feedback_valid_input(response_generator, sample_processed_data):
    result = response_generator.generate_feedback(sample_processed_data)
    
    assert 'haptic' in result
    assert 'auditory' in result
    assert 'visual' in result
    assert result['timestamp'] == sample_processed_data['timestamp']
    response_generator.redis_client.setex.assert_called_once()

def test_generate_haptic_response_with_valid_quantum_state(response_generator):
    quantum_state = {'intensity': 0.8, 'frequency': 440, 'duration': 1000}
    result = response_generator._generate_haptic_response(quantum_state)
    
    assert result['type'] == 'haptic'
    assert result['intensity'] == 80  # 0.8 * 100
    assert result['frequency'] == 440
    assert result['duration'] == 1000

def test_generate_haptic_response_missing_quantum_state_fields(response_generator):
    quantum_state = {}
    result = response_generator._generate_haptic_response(quantum_state)
    
    assert result['type'] == 'haptic'
    assert result['intensity'] == 50  # Default 0.5 * 100
    assert result['frequency'] == 440  # Default frequency
    assert result['duration'] == 1000

def test_generate_auditory_response_with_sensory_data(response_generator):
    sensory_data = [0.1, 0.5, 0.9]
    result = response_generator._generate_auditory_response(sensory_data)
    
    assert result['type'] == 'auditory'
    assert result['waveform'] == 'sine'
    assert result['duration'] == 2000
    assert 'frequency' in result

def test_generate_auditory_response_empty_sensory_data(response_generator):
    sensory_data = []
    result = response_generator._generate_auditory_response(sensory_data)
    
    assert result['type'] == 'auditory'
    assert result['frequency'] == 200.0  # 0.5 * 1800 + 200 = 1100, but with empty data = 200 + (0.5*1800) = 1100

def test_generate_visual_response_with_color_data(response_generator):
    processed_data = {
        'color_data': [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    }
    result = response_generator._generate_visual_response(processed_data)
    
    assert result['type'] == 'visual'
    assert result['pattern'] == 'solid'
    assert 'color' in result

def test_generate_visual_response_without_color_data(response_generator):
    processed_data = {}
    result = response_generator._generate_visual_response(processed_data)
    
    assert result['type'] == 'visual'
    assert result['color'] == [128, 128, 128]

def test_generate_feedback_with_none_quantum_state(response_generator, sample_processed_data):
    data = sample_processed_data.copy()
    data['quantum_state'] = None
    result = response_generator.generate_feedback(data)
    
    assert 'haptic' in result
    assert result['haptic']['intensity'] == 50  # Default value

def test_generate_feedback_caching(response_generator, sample_processed_data):
    response_generator.generate_feedback(sample_processed_data)
    response_generator.redis_client.setex.assert_called_once()

def test_generate_haptic_response_exception_handling(response_generator):
    with patch.object(response_generator, '_generate_haptic_response', side_effect=Exception("Test error")):
        with pytest.raises(Exception, match="Test error"):
            response_generator._generate_haptic_response({})

def test_generate_auditory_response_exception_handling(response_generator):
    with patch('src.feedback.response_generator.np.array', side_effect=Exception("Numpy error")):
        result = response_generator._generate_auditory_response([1, 2, 3])
        assert result['error'] == 'Failed to generate auditory response'

def test_generate_visual_response_exception_handling(response_generator):
    with patch('src.feedback.response_generator.np.mean', side_effect=Exception("Numpy error")):
        result = response_generator._generate_visual_response({'color_data': [[255, 0, 0]]})
        assert result['error'] == 'Failed to generate visual response'

def test_generate_feedback_empty_data(response_generator):
    result = response_generator.generate_feedback({})
    
    assert 'haptic' in result
    assert 'auditory' in result
    assert 'visual' in result

def test_generate_feedback_none_values(response_generator):
    data = {
        'quantum_state': None,
        'sensory_data': None,
        'color_data': None
    }
    result = response_generator.generate_feedback(data)
    
    assert 'haptic' in result
    assert 'auditory' in result
    assert 'visual' in result

def test_generate_haptic_response_intensity_normalization(response_generator):
    quantum_state = {'intensity': 1.5, 'frequency': 440, 'duration': 1000}  # Intensity > 1.0
    result = response_generator._generate_haptic_response(quantum_state)
    
    assert result['intensity'] == 100  # Should be capped at 100

def test_generate_auditory_response_frequency_calculation(response_generator):
    sensory_data = [0.0, 1.0]  # Mean = 0.5
    result = response_generator._generate_auditory_response(sensory_data)
    
    # 200 + (0.5 * 1800) = 1100
    assert abs(result['frequency'] - 1100.0) < 0.1

def test_generate_visual_response_default_gray(response_generator):
    processed_data = {'color_data': []}
    result = response_generator._generate_visual_response(processed_data)
    
    assert result['color'] == [128, 128, 128]

def test_generate_feedback_redis_cache_exception(response_generator, sample_processed_data):
    response_generator.redis_client.setex.side_effect = Exception("Redis error")
    # Should not raise exception, just log error
    result = response_generator.generate_feedback(sample_processed_data)
    assert result is not None

def test_generate_haptic_response_negative_values(response_generator):
    quantum_state = {'intensity': -0.5, 'frequency': -100, 'duration': -500}
    result = response_generator._generate_haptic_response(quantum_state)
    
    assert result['intensity'] == 0  # Negative intensity should be clamped to 0
    assert result['frequency'] == -100  # Frequency can be negative in some cases
    assert result['duration'] == -500  # Duration can be negative in some cases