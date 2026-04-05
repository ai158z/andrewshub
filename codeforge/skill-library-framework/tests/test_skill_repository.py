import pytest
from unittest.mock import Mock, patch, MagicMock
from src.skill_library.storage.skill_repository import SkillRepository
from src.skill_library.core.skill import Skill

class MockSkill:
    def __init__(self, id="test_id", name="Test Skill"):
        self.id = id
        self.name = name
        self.description = "Test description"
        self.domain = Mock()
        self.domain.get_category = Mock(return_value="test_domain")
        self.complexity = Mock()
        self.complexity.assess = Mock(return_value="medium")
        self.utility = Mock()
        self.utility.calculate = Mock(return_value=0.8)
        self.metadata = {"author": "test"}

class TestSkillRepository:
    @patch('sqlite3.connect')
    def test_init_db_creates_table(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        
        repo = SkillRepository()
        
        mock_connect.assert_called()
        mock_cursor.execute.assert_called()

    @patch('sqlite3.connect')
    @patch('src.skill_library.storage.skill_repository.VectorDB')
    def test_save_skill_success(self, mock_vector_db, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_vector_db_instance = Mock()
        mock_vector_db.return_value = mock_vector_db_instance
        
        skill = MockSkill()
        repo = SkillRepository()
        result = repo.save(skill)
        
        assert result == True
        mock_cursor.execute.assert_called()
        mock_vector_db_instance.add_skill.assert_called_with(skill)

    @patch('sqlite3.connect')
    @patch('src.skill_library.storage.skill_repository.VectorDB')
    def test_save_skill_failure(self, mock_vector_db, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.__enter__.side_effect = Exception("DB Error")
        
        skill = MockSkill()
        repo = SkillRepository()
        result = repo.save(skill)
        
        assert result == False

    @patch('sqlite3.connect')
    def test_get_skill_exists(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test_id', 'Test Skill', 'Test description', 'test_domain', 'medium', 0.8, '{"author": "test"}')
        
        repo = SkillRepository()
        result = repo.get('test_id')
        
        assert result is not None
        mock_cursor.execute.assert_called_with('SELECT * FROM skills WHERE id = ?', ('test_id',))

    @patch('sqlite3.connect')
    def test_get_skill_not_exists(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        repo = SkillRepository()
        result = repo.get('nonexistent')
        
        assert result is None

    @patch('sqlite3.connect')
    def test_get_skill_exception(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.side_effect = Exception("DB Error")
        
        repo = SkillRepository()
        result = repo.get('test_id')
        
        assert result is None

    @patch('sqlite3.connect')
    def test_delete_skill_success(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        
        repo = SkillRepository()
        result = repo.delete('test_id')
        
        assert result == True
        mock_cursor.execute.assert_called_with('DELETE FROM skills WHERE id = ?', ('test_id',))

    @patch('sqlite3.connect')
    def test_delete_skill_not_found(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        
        repo = SkillRepository()
        result = repo.delete('nonexistent')
        
        assert result == False

    @patch('sqlite3.connect')
    def test_delete_skill_exception(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.side_effect = Exception("DB Error")
        
        repo = SkillRepository()
        result = repo.delete('test_id')
        
        assert result == False

    @patch('os.environ.get')
    def test_db_path_from_env(self, mock_get):
        mock_get.return_value = "sqlite:///test.db"
        repo = SkillRepository()
        assert repo.db_path == "sqlite:///test.db"

    def test_db_path_default(self):
        with patch.dict('os.environ', clear=True):
            repo = SkillRepository()
            assert repo.db_path == "sqlite:///skills.db"

    @patch('sqlite3.connect')
    def test_init_db_exception(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("DB Error")
        
        with pytest.raises(Exception):
            SkillRepository()

    @patch('sqlite3.connect')
    @patch('src.skill_library.storage.skill_repository.VectorDB')
    def test_save_with_none_values(self, mock_vector_db, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_vector_db_instance = Mock()
        mock_vector_db.return_value = mock_vector_db_instance
        
        skill = MockSkill()
        skill.domain = None
        skill.complexity = None
        skill.utility = None
        skill.metadata = None
        
        repo = SkillRepository()
        result = repo.save(skill)
        
        assert result == True
        mock_cursor.execute.assert_called()

    @patch('sqlite3.connect')
    def test_get_with_no_metadata(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test_id', 'Test Skill', 'Test description', None, None, None, None)
        
        repo = SkillRepository()
        result = repo.get('test_id')
        
        assert result is not None

    @patch('sqlite3.connect')
    def test_get_with_empty_string_id(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        repo = SkillRepository()
        result = repo.get('')
        
        assert result is None

    @patch('sqlite3.connect')
    def test_delete_with_empty_id(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = Mock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        
        repo = SkillRepository()
        result = repo.delete('')
        
        assert result == False