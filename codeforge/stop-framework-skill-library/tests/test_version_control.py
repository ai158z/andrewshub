import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from stop_skill_library.models import Skill, SkillVersion
from stop_skill_library.version_control import VersionControl

class TestVersionControl:
    
    @pytest.fixture
    def skill_library(self):
        return Mock()
    
    @pytest.fixture
    def version_manager(self):
        return Mock()
    
    @pytest.fixture
    def version_control(self, skill_library, version_manager):
        vc = VersionControl(skill_library)
        vc.version_manager = version_manager
        return vc
    
    def test_commit_success(self, version_control, skill_library, version_manager):
        # Setup
        skill = Skill(id="test_skill", name="Test Skill", description="Test", code="print('hello')")
        skill_library.get_skill.return_value = skill
        version_manager.create_version.return_value = "version_123"
        
        # Test
        result = version_control.commit("test_skill", {"key": "value"}, "Test commit", "author")
        
        # Assert
        assert result == "version_123"
        skill_library.get_skill.assert_called_once_with("test_skill")
        version_manager.create_version.assert_called_once()
    
    def test_commit_skill_not_found(self, version_control, skill_library):
        # Setup
        skill_library.get_skill.return_value = None
        
        # Test and Assert
        with pytest.raises(ValueError, match="Skill with ID.*not found"):
            version_control.commit("nonexistent", {}, "Test commit", "author")
    
    def test_commit_version_manager_exception(self, version_control, skill_library, version_manager):
        # Setup
        skill_library.get_skill.return_value = Mock()
        version_manager.create_version.side_effect = Exception("DB error")
        
        # Test and Assert
        with pytest.raises(Exception, match="Commit failed"):
            version_control.commit("test_skill", {}, "Test commit", "author")
    
    def test_rollback_success(self, version_control, skill_library, version_manager):
        # Setup
        skill_library.get_skill.return_value = Mock()
        version_manager.get_version.return_value = {
            'content': {'name': 'Test Skill', 'description': 'Test', 'code': 'code'},
            'changes': {}
        }
        
        # Test
        result = version_control.rollback("test_skill", "version_123")
        
        # Assert
        assert result is True
        version_manager.get_version.assert_called_once_with("test_skill", "version_123")
    
    def test_rollback_version_not_found(self, version_control, version_manager):
        # Setup
        version_manager.get_version.return_value = None
        
        # Test and Assert
        with pytest.raises(ValueError, match="Version.*not found"):
            version_control.rollback("test_skill", "nonexistent_version")
    
    def test_rollback_skill_not_found(self, version_control, version_manager, version_control, skill_library):
        # Setup
        version_manager.get_version.return_value = {'content': {}}
        skill_library.get_skill.return_value = None
        
        # Test
        result = version_control.rollback("test_skill", "version_123")
        
        # Assert
        assert result is False
    
    def test_get_history_success(self, version_control, version_manager):
        # Setup
        version_manager.get_history.return_value = {
            "version1": {
                "message": "Test message",
                "author": "test_author",
                "timestamp": "2023-01-01T00:00:00"
            }
        }
        
        # Test
        result = version_control.get_history("test_skill")
        
        # Assert
        assert len(result) == 1
        assert result[0]["version_id"] == "version1"
        assert result[0]["message"] == "Test message"
    
    def test_get_history_empty(self, version_control, version_manager):
        # Setup
        version_manager.get_history.return_value = {}
        
        # Test
        result = version_control.get_history("test_skill")
        
        # Assert
        assert result == []
    
    def test_get_history_exception(self, version_control, version_manager):
        # Setup
        version_manager.get_history.side_effect = Exception("DB error")
        
        # Test and Assert
        with pytest.raises(ValueError, match="Failed to retrieve history"):
            version_control.get_history("test_skill")
    
    def test_get_version_found(self, version_control, version_manager):
        # Setup
        version_manager.get_version.return_value = {
            'content': {'name': 'Test Skill'},
            'changes': {},
            'message': 'Test message',
            'author': 'test_author',
            'timestamp': '2023-01-01T00:00:00'
        }
        
        # Test
        result = version_control.get_version("test_skill", "version_123")
        
        # Assert
        assert result is not None
        assert result.version_id == "version_123"
        assert result.skill_id == "test_skill"
    
    def test_get_version_not_found(self, version_control, version_manager):
        # Setup
        version_manager.get_version.return_value = None
        
        # Test
        result = version_control.get_version("test_skill", "nonexistent")
        
        # Assert
        assert result is None
    
    def test_get_version_exception(self, version_control, version_manager):
        # Setup
        version_manager.get_version.side_effect = Exception("DB error")
        
        # Test
        result = version_control.get_version("test_skill", "version_123")
        
        # Assert
        assert result is None
    
    def test_rollback_restores_skill(self, version_control, skill_library, version_manager):
        # Setup
        skill = Mock()
        skill_library.get_skill.return_value = skill
        version_manager.get_version.return_value = {
            'content': {'name': 'Restored Skill', 'description': 'Test', 'code': 'code'},
            'changes': {}
        }
        
        # Test
        result = version_control.rollback("test_skill", "version_123")
        
        # Assert
        assert result is True
        skill_library.add_skill.assert_called_once()
    
    def test_commit_with_skill_dict_conversion(self, version_control, skill_library, version_manager):
        # Setup
        skill_dict = {'name': 'Test Skill', 'description': 'Test', 'code': 'code'}
        skill = Mock()
        skill.dict.return_value = skill_dict
        skill_library.get_skill.return_value = skill
        version_manager.create_version.return_value = "version_123"
        
        # Test
        result = version_control.commit("test_skill", {"key": "value"}, "Test commit", "author")
        
        # Assert
        assert result == "version_123"
        version_manager.create_version.assert_called_once()
    
    def test_get_history_sorting(self, version_control, version_manager):
        # Setup
        version_manager.get_history.return_value = {
            "version1": {
                "message": "Old commit",
                "author": "author1",
                "timestamp": "2023-01-01T10:00:00"
            },
            "version2": {
                "message": "Newer commit",
                "author": "author2", 
                "timestamp": "2023-01-01T11:00:00"
            }
        }
        
        # Test
        result = version_control.get_history("test_skill")
        
        # Assert
        assert result[0]["message"] == "Newer commit"
        assert result[1]["message"] == "Old commit"
    
    def test_rollback_with_empty_skill_content(self, version_control, version_manager, skill_library):
        # Setup
        version_manager.get_version.return_value = {'content': {}, 'changes': {}}
        skill_library.get_skill.return_value = Mock()
        
        # Test
        result = version_control.rollback("test_skill", "version_123")
        
        # Assert
        assert result is True
    
    def test_commit_with_no_changes(self, version_control, skill_library, version_manager):
        # Setup
        skill_library.get_skill.return_value = Mock()
        version_manager.create_version.return_value = "version_123"
        
        # Test
        result = version_control.commit("test_skill", {}, "Test commit", "author")
        
        # Assert
        assert result == "version_123"
    
    def test_get_version_with_minimal_data(self, version_control, version_manager):
        # Setup
        version_manager.get_version.return_value = {
            'content': {},
            'changes': {},
            'message': '',
            'author': '',
            'timestamp': ''
        }
        
        # Test
        result = version_control.get_version("test_skill", "version_123")
        
        # Assert
        assert result is not None
        assert result.message == ""
        assert result.author == ""
    
    def test_rollback_failure_due_to_exception(self, version_control, version_manager):
        # Setup
        version_manager.get_version.side_effect = Exception("DB error")
        
        # Test
        result = version_control.rollback("test_skill", "version_123")
        
        # Assert
        assert result is False
    
    def test_commit_timestamp_generation(self, version_control, skill_library, version_manager):
        # Setup
        skill = Skill(id="test_skill", name="Test Skill", description="Test", code="print('hello')")
        skill_library.get_skill.return_value = skill
        version_manager.create_version.return_value = "version_123"
        
        # Test - checking that timestamp is generated
        with patch('stop_skill_library.version_control.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value.isoformat.return_value = "2023-01-01T00:00:00"
            result = version_control.commit("test_skill", {"key": "value"}, "Test commit", "author")
            
            # Assert
            assert result == "version_123"
            version_manager.create_version.assert_called_once()
    
    def test_get_history_with_malformed_data(self, version_control, version_manager):
        # Setup
        version_manager.get_history.return_value = {
            "version1": {
                # Missing required fields
            }
        }
        
        # Test
        result = version_control.get_history("test_skill")
        
        # Assert
        assert len(result) == 1
        # Should have empty values for missing fields
        assert result[0]["message"] == ""
        assert result[0]["author"] == ""
    
    def test_rollback_with_no_changes(self, version_control, version_manager, skill_library):
        # Setup
        version_manager.get_version.return_value = {'content': {}, 'changes': {}}
        skill_library.get_skill.return_value = Mock()
        
        # Test
        result = version_control.rollback("test_skill", "version_123")
        
        # Assert
        assert result is True
    
    def test_commit_with_none_skill(self, version_control, skill_library):
        # Setup
        skill_library.get_skill.return_value = None
        
        # Test and Assert
        with pytest.raises(ValueError):
            version_control.commit("nonexistent", {}, "Test", "author")