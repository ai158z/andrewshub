import pytest
from unittest.mock import Mock, patch
from src.curiosity_budget import CuriosityBudgetManager, allocate_budget, adjust_budget, get_budget_status

@pytest.fixture
def mock_dependencies():
    return {
        'skill_catalog': Mock(),
        'curiosity_allocator': Mock(),
        'task_scorer': Mock(),
        'skill_manager': Mock()
    }

@pytest.fixture
def budget_manager(mock_dependencies):
    return CuriosityBudgetManager(**mock_dependencies)

def test_init_budget_manager(budget_manager):
    # Test that the manager initializes without error
    assert budget_manager is not None

def test_get_budget_status_returns_dict(budget_manager):
    mock_status = {
        'current_curiosity': 5.0,
        'allocated_budget': 10.0,
        'remaining_budget': 5.0,
        'threshold': 2.0
    }
    
    with patch('src.curiosity_budget.get_budget_status') as mock_get:
        mock_get.return_value = mock_status
        result = budget_manager.get_budget_status('test_skill')
        assert isinstance(result, dict)
        assert 'current_curosity' in result
        assert 'allocated_budget' in result
        assert 'remaining_budget' in result
        assert 'threshold' in result

def test_allocate_budget_calls_allocator(budget_manager):
    with patch.object(budget_manager, 'curiosity_allocator') as mock_allocator:
        budget_manager.allocate_budget('test_skill', 5.0)
        mock_allocator.allocate.assert_called_once()

def test_adjust_budget_calls_allocator(budget_manager):
    with patch.object(budget_manager, 'curiosity_allocator') as mock_allocator:
        budget_manager.adjust_budget('test_skill', 2.0)
        mock_allocator.adjust.assert_called_once()

def test_allocate_budget_module_function():
    with patch('src.curiosity_budget.allocate_budget') as mock_allocate:
        allocate_budget('test_skill', 10.0)
        mock_allocate.assert_called_once_with('test_skill', 10.0)

def test_adjust_budget_module_function():
    with patch('src.curiosity_budget.adjust_budget') as mock_adjust:
        adjust_budget('test_skill', 3.0)
        mock_adjust.assert_called_once_with('test_skill', 3.0)

def test_get_budget_status_module_function():
    mock_return = {
        'skill_id': 'test_skill',
        'current_curiosity': 5.0,
        'allocated_budget': 10.0,
        'remaining_budget': 5.0,
        'threshold': 2.0
    }
    
    with patch('src.curiosity_budget.get_budget_status') as mock_get:
        mock_get.return_value = mock_return
        result = get_budget_status('test_skill')
        assert result == mock_return

def test_get_budget_status_default_values():
    with patch('src.curiosity_budget.get_budget_status') as mock_get_status:
        mock_get_status.return_value = {
            'current_curiosity': 0.0,
            'allocated_budget': 0.0,
            'remaining_budget': 0.0,
            'threshold': 0.0
        }
        result = get_budget_status('test')
        assert result['current_curiosity'] == 0.0
        assert result['allocated_budget'] == 0.0
        assert result['remaining_budget'] == 0.0
        assert result['threshold'] == 0.0

def test_allocate_budget_zero_amount():
    with patch('src.curiosity_budget.allocate_budget') as mock_allocate:
        allocate_budget('test_skill', 0.0)
        mock_allocate.assert_called_once_with('test_skill', 0.0)

def test_adjust_budget_zero_delta():
    with patch('src.curiosity_budget.adjust_budget') as mock_adjust:
        adjust_budget('test_skill', 0.0)
        mock_adjust.assert_called_once_with('test_skill', 0.0)

def test_get_budget_status_empty_skill_id():
    with patch('src.curiosity_budget.get_budget_status') as mock_get_status:
        mock_get_status.return_value = {}
        result = get_budget_status('')
        assert isinstance(result, dict)

def test_allocate_budget_negative_amount():
    with patch('src.curiosity_budget.allocate_budget') as mock_allocate:
        allocate_budget('test_skill', -5.0)
        mock_allocate.assert_called_once_with('test_skill', -5.0)

def test_adjust_budget_negative_delta():
    with patch('src.curiosity_budget.adjust_budget') as mock_adjust:
        adjust_budget('test_skill', -2.0)
        mock_adjust.assert_called_once_with('test_skill', -2.0)

def test_get_budget_status_invalid_skill_id():
    with patch('src.curiosity_budget.get_budget_status') as mock_get:
        mock_get.return_value = {
            'skill_id': 'invalid',
            'current_curiosity': -1.0,
            'allocated_budget': -1.0,
            'remaining_budget': -1.0,
            'threshold': -1.0
        }
        result = get_budget_status('invalid')
        assert result['current_curiosity'] == -1.0

def test_allocate_budget_large_amount():
    with patch('src.curiosity_budget.allocate_budget') as mock_allocate:
        allocate_budget('test_skill', 1000.0)
        mock_allocate.assert_called_once_with('test_skill', 1000.0)

def test_adjust_budget_large_delta():
    with patch('src.curiosity_budget.adjust_budget') as mock_adjust:
        adjust_budget('test_skill', 100.0)
        mock_adjust.assert_called_once_with('test_skill', 100.0)

def test_get_budget_status_special_chars():
    with patch('src.curiosity_budget.get_budget_status') as mock_get_status:
        mock_get_status.return_value = {
            'current_curiosity': 1.5,
            'allocated_budget': 2.5,
            'remaining_budget': 1.0,
            'threshold': 0.5
        }
        result = get_budget_status('special@#$%')
        assert result['current_curiosity'] == 1.5

def test_allocate_budget_type_validation():
    with patch('src.curiosity_budget.allocate_budget') as mock_allocate:
        with pytest.raises(TypeError):
            allocate_budget(123, 'invalid')

def test_adjust_budget_type_validation():
    with patch('src.curiosity_budget.adjust_budget') as mock_adjust:
        with pytest.raises(TypeError):
            adjust_budget(123, 'invalid')

def test_get_budget_status_type_validation():
    with patch('src.curiosity_budget.get_budget_status') as mock_get_status:
        mock_get_status.return_value = {}
        with pytest.raises(KeyError):
            result = get_budget_status('test')
            result['invalid_key']