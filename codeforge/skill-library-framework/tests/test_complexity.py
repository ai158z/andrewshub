import pytest
from unittest.mock import Mock, create_autospec
from src.skill_library.core.complexity import Complexity
from src.skill_library.core.skill import Skill
from src.skill_library.core.domain import Domain
from src.skill_library.core.utility import Utility
from src.skill_library.models.predictive_scoring import PredictiveScoringModel
from src.skill_library.models.curiosity_budget import CuriosityBudget
from src.skill_library.models.task_scoring_model import TaskScoringModel

def test_complexity_initialization_with_valid_dependencies():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    assert complexity.domain == domain
    assert complexity.utility == utility
    assert complexity.predictive_model == predictive_model
    assert complexity.curiosity_budget == curiosity_budget
    assert complexity.task_scoring_model == task_scoring_model

def test_complexity_initialization_with_invalid_domain_type():
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    with pytest.raises(TypeError, match="domain must be an instance of Domain"):
        Complexity("invalid_domain", utility, predictive_model, curiosity_budget, task_scoring_model)

def test_complexity_initialization_with_invalid_utility_type():
    domain = create_autospec(Domain)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    with pytest.raises(TypeError, match="utility must be an instance of Utility"):
        Complexity(domain, "invalid_utility", predictive_model, curiosity_budget, task_scoring_model)

def test_complexity_initialization_with_invalid_predictive_model_type():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    with pytest.raises(TypeError, match="predictive_model must be an instance of PredictiveScoringModel"):
        Complexity(domain, utility, "invalid_model", curiosity_budget, task_scoring_model)

def test_complexity_initialization_with_invalid_curiosity_budget_type():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    with pytest.raises(TypeError, match="curiosity_budget must be an instance of CuriosityBudget"):
        Complexity(domain, utility, predictive_model, "invalid_budget", task_scoring_model)

def test_complexity_initialization_with_invalid_task_scoring_model_type():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    
    with pytest.raises(TypeError, match="task_scoring_model must be an instance of TaskScoringModel"):
        Complexity(domain, utility, predictive_model, curiosity_budget, "invalid_task_model")

def test_assess_with_valid_skill():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 0.8
    predictive_model.predict_relevance.return_value = 0.7
    curiosity_budget.allocate_budget.return_value = 0.6
    task_scoring_model.score_task.return_value = {"task1": 0.9}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill_123"
    
    result = complexity.assess(skill)
    
    assert result["skill_id"] == "test_skill_123"
    assert result["category"] == "test_category"
    assert result["utility_score"] == 0.8
    assert result["predictive_score"] == 0.7
    assert result["budget_allocation"] == 0.6
    assert result["task_scores"] == {"task1": 0.9}
    assert "complexity_score" in result

def test_assess_with_invalid_skill_type():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    with pytest.raises(TypeError, match="skill must be an instance of Skill"):
        complexity.assess("not_a_skill")

def test_assess_handles_exception_during_processing():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.side_effect = Exception("Domain error")
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    with pytest.raises(Exception, match="Domain error"):
        complexity.assess(skill)

def test_assess_calculates_correct_complexity_score():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "category_a"
    utility.calculate.return_value = 0.5
    predictive_model.predict_relevance.return_value = 0.3
    curiosity_budget.allocate_budget.return_value = 0.8
    task_scoring_model.score_task.return_value = {"task_score": 0.7}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    result = complexity.assess(skill)
    
    expected_score = 0.3 * 0.5 + 0.4 * 0.3 + 0.3 * 0.8
    assert result["complexity_score"] == expected_score

def test_assess_with_missing_dependencies():
    domain = Mock()
    utility = Mock()
    predictive_model = Mock()
    curiosity_budget = Mock()
    task_scoring_model = Mock()
    
    # Simulate missing methods
    utility.calculate.return_value = 0.5
    predictive_model.predict_relevance.return_value = 0.3
    curiosity_budget.allocate_budget.return_value = 0.8
    task_scoring_model.score_task.return_value = {"task_score": 0.7}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    # Should not raise, but work normally
    result = complexity.assess(skill)
    assert result is not None

def test_assess_with_zero_values():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 0.0
    predictive_model.predict_relevance.return_value = 0.0
    curiosity_budget.allocate_budget.return_value = 0.0
    task_scoring_model.score_task.return_value = {"task1": 0.0}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    result = complexity.assess(skill)
    
    assert result["utility_score"] == 0.0
    assert result["predictive_score"] == 0.0
    assert result["budget_allocation"] == 0.0
    assert result["complexity_score"] == 0.0

def test_assess_with_unity_values():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 1.0
    predictive_model.predict_relevance.return_value = 1.0
    curiosity_budget.allocate_budget.return_value = 1.0
    task_scoring_model.score_task.return_value = {"task1": 1.0}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    result = complexity.assess(skill)
    
    # With all 1.0 values, complexity should be 1.0
    # 0.3 * 1.0 + 0.4 * 1.0 + 0.3 * 1.0 = 1.0
    assert result["complexity_score"] == 1.0

def test_assess_with_mixed_values():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 0.2
    predictive_model.predict_relevance.return_value = 0.8
    curiosity_budget.allocate_budget.return_value = 0.5
    task_scoring_model.score_task.return_value = {"task1": 0.9}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    result = complexity.assess(skill)
    
    # 0.3 * 0.2 + 0.4 * 0.8 + 0.3 * 0.5 = 0.06 + 0.32 + 0.15 = 0.53
    assert result["complexity_score"] == 0.53

def test_assess_with_none_values():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 0.0
    predictive_model.predict_relevance.return_value = 0.0
    curiosity_budget.allocate_budget.return_value = 0.0
    task_scoring_model.score_task.return_value = {}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    result = complexity.assess(skill)
    
    assert result["complexity_score"] == 0.0

def test_assess_with_negative_values():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = -0.2
    predictive_model.predict_relevance.return_value = 0.8
    curiosity_budget.allocate_budget.return_value = 0.5
    task_scoring_model.score_task.return_value = {"task1": -0.3}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    # -0.3 * 0.2 + 0.4 * 0.8 + 0.3 * 0.5 = -0.06 + 0.32 + 0.15 = 0.41
    expected_score = 0.3 * -0.2 + 0.4 * 0.8 + 0.3 * 0.5
    result = complexity.assess(skill)
    assert abs(result["complexity_score"] - expected_score) < 0.001

def test_assess_with_very_high_values():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 10.0
    predictive_model.predict_relevance.return_value = 5.0
    curiosity_budget.allocate_budget.return_value = 2.0
    task_scoring_model.score_task.return_value = {"task1": 1.0}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    result = complexity.assess(skill)
    
    # 0.3 * 10.0 + 0.4 * 5.0 + 0.3 * 2.0 = 3.0 + 2.0 + 0.6 = 5.6
    assert result["complexity_score"] == 5.6

def test_assess_with_very_low_values():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 0.01
    predictive_model.predict_relevance.return_value = 0.02
    curiosity_budget.allocate_budget.return_value = 0.03
    task_scoring_model.score_task.return_value = {"task1": 0.01}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    
    result = complexity.assess(skill)
    
    # 0.3 * 0.01 + 0.4 * 0.02 + 0.3 * 0.03 = 0.003 + 0.008 + 0.009 = 0.02
    assert abs(result["complexity_score"] - 0.02) < 0.001