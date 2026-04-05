import pytest
from unittest.mock import patch, Mock
from decimal import Decimal
from src.routes.api import validate_input

def test_validate_input_missing_fields():
    data = {'principal': 1000, 'apr': 5.0}
    assert validate_input(data) is False

def test_validate_input_invalid_principal_type():
    data = {'principal': None, 'apr': 5.0, 'duration': 30}
    assert validate_input(data) is False

def test_validate_input_invalid_principal_value():
    data = {'principal': 'invalid', 'apr': 5.0, 'duration': 30}
    assert validate_input(data) is False

def test_validate_input_valid_data():
    data = {'principal': 1000.0, 'apr': 5.0, 'duration': 30}
    assert validate_input(data) is True

def test_calculate_invalid_json():
    with patch('src.routes.api.request') as mock_request:
        mock_request.json = None
        with patch('src.routes.api.jsonify') as mock_jsonify:
            from src.routes.api import calculate
            calculate()
            mock_jsonify.assert_called_with({'error': 'Invalid input format'})

def test_calculate_missing_data():
    with patch('src.routes.api.request') as mock_request:
        mock_request.json = {}
        with patch('src.routes.api.jsonify') as mock_jsonify:
            from src.routes.api import calculate
            response = calculate()
            assert response[1] == 400

def test_calculate_invalid_values():
    with patch('src.routes.api.request') as mock_request:
        mock_request.json = {'principal': 'invalid', 'apr': 'invalid', 'duration': 'invalid'}
        with patch('src.routes.api.jsonify') as mock_jsonify:
            from src.routes.api import calculate
            response = calculate()
            assert response[1] == 400

def test_calculate_valid_input():
    with patch('src.routes.api.request') as mock_request:
        mock_request.json = {'principal': 1000, 'apr': 5.0, 'duration': 30}
        with patch('src.routes.api.calculate_rewards') as mock_calculate_rewards:
            mock_calculate_rewards.return_value = Decimal('150.0')
            with patch('src.routes.api.jsonify') as mock_jsonify:
                from src.routes.api import calculate
                calculate()
                mock_jsonify.assert_called_with({'rewards': Decimal('150.0')})

def test_calculate_success():
    with patch('src.routes.api.request') as mock_request:
        mock_request.json = {'principal': 1000, 'apr': 5.0, 'duration': 30}
        with patch('src.routes.api.calculate_rewards') as mock_calculate_rewards:
            mock_calculate_rewards.return_value = Decimal('150.0')
            from src.routes.api import calculate
            response = calculate()
            assert response[1] == 200

def test_calculate_rewards_exception():
    with patch('src.routes.api.request') as mock_request:
        mock_request.json = {'principal': 1000, 'apr': 5.0, 'duration': 30}
        with patch('src.routes.api.calculate_rewards') as mock_calculate_rewards:
            mock_calculate_rewards.side_effect = Exception('Calculation error')
            from src.routes.api import calculate
            response = calculate()
            assert response[1] == 500

def test_register_routes():
    mock_app = Mock()
    from src.routes.api import register_routes
    register_routes(mock_app)
    mock_app.register_blueprint.assert_called_once()

def test_calculate_missing_principal():
    data = {'apr': 5.0, 'duration': 30}
    assert validate_input(data) is False

def test_calculate_missing_apr():
    data = {'principal': 1000, 'duration': 30}
    assert validate_input(data) is False

def test_calculate_missing_duration():
    data = {'principal': 1000, 'apr': 5.0}
    assert validate_input(data) is False

def test_calculate_negative_duration():
    data = {'principal': 1000, 'apr': 5.0, 'duration': -30}
    assert validate_input(data) is True

def test_calculate_zero_values():
    data = {'principal': 0, 'apr': 0.0, 'duration': 0}
    assert validate_input(data) is True

def test_calculate_string_principal():
    data = {'principal': '1000', 'apr': 5.0, 'duration': 30}
    assert validate_input(data) is True

def test_calculate_invalid_principal_type_in_validation():
    data = {'principal': [], 'apr': 5.0, 'duration': 30}
    assert validate_input(data) is False

def test_calculate_float_principal():
    data = {'principal': 1000.50, 'apr': 5.0, 'duration': 30}
    result = validate_input(data)
    assert result is True

def test_calculate_no_json_data():
    with patch('src.routes.api.request') as mock_request:
        mock_request.json = None
        from src.routes.api import calculate
        response = calculate()
        assert response[1] == 400