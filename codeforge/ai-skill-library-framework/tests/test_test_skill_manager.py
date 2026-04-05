import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.skill_manager import SkillManager
from src.models.skill import Skill


class TestSkillManager:
    """Test suite for SkillManager class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        self.skill_manager = SkillManager()
        self.mock_skill = Mock(spec=Skill)
        self.mock_skill.name = "test_skill"
        self.mock_skill.id = "test_id"
        self.mock_skill.execute = Mock(return_value={"result": "success"})
        yield
        self.skill_manager = None

    def test_skill_registration_success(self):
        """Test successful skill registration."""
        self.skill_manager.register_skill(self.mock_skill)
        assert self.mock_skill.id in self.skill_manager.skills

    def test_skill_registration_duplicate(self):
        """Test duplicate skill registration raises error."""
        self.skill_manager.register_skill(self.mock_skill)
        
        with pytest.raises(ValueError, match="Skill with this ID already exists"):
            self.skill_manager.register_skill(self.mock_skill)

    def test_skill_registration_none(self):
        """Test registering None skill raises error."""
        with pytest.raises(TypeError):
            self.skill_manager.register_skill(None)

    def test_skill_registration_invalid_object(self):
        """Test registering invalid skill object."""
        invalid_skill = "not a skill"
        with pytest.raises(AttributeError):
            self.skill_manager.register_skill(invalid_skill)

    def test_skill_registration_empty_id(self):
        """Test skill with empty ID raises error."""
        invalid_skill = Mock(spec=Skill)
        invalid_skill.id = ""
        
        with pytest.raises(ValueError, match="Skill ID cannot be empty"):
            self.skill_manager.register_skill(invalid_skill)

    def test_skill_execution_success(self):
        """Test successful skill execution."""
        self.skill_manager.register_skill(self.mock_skill)
        result = self.skill_manager.execute_skill(self.mock_skill.id)
        assert result == {"result": "success"}

    def test_skill_execution_invalid_id(self):
        """Test skill execution with invalid ID."""
        with pytest.raises(KeyError):
            self.skill_manager.execute_skill("invalid_id")

    def test_skill_execution_unregistered(self):
        """Test executing unregistered skill."""
        with pytest.raises(KeyError):
            self.skill_manager.execute_skill("unregistered_id")

    def test_skill_execution_with_parameters(self):
        """Test skill execution with parameters."""
        self.skill_manager.register_skill(self.mock_skill)
        params = {"param1": "value1", "param2": "value2"}
        self.skill_manager.execute_skill(self.mock_skill.id, **params)
        self.mock_skill.execute.assert_called_with(**params)

    def test_remove_skill_success(self):
        """Test successful skill removal."""
        self.skill_manager.register_skill(self.mock_skill)
        self.skill_manager.remove_skill(self.mock_skill.id)
        assert self.mock_skill.id not in self.skill_manager.skills

    def test_remove_skill_nonexistent(self):
        """Test removing nonexistent skill."""
        with pytest.raises(KeyError):
            self.skill_manager.remove_skill("nonexistent")

    def test_update_skill_success(self):
        """Test skill update functionality."""
        self.skill_manager.register_skill(self.mock_skill)
        update_data = {"new_param": "value"}
        self.skill_manager.update_skill(self.mock_skill.id, update_data)
        self.mock_skill.update.assert_called_once_with(update_data)

    def test_update_skill_nonexistent(self):
        """Test updating nonexistent skill."""
        with pytest.raises(KeyError):
            self.skill_manager.update_skill("nonexistent", {})

    @patch('src.skill_manager.Skill')
    def test_execute_skill_mocked(self, mock_skill_class):
        """Test skill execution with mocked Skill class."""
        mock_skill_instance = Mock()
        mock_skill_instance.id = "mocked_skill"
        mock_skill_instance.execute.return_value = {"mocked": "result"}
        mock_skill_class.return_value = mock_skill_instance
        
        self.skill_manager.register_skill(mock_skill_instance)
        result = self.skill_manager.execute_skill("mocked_skill")
        
        assert result == {"mocked": "result"}
        mock_skill_instance.execute.assert_called_once()

    def test_update_policy_effect(self):
        """Test that policy updates affect skill selection."""
        self.skill_manager.register_skill(self.mock_skill)
        
        # Mock the dependencies
        mock_allocator = Mock()
        mock_scorer = Mock()
        
        # Simulate policy update
        with patch('src.curiosity_allocator.CuriosityAllocator') as mock_alloc_cls, \
             patch('src.task_scorer.TaskScorer') as mock_scorer_cls:
            
            mock_alloc = Mock()
            mock_alloc_cls.return_value = mock_alloc
            mock_scorer_cls.return_value = mock_scorer
            
            # Update policy
            self.skill_manager.update_skill(self.mock_skill.id, {"learning_rate": 0.1})
            
            # Verify policy was considered
            mock_alloc.update_policy.assert_called()