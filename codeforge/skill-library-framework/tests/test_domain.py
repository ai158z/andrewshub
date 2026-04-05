import pytest
from unittest.mock import Mock, patch
from src.skill_library.core.domain import Domain
from src.skill_library.core.skill import Skill

class TestDomain:
    """Test suite for Domain class."""
    
    def test_init_with_valid_inputs(self):
        """Test Domain initialization with valid inputs."""
        domain = Domain("Technology")
        assert domain.domain_name == "Technology"
        assert domain.categories == {}
    
    def test_init_with_categories(self):
        """Test Domain initialization with categories."""
        categories = {"programming": ["python", "java"], "design": ["ui", "ux"]}
        domain = Domain("Creative", categories=categories)
        assert domain.domain_name == "Creative"
        assert domain.categories == categories
    
    def test_init_invalid_domain_name(self):
        """Test Domain initialization with invalid domain name."""
        with pytest.raises(ValueError, match="Domain name must be a non-empty string"):
            Domain("")
    
    def test_init_invalid_categories_type(self):
        """Test Domain initialization with invalid categories type."""
        with pytest.raises(TypeError, match="Categories must be a dictionary"):
            Domain("Test", categories="invalid")
    
    def test_add_category_valid_inputs(self):
        """Test adding a category with valid inputs."""
        domain = Domain("Test")
        domain.add_category("programming", ["python", "java", "javascript"])
        assert "programming" in domain.categories
        assert domain.categories["programming"] == ["python", "java", "javascript"]
    
    def test_add_category_invalid_name(self):
        """Test adding category with invalid name."""
        domain = Domain("Test")
        with pytest.raises(ValueError, match="Category name must be a non-empty string"):
            domain.add_category("", ["keyword"])
    
    def test_add_category_invalid_keywords_type(self):
        """Test adding category with invalid keywords type."""
        domain = Domain("Test")
        with pytest.raises(TypeError, match="Keywords must be a list of strings"):
            domain.add_category("test", "invalid")
    
    def test_add_category_invalid_keyword_type(self):
        """Test adding category with invalid keyword type."""
        domain = Domain("Test")
        with pytest.raises(TypeError, match="All keywords must be strings"):
            domain.add_category("test", ["valid", 123, "invalid"])
    
    def test_remove_category_success(self):
        """Test successful category removal."""
        domain = Domain("Test")
        domain.add_category("test_category", ["keyword1", "keyword2"])
        result = domain.remove_category("test_category")
        assert result is True
        assert "test_category" not in domain.categories
    
    def test_remove_category_not_found(self):
        """Test removing non-existent category."""
        domain = Domain("Test")
        result = domain.remove_category("nonexistent")
        assert result is False
    
    def test_remove_category_invalid_name(self):
        """Test removing category with invalid name."""
        domain = Domain("Test")
        with pytest.raises(ValueError, match="Category name must be a non-empty string"):
            domain.remove_category("")
    
    def test_list_categories(self):
        """Test listing categories."""
        categories = {"cat1": ["k1"], "cat2": ["k2"]}
        domain = Domain("Test", categories=categories)
        result = domain.list_categories()
        assert set(result) == {"cat1", "cat2"}
    
    def test_get_category_keywords(self):
        """Test getting category keywords."""
        categories = {"programming": ["python", "java"]}
        domain = Domain("Test", categories=categories)
        result = domain.get_category_keywords("programming")
        assert result == ["python", "java"]
    
    def test_get_category_keywords_not_found(self):
        """Test getting keywords for non-existent category."""
        domain = Domain("Test")
        result = domain.get_category_keywords("nonexistent")
        assert result == []
    
    def test_get_category_keywords_invalid_name(self):
        """Test getting category keywords with invalid name."""
        domain = Domain("Test")
        with pytest.raises(ValueError, match="Category name must be a non-empty string"):
            domain.get_category_keywords("")
    
    def test_update_category_keywords_success(self):
        """Test successfully updating category keywords."""
        domain = Domain("Test")
        domain.add_category("programming", ["old"])
        domain.update_category_keywords("programming", ["python", "java", "javascript"])
        assert domain.categories["programming"] == ["python", "java", "javascript"]
    
    def test_update_category_keywords_not_found(self):
        """Test updating keywords for non-existent category."""
        domain = Domain("Test")
        with pytest.raises(KeyError):
            domain.update_category_keywords("nonexistent", ["keyword"])
    
    def test_update_category_keywords_invalid_name(self):
        """Test updating category keywords with invalid name."""
        domain = Domain("Test")
        with pytest.raises(ValueError, match="Category name must be a non-empty string"):
            domain.update_category_keywords("", ["keyword"])
    
    def test_update_category_keywords_invalid_type(self):
        """Test updating category keywords with invalid type."""
        domain = Domain("Test")
        domain.add_category("test", ["keyword"])
        with pytest.raises(TypeError, match="Keywords must be a list"):
            domain.update_category_keywords("test", "invalid")
    
    def test_get_category_exact_match(self):
        """Test exact category matching."""
        categories = {"programming": ["python", "java", "javascript"]}
        domain = Domain("Technology", categories=categories)
        skill = Skill(name="Python Programming", description="Learn Python programming")
        result = domain._find_exact_category_match(skill)
        assert result == "programming"
    
    def test_get_category_no_match(self):
        """Test category detection with no match."""
        domain = Domain("Test")
        skill = Skill(name="Unknown Skill", description="Some description")
        result = domain._find_exact_category_match(skill)
        assert result is None
    
    def test_get_category_invalid_skill(self):
        """Test category detection with invalid skill type."""
        domain = Domain("Test")
        with pytest.raises(TypeError, match="Input must be a Skill instance"):
            domain.get_category("invalid")
    
    def test_get_category_with_predictive_model(self):
        """Test category prediction with model."""
        domain = Domain("Test")
        skill = Skill(name="Python Programming", description="Learn Python")
        
        # Mock the predictive model and vector db
        with patch.object(domain, 'predictive_model', Mock()) as mock_model:
            with patch.object(domain, 'vector_db', Mock()) as mock_db:
                mock_db.find_similar_skills.return_value = [(Skill(name="Java", description="Java programming"), 0.8)]
                domain.predictive_model = mock_model
                domain.vector_db = mock_db
                domain.categories = {"programming": ["python", "java"]}
                result = domain._predict_category(skill)
                assert result == "programming"
    
    def test_fallback_categorization(self):
        """Test fallback categorization."""
        domain = Domain("Test")
        skill = Skill(name="Test Skill", description="Test description")
        result = domain._fallback_categorization(skill)
        assert result == "uncategorized"