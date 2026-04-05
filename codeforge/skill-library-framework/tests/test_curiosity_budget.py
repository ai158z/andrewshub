import pytest
from unittest.mock import Mock, create_autospec
from src.skill_library.models.curiosity_budget import CuriosityBudget, BudgetAllocation
from src.skill_library.core.skill import Skill

class TestCuriosityBudget:
    @pytest.fixture
    def mock_dependencies(self):
        return {
            'skill_repository': create_autospec(CuriosityBudget().skill_repository),
            'vector_db': create_autospec(CuriosityBudget().vector_db),
            'predictive_model': create_autospec(CuriosityBudget().predictive_model),
            'task_scoring_model': create_autospec(CuriosityBudget().task_scoring_model)
        }

    @pytest.fixture
    def sample_skills(self):
        skill1 = Skill(id="skill_1", name="Python")
        skill2 = Skill(id="skill_2", name="JavaScript")
        return [skill1, skill2]

    def test_init_with_defaults(self):
        # Arrange & Act
        budget = CuriosityBudget()
        
        # Assert
        assert budget.total_budget == 100.0
        assert budget.current_budget == 100.0
        assert budget.allocation_strategy == "proportional"

    def test_init_with_custom_values(self):
        # Arrange & Act
        budget = CuriosityBudget(total_budget=200.0, allocation_strategy="custom")
        
        # Assert
        assert budget.total_budget == 200.0
        assert budget.allocation_strategy == "custom"

    def test_allocate_budget_empty_skills(self, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        
        # Act
        allocations, remaining = budget.allocate_budget([])
        
        # Assert
        assert allocations == []
        assert remaining == 100.0

    def test_allocate_budget_success(self, sample_skills, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        budget._evaluate_skills = Mock(return_value=[
            {
                'skill_id': 'skill_1',
                'domain_score': 0.8,
                'complexity_score': 0.7,
                'utility_score': 0.6,
                'predictive_score': 0.9,
                'combined_score': 0.75
            },
            {
                'skill_id': 'skill_2',
                'domain_score': 0.6,
                'complexity_score': 0.5,
                'utility_score': 0.4,
                'predictive_score': 0.8,
                'combined_score': 0.575
            }
        ])
        budget._calculate_allocations = Mock(return_value=[
            BudgetAllocation("skill_1", 60.0, "test", {}),
            BudgetAllocation("skill_2", 40.0, "test", {})
        ])
        
        # Act
        allocations, remaining = budget.allocate_budget(sample_skills)
        
        # Assert
        assert len(allocations) == 2
        assert remaining == 0.0

    def test_allocate_budget_with_exception(self, sample_skills, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        budget._evaluate_skills = Mock(side_effect=Exception("Test exception"))
        
        # Act & Assert
        with pytest.raises(Exception):
            budget.allocate_budget(sample_skills)

    def test_evaluate_skills_success(self, sample_skills, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        budget.domain.get_category = Mock(return_value={'relevance': 0.8})
        budget.complexity.assess = Mock(return_value=0.7)
        budget.utility.calculate = Mock(return_value=0.6)
        budget.predictive_model.predict_relevance = Mock(return_value=0.9)
        
        # Act
        scores = budget._evaluate_skills(sample_skills)
        
        # Assert
        assert len(scores) == 2
        assert all(score['combined_score'] > 0 for score in scores)

    def test_evaluate_skills_exception_handling(self, sample_skills, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        budget.domain.get_category = Mock(side_effect=Exception("Domain error"))
        budget.complexity.assess = Mock(side_effect=Exception("Complexity error"))
        budget.utility.calculate = Mock(side_effect=Exception("Utility error"))
        budget.predictive_model.predict_relevance = Mock(side_effect=Exception("Predictive error"))
        
        # Act
        scores = budget._evaluate_skills(sample_skills)
        
        # Assert
        assert len(scores) == 2
        # Should use default scores when exceptions occur
        assert all(score['combined_score'] == 0.1 for score in scores)

    def test_calculate_allocations_empty_scores(self, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        
        # Act
        allocations = budget._calculate_allocations([], [])
        
        # Assert
        assert allocations == []

    def test_calculate_allocations_zero_total_score(self, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        scores = [
            {'skill_id': 'skill_1', 'combined_score': 0.0},
            {'skill_id': 'skill_2', 'combined_score': 0.0}
        ]
        
        # Act
        allocations = budget._calculate_allocations([], scores)
        
        # Assert
        assert allocations == []

    def test_get_budget_status(self, sample_skills, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(total_budget=150.0, **mock_dependencies)
        budget.allocations = [
            BudgetAllocation("skill_1", 60.0, "test", {}),
            BudgetAllocation("skill_2", 40.0, "test", {})
        ]
        budget.current_budget = 50.0
        
        # Act
        status = budget.get_budget_status()
        
        # Assert
        assert status['total_budget'] == 150.0
        assert status['current_budget'] == 50.0
        assert status['allocated_budget'] == 100.0
        assert len(status['allocations']) == 2

    def test_consume_budget_success(self, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(total_budget=100.0, **mock_dependencies)
        
        # Act
        result = budget.consume_budget(30.0)
        
        # Assert
        assert result is True
        assert budget.current_budget == 70.0

    def test_consume_budget_insufficient_funds(self, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(total_budget=50.0, **mock_dependencies)
        
        # Act
        result = budget.consume_budget(100.0)
        
        # Assert
        assert result is False
        assert budget.current_budget == 50.0

    def test_reset_budget(self, mock_dependencies):
        # Arrange
        budget = CuriosityBudget(**mock_dependencies)
        budget.current_budget = 50.0
        budget.allocations = [BudgetAllocation("test", 10.0, "test", {})]
        
        # Act
        budget.reset_budget()
        
        # Assert
        assert budget.current_budget == budget.total_budget
        assert budget.allocations == []