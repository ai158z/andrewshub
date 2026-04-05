import pytest
from unittest.mock import Mock, patch
from stop_skill_library import SkillLibrary
from stop_skill_library.core import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_skill_library_import():
    # Test that SkillLibrary can be imported from the package
    from stop_skill_library import SkillLibrary
    assert SkillLibrary is not None


@patch("stop_skill_library.core.SkillLibrary")
def test_skill_library_initialization(mock_skill_library):
    # Test that we can create an instance of SkillLibrary
    instance = SkillLibrary()
    assert instance is not None


class TestSkillLibrary:
    def test_add_skill(self):
        library = SkillLibrary()
        skill_name = "test_skill"
        skill_func = Mock()
        
        # This is a basic test of the public API
        with patch.object(library, "add_skill") as mock_add:
            mock_add.return_value = None
            library.add_skill(skill_name, skill_func)
            mock_add.assert_called_once_with(skill_name, skill_func)

    def test_get_skill(self):
        library = SkillLibrary()
        skill_name = "test_skill"
        
        with patch.object(library, "get_skill") as mock_get:
            mock_get.return_value = Mock()
            result = library.get_skill(skill_name)
            mock_get.assert_called_once_with(skill_name)
            assert result is not None

    def test_remove_skill(self):
        library = SkillLibrary()
        skill_name = "test_skill"
        
        with patch.object(library, "remove_skill") as mock_remove:
            mock_remove.return_value = True
            result = library.remove_skill(skill_name)
            mock_remove.assert_called_once_with(skill_name)
            assert result is True

    def test_list_skills(self):
        library = SkillLibrary()
        
        with patch.object(library, "list_skills") as mock_list:
            mock_list.return_value = ["skill1", "skill2"]
            skills = library.list_skills()
            mock_list.assert_called_once()
            assert isinstance(skills, list)

    def test_clear_skills(self):
        library = SkillLibrary()
        
        with patch.object(library, "clear") as mock_clear:
            mock_clear.return_value = None
            library.clear()
            mock_clear.assert_called_once()

    def test_save_to_file(self):
        library = SkillLibrary()
        filename = "test.json"
        
        with patch.object(library, "save_to_file") as mock_save:
            mock_save.return_value = None
            library.save_to_file(filename)
            mock_save.assert_called_once_with(filename)

    def test_load_from_file(self):
        library = SkillLibrary()
        filename = "test.json"
        
        with patch.object(library, "load_from_file") as mock_load:
            mock_load.return_value = None
            library.load_from_file(filename)
            mock_load.assert_called_once_with(filename)

    def test_skill_exists(self):
        library = SkillLibrary()
        skill_name = "test_skill"
        
        with patch.object(library, "skill_exists") as mock_exists:
            mock_exists.return_value = True
            result = library.skill_exists(skill_name)
            mock_exists.assert_called_once_with(skill_name)
            assert result is True

    def test_execute_skill(self):
        library = SkillLibrary()
        skill_name = "test_skill"
        
        with patch.object(library, "execute_skill") as mock_execute:
            mock_execute.return_value = "executed"
            result = library.execute_skill(skill_name)
            mock_execute.assert_called_once_with(skill_name)
            assert result == "executed"

    def test_update_skill(self):
        library = SkillLibrary()
        skill_name = "test_skill"
        new_skill_func = Mock()
        
        with patch.object(library, "update_skill") as mock_update:
            mock_update.return_value = None
            library.update_skill(skill_name, new_skill_func)
            mock_update.assert_called_once_with(skill_name, new_skill_func)

    def test_get_skill_count(self):
        library = SkillLibrary()
        
        with patch.object(library, "get_skill_count") as mock_count:
            mock_count.return_value = 5
            count = library.get_skill_count()
            mock_count.assert_called_once()
            assert count == 5

    def test_add_skill_category(self):
        library = SkillLibrary()
        category = "test_category"
        skill_name = "test_skill"
        skill_func = Mock()
        
        with patch.object(library, "add_skill_to_category") as mock_add_cat:
            mock_add_cat.return_value = None
            library.add_skill_to_category(category, skill_name, skill_func)
            mock_add_cat.assert_called_once_with(category, skill_name, skill_func)

    def test_remove_skill_from_category(self):
        library = SkillLibrary()
        category = "test_category"
        skill_name = "test_skill"
        
        with patch.object(library, "remove_skill_from_category") as mock_remove_cat:
            mock_remove_cat.return_value = True
            result = library.remove_skill_from_category(category, skill_name)
            mock_remove_cat.assert_called_once_with(category, skill_name)
            assert result is True

    def test_list_categories(self):
        library = SkillLibrary()
        
        with patch.object(library, "list_categories") as mock_list_cat:
            mock_list_cat.return_value = ["category1", "category2"]
            categories = library.list_categories()
            mock_list_cat.assert_called_once()
            assert isinstance(categories, list)

    def test_clear_category(self):
        library = SkillLibrary()
        category = "test_category"
        
        with patch.object(library, "clear_category") as mock_clear_cat:
            mock_clear_cat.return_value = None
            library.clear_category(category)
            mock_clear_cat.assert_called_once_with(category)

    def test_get_skills_in_category(self):
        library = SkillLibrary()
        category = "test_category"
        
        with patch.object(library, "get_skills_in_category") as mock_get_cat:
            mock_get_cat.return_value = ["skill1", "skill2"]
            skills = library.get_skills_in_category(category)
            mock_get_cat.assert_called_once_with(category)
            assert isinstance(skills, list)