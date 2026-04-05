import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.skill_library.storage.vector_db import VectorDB
from src.skill_library.core.skill import Skill

class TestVectorDB:
    """Test cases for VectorDB class."""

    @pytest.fixture
    def mock_skill_repo(self):
        """Create a mock skill repository."""
        return Mock()

    @pytest.fixture
    def sample_skills(self):
        """Create sample skills for testing."""
        return [
            Skill(id="1", name="Python Programming", description="Expert in Python development"),
            Skill(id="2", name="Java Development", description="Skilled in Java programming"),
            Skill(id="3", name="Web Design", description="Frontend web design expertise")
        ]

    @pytest.fixture
    def vector_db(self, mock_skill_repo, sample_skills):
        """Create a VectorDB instance with mocked repository."""
        # Setup mock to return sample skills
        mock_skill_repo.get_all_skills.return_value = sample_skills
        return VectorDB(mock_skill_repo)

    def test_init_with_skills(self, mock_skill_repo, sample_skills):
        """Test VectorDB initialization with existing skills."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        # Verify initialization completed
        assert len(vector_db.skill_ids) == len(sample_skills)
        assert mock_skill_repo.get_all_skills.called

    def test_init_without_skills(self, mock_skill_repo):
        """Test VectorDB initialization with no existing skills."""
        mock_skill_repo.get_all_skills.return_value = []
        vector_db = VectorDB(mock_skill_repo)
        
        assert len(vector_db.skill_ids) == 0
        assert vector_db.index.ntotal == 0

    def test_add_skill_success(self, mock_skill_repo, sample_skills):
        """Test successfully adding a skill to VectorDB."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        new_skill = Skill(id="4", name="Data Science", description="Machine learning expertise")
        vector_db.add_skill(new_skill)
        
        assert len(vector_db.skill_ids) == len(sample_skills) + 1
        assert "4" in vector_db.skill_ids

    def test_add_skill_without_description(self, mock_skill_repo):
        """Test adding a skill with no description."""
        mock_skill_repo.get_all_skills.return_value = []
        vector_db = VectorDB(mock_skill_repo)
        
        skill = Skill(id="1", name="Test Skill", description=None)
        vector_db.add_skill(skill)
        
        assert "1" in vector_db.skill_ids

    def test_find_similar_skills_success(self, mock_skill_repo, sample_skills):
        """Test finding similar skills returns correct results."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        # Mock the FAISS search to return predictable results
        with patch.object(vector_db.index, 'search') as mock_search:
            mock_search.return_value = (np.array([[0.9, 0.8, 0.7]]), np.array([[1, 0, 2]]))
            vector_db.skill_ids = ["1", "2", "3"]
            vector_db.skill_texts = ["skill1", "skill2", "skill3"]
            
            results = vector_db.find_similar_skills("1", k=2)
            assert len(results) == 2
            assert isinstance(results[0], tuple)
            assert len(results[0]) == 2

    def test_find_similar_skills_skill_not_found(self, mock_skill_repo, sample_skills):
        """Test finding similar skills for non-existent skill."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        results = vector_db.find_similar_skills("999", k=5)
        assert results == []

    def test_update_existing_skill(self, mock_skill_repo, sample_skills):
        """Test updating an existing skill in VectorDB."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        # Create updated skill
        updated_skill = Skill(id="1", name="Python Programming Updated", description="Advanced Python development")
        vector_db.update_skill(updated_skill)
        
        # Should have rebuilt index
        assert mock_skill_repo.get_all_skills.call_count >= 1

    def test_update_new_skill(self, mock_skill_repo):
        """Test updating a new skill adds it to VectorDB."""
        mock_skill_repo.get_all_skills.return_value = []
        vector_db = VectorDB(mock_skill_repo)
        
        new_skill = Skill(id="1", name="New Skill", description="New skill description")
        vector_db.update_skill(new_skill)
        
        assert "1" in vector_db.skill_ids

    def test_remove_skill_success(self, mock_skill_repo, sample_skills):
        """Test successfully removing a skill from VectorDB."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        # Initially has 3 skills
        initial_count = len(vector_db.skill_ids)
        vector_db.remove_skill("1")
        
        # Should have triggered reindex
        assert mock_skill_repo.get_all_skills.call_count >= 2

    def test_remove_nonexistent_skill(self, mock_skill_repo, sample_skills):
        """Test removing a skill that doesn't exist."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        # Try to remove non-existent skill
        vector_db.remove_skill("999")
        
        # Should still have same number of skills since no actual removal happened
        assert len(vector_db.skill_ids) == len(sample_skills)

    def test_build_index_empty_skills(self, mock_skill_repo):
        """Test building index with empty skills list."""
        mock_skill_repo.get_all_skills.return_value = []
        vector_db = VectorDB(mock_skill_repo)
        
        # _build_index should handle empty list gracefully
        vector_db._build_index([])  # Should not raise exception

    def test_add_skill_with_exception(self, mock_skill_repo):
        """Test add_skill handles vectorization exceptions."""
        mock_skill_repo.get_all_skills.return_value = []
        vector_db = VectorDB(mock_skill_repo)
        
        # Mock vectorizer to raise exception
        with patch.object(vector_db.vectorizer, 'transform', side_effect=Exception("Vectorization failed")):
            with pytest.raises(Exception):
                skill = Skill(id="1", name="Test", description="Test skill")
                vector_db.add_skill(skill)

    def test_find_similar_skills_with_fewer_results(self, mock_skill_repo):
        """Test find_similar_skills when requesting more results than available."""
        mock_skill_repo.get_all_skills.return_value = [
            Skill(id="1", name="Skill 1", description="First skill")
        ]
        vector_db = VectorDB(mock_skill_repo)
        vector_db.skill_ids = ["1"]
        vector_db.skill_texts = ["skill 1"]
        
        # Mock FAISS search to return only one result
        with patch.object(vector_db.index, 'search') as mock_search:
            mock_search.return_value = (np.array([[0.9]]), np.array([[0]]))
            
            results = vector_db.find_similar_skills("1", k=5)
            # Should return empty list since we're searching for self
            assert results == []

    def test_initialize_index_exception(self, mock_skill_repo):
        """Test VectorDB initialization handles repository exceptions."""
        mock_skill_repo.get_all_skills.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            VectorDB(mock_skill_repo)

    def test_get_vector_at_index_out_of_bounds(self, mock_skill_repo):
        """Test _get_vector_at_index with invalid index."""
        mock_skill_repo.get_all_skills.return_value = []
        vector_db = VectorDB(mock_skill_repo)
        
        # Test with out of bounds index
        vector = vector_db._get_vector_at_index(999)
        assert vector is None

    def test_get_vector_at_index_exception(self, mock_skill_repo):
        """Test _get_vector_at_index handles vectorizer exceptions."""
        mock_skill_repo.get_all_skills.return_value = []
        vector_db = VectorDB(mock_skill_repo)
        
        with patch.object(vector_db.vectorizer, 'transform', side_effect=Exception("Transform error")):
            vector = vector_db._get_vector_at_index(0)
            assert vector is None

    def test_find_similar_skills_index_error(self, mock_skill_repo, sample_skills):
        """Test find_similar_skills when index operation fails."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        vector_db.skill_ids = ["1", "2"]
        
        # Mock index search to fail
        with patch.object(vector_db.index, 'search', side_effect=Exception("Search failed")):
            results = vector_db.find_similar_skills("1", 5)
            assert results == []

    def test_add_skill_index_update(self, mock_skill_repo, sample_skills):
        """Test that add_skill properly updates the index."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        initial_index_size = vector_db.index.ntotal
        new_skill = Skill(id="new", name="New Skill", description="A new skill")
        vector_db.add_skill(new_skill)
        
        # Index should have grown by 1
        assert vector_db.index.ntotal == initial_index_size + 1

    def test_update_skill_rebuilds_index(self, mock_skill_repo, sample_skills):
        """Test that update_skill causes index rebuild."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        # Update should trigger a rebuild
        updated_skill = Skill(id="1", name="Updated Python", description="Updated Python skill")
        original_call_count = mock_skill_repo.get_all_skills.call_count
        vector_db.update_skill(updated_skill)
        
        # Should have called get_all_skills again for rebuild
        assert mock_skill_repo.get_all_skills.call_count > original_call_count

    def test_remove_skill_triggers_rebuild(self, mock_skill_repo, sample_skills):
        """Test that remove_skill causes index rebuild."""
        mock_skill_repo.get_all_skills.return_value = sample_skills
        vector_db = VectorDB(mock_skill_repo)
        
        original_count = len(sample_skills)
        vector_db.remove_skill("1")
        
        # Should have called get_all_skills to rebuild
        assert mock_skill_repo.get_all_skills.call_count >= 2