import pytest
import torch
import numpy as np
from unittest.mock import Mock, patch
from curiosity_budget.skill_valuation import SkillValuation
from curiosity_budget.agent import CuriosityAgent
from curiosity_budget.models import BaseModel

class TestSkillValuation:
    @pytest.fixture
    def mock_agent(self):
        agent = Mock(spec=CuriosityAgent)
        agent.skill_selector = Mock()
        agent.skill_selector.skills = {'skill1': {}, 'skill2': {}}
        return agent

    @pytest.fixture
    def skill_valuation(self, mock_agent):
        return SkillValuation(mock_agent)

    def test_init_with_agent(self, mock_agent):
        sv = SkillValuation(mock_agent)
        assert sv.agent == mock_agent
        assert sv.values == {}

    def test_init_with_model(self, mock_agent):
        mock_model = Mock(spec=BaseModel)
        sv = SkillValuation(mock_agent, mock_model)
        assert sv.model == mock_model

    def test_evaluate_skills_success(self, skill_valuation):
        result = skill_valuation.evaluate_skills()
        assert isinstance(result, dict)
        assert len(result) == 2

    def test_evaluate_skills_with_no_skills(self, mock_agent, skill_valuation):
        mock_agent.skill_selector.skills = {}
        result = skill_valuation.evaluate_skills()
        assert result == {}

    def test_evaluate_skills_exception_handling(self, mock_agent, skill_valuation):
        mock_agent.skill_selector.side_effect = Exception("Test error")
        result = skill_valuation.evaluate_skills()
        assert result == {}

    def test_calculate_skill_value_default(self, skill_valuation):
        value = skill_valuation._calculate_skill_value("test_skill")
        assert value == 0.0

    def test_get_value_for_existing_skill(self, skill_valuation):
        skill_valuation.values = {'skill1': 0.5}
        result = skill_valuation.get_value('skill1')
        assert result == 0.5

    def test_get_value_for_nonexistent_skill(self, skill_valuation):
        result = skill_valuation.get_value('nonexistent')
        assert result == 0.0

    def test_get_value_all_skills(self, skill_valuation):
        skill_valuation.values = {'skill1': 0.3, 'skill2': 0.7}
        result = skill_valuation.get_value()
        assert result == {'skill1': 0.3, 'skill2': 0.7}

    def test_update_values(self, skill_valuation):
        new_values = {'skill1': 0.8, 'skill2': 0.2}
        skill_valuation.update_values(new_values)
        assert skill_valuation.values == new_values

    def test_update_values_partial(self, skill_valuation):
        initial_values = {'skill1': 0.5}
        skill_valuation.values = initial_values
        new_values = {'skill1': 0.8, 'skill3': 0.9}
        skill_valuation.update_values(new_values)
        expected = {'skill1': 0.8, 'skill3': 0.9}
        assert skill_valuation.values == expected

    def test_evaluate_skills_with_skill_selector_error(self, mock_agent, skill_valuation):
        mock_agent.skill_selector = None
        result = skill_valuation.evaluate_skills()
        assert result == {}

    def test_get_value_empty_values(self, skill_valuation):
        result = skill_valuation.get_value()
        assert result == {}

    @patch('curiosity_budget.skill_valuation.logging')
    def test_evaluate_skills_logs_error(self, mock_logging, skill_valuation):
        skill_valuation.agent.skill_selector.skills = {'skill1': {}, 'skill2': {}}
        skill_valuation._calculate_skill_value = Mock(side_effect=Exception("Test error"))
        skill_valuation.evaluate_skills()
        mock_logging.getLogger.return_value.error.assert_called()

    def test_skill_valuation_inheritance(self):
        assert issubclass(SkillValuation, object)

    def test_evaluate_skills_returns_dict(self, skill_valuation):
        result = skill_valuation.evaluate_skills()
        assert isinstance(result, dict)

    def test_update_values_empty_dict(self, skill_valuation):
        skill_valuation.update_values({})
        assert skill_valuation.values == {}

    def test_update_values_overwrites_existing(self, skill_valuation):
        skill_valuation.values = {'skill1': 0.5}
        skill_valuation.update_values({'skill1': 0.7})
        assert skill_valuation.values == {'skill1': 0.7}