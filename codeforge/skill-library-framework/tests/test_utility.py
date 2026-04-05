import pytest
import numpy as np
from unittest.mock import Mock, create_autospec
from skill_library.core.skill import Skill
from skill_library.core.utility import Utility

def create_mock_skill():
    return create_autospec(Skill)

def create_utility_with_mocks():
    complexity_model = Mock()
    domain_model = Mock()
    predictive_model = Mock()
    task_scoring_model = Mock()
    curiosity_budget_model = Mock()
    vector_db = Mock()
    skill_repo = Mock()
    memory_system = Mock()
    pytorch_integration = Mock()
    
    utility = Utility(
        complexity_model=complexity_model,
        domain_model=domain_model,
        predictive_model=predictive_model,
        task_scoring_model=task_scoring_model,
        curiosity_budget_model=curiosity_budget_model,
        vector_db=vector_db,
        skill_repo=skill_repo,
        memory_system=memory_system,
        pytorch_integration=pytorch_integration
    )
    
    return utility

def test_utility_initialization():
    utility = create_utility_with_mocks()
    assert utility is not None
    assert hasattr(utility, 'complexity_model')
    assert hasattr(utility, 'domain_model')

def test_calculate_returns_float():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    result = utility.calculate(skill)
    assert isinstance(result, float)

def test_calculate_with_default_weights():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Mock all internal methods to return known values
    utility._get_performance_score = Mock(return_value=0.8)
    utility._get_complexity_score = Mock(return_value=0.7)
    utility._get_domain_relevance = Mock(return_value=0.9)
    utility._get_predictive_score = Mock(return_value=0.6)
    utility._get_curiosity_score = Mock(return_value=0.5)
    
    result = utility.calculate(skill)
    expected = 0.25*0.8 + 0.20*0.7 + 0.20*0.9 + 0.20*0.6 + 0.15*0.5
    assert round(result, 4) == round(expected, 4)

def test_calculate_with_zero_scores():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Mock all internal methods to return zero
    utility._get_performance_score = Mock(return_value=0.0)
    utility._get_complexity_score = Mock(return_value=0.0)
    utility._get_domain_relevance = Mock(return_value=0.0)
    utility._get_predictive_score = Mock(return_value=0.0)
    utility._get_curiosity_score = Mock(return_value=0.0)
    
    result = utility.calculate(skill)
    assert result == 0.0

def test_calculate_with_max_scores():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Mock all internal methods to return maximum values (1.0)
    utility._get_performance_score = Mock(return_value=1.0)
    utility._get_complexity_score = Mock(return_value=1.0)
    utility._get_domain_relevance = Mock(return_value=1.0)
    utility._get_predictive_score = Mock(return_value=1.0)
    utility._get_curiosity_score = Mock(return_value=1.0)
    
    result = utility.calculate(skill)
    assert result == 1.0

def test_calculate_performance_weight():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Test with only performance score contributing
    utility._get_performance_score = Mock(return_value=1.0)
    utility._get_complexity_score = Mock(return_value=0.0)
    utility._get_domain_relevance = Mock(return_value=0.0)
    utility._get_predictive_score = Mock(return_value=0.0)
    utility._get_curiosity_score = Mock(return_value=0.0)
    
    result = utility.calculate(skill)
    # With performance weight 0.25, should return 0.25
    assert result == 0.25

def test_calculate_complexity_weight():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Test with only complexity score contributing
    utility._get_performance_score = Mock(return_value=0.0)
    utility._get_complexity_score = Mock(return_value=1.0)
    utility._get_domain_relevance = Mock(return_value=0.0)
    utility._get_predictive_score = Mock(return_value=0.0)
    utility._get_curiosity_score = Mock(return_value=0.0)
    
    result = utility.calculate(skill)
    # With complexity weight 0.20, should return 0.20
    assert result == 0.20

def test_calculate_domain_weight():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Test with only domain relevance contributing
    utility._get_performance_score = Mock(return_value=0.0)
    utility._get_complexity_score = Mock(return_value=0.0)
    utility._get_domain_relevance = Mock(return_value=1.0)
    utility._get_predictive_score = Mock(return_value=0.0)
    utility._get_curiosity_score = Mock(return_value=0.0)
    
    result = utility.calculate(skill)
    # With domain weight 0.20, should return 0.20
    assert result == 0.20

def test_calculate_predictive_weight():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Test with only predictive score contributing
    utility._get_performance_score = Mock(return_value=0.0)
    utility._get_complexity_score = Mock(return_value=0.0)
    utility._get_domain_relevance = Mock(return_value=0.0)
    utility._get_predictive_score = Mock(return_value=1.0)
    utility._get_curiosity_score = Mock(return_value=0.0)
    
    result = utility.calculate(skill)
    # With predictive weight 0.20, should return 0.20
    assert result == 0.20

def test_calculate_curiosity_weight():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    # Test with only curiosity score contributing
    utility._get_performance_score = Mock(return_value=0.0)
    utility._get_complexity_score = Mock(return_value=0.0)
    utility._get_domain_relevance = Mock(return_value=0.0)
    utility._get_predictive_score = Mock(return_value=0.0)
    utility._get_curiosity_score = Mock(return_value=1.0)
    
    result = utility.calculate(skill)
    # With curiosity weight 0.15, should return 0.15
    assert result == 0.15

def test_calculate_all_scores_zero():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    utility._get_performance_score = Mock(return_value=0.0)
    utility._get_complexity_score = Mock(return_value=0.0)
    utility._get_domain_relevance = Mock(return_value=0.0)
    utility._get_predictive_score = Mock(return_value=0.0)
    utility._get_curiosity_score = Mock(return_value=0.0)
    
    result = utility.calculate(skill)
    assert result == 0.0

def test_calculate_all_scores_max():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    utility._get_performance_score = Mock(return_value=1.0)
    utility._get_complexity_score = Mock(return_value=1.0)
    utility._get_domain_relevance = Mock(return_value=1.0)
    utility._get_predictive_score = Mock(return_value=1.0)
    utility._get_curiosity_score = Mock(return_value=1.0)
    
    result = utility.calculate(skill)
    assert result == 1.0

def test_calculate_mixed_scores():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    utility._get_performance_score = Mock(return_value=0.5)
    utility._get_complexity_score = Mock(return_value=0.8)
    utility._get_domain_relevance = Mock(return_value=0.3)
    utility._get_predictive_score = Mock(return_value=0.9)
    utility._get_curiosity_score = Mock(return_value=0.7)
    
    result = utility.calculate(skill)
    expected = 0.25*0.5 + 0.20*0.8 + 0.20*0.3 + 0.20*0.9 + 0.15*0.7
    assert round(result, 4) == round(expected, 4)

def test_calculate_with_negative_scores():
    utility = create_utility_with_mocks()
    skill = create_mock_skill()
    
    utility._get_performance_score = Mock(return_value=-0.5)
    utility._get_complexity_score = Mock(return_value=0.0)
    utility._get_domain_relevance = Mock(return_value=0.0)
    utility._get_predictive_score = Mock(return_value=0.0)
    utility._get_curiosity_score = Mock(return_value=0.0)
    
    result = utility.calculate(skill)
    # Should handle negative values in calculation
    assert result == -0.125  # 0.25 * -0.5

def test_calculate_with_high_scores():
    utility = create_utility_with_mocks()
    
    # Test with scores above 1.0
    utility._get_performance_score = Mock(return_value=1.5)
    utility._get_complexity_score = Mock(return_value=1.0)
    utility._get_domain_relevance = Mock(return_value=1.0)
    utility._get_predictive_score = Mock(return_value=1.0)
    utility._get_curiosity_score = Mock(return_value=1.0)
    
    skill = create_mock_skill()
    result = utility.calculate(skill)
    # Result should be above 1.0 due to high performance score
    expected = 0.25*1.5 + 0.20*1.0 + 0.20*1.0 + 0.20*1.0 + 0.15*1.0
    assert result > 1.0
    assert round(result, 4) == round(expected, 4)