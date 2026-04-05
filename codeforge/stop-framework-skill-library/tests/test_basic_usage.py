import pytest
from unittest.mock import Mock, patch
from examples import basic_usage
from examples.basic_usage import create_sample_skill, demonstrate_skill_lifecycle, main

def test_create_sample_skill():
    skill_dict = create_sample_skill()
    expected = {
        "id": "sample-skill-001",
        "name": "Data Processing",
        "description": "Process and analyze large datasets efficiently",
        "version": "1.0.0",
        "code": "def process_data(data): return data",
        "metadata": {
            "category": "data_science",
            "complexity": "intermediate",
            "last_updated": "2024-01-01"
        }
    }
    assert skill_dict == expected

@patch('examples.basic_usage.logger')
def test_demonstrate_skill_lifecycle_with_mocks(mock_logger):
    library = Mock()
    mock_skill = Mock()
    mock_skill.id = "sample-skill-001"
    mock_skill.name = "Data Processing"
    library.get_skill.return_value = mock_skill
    library.list_skills.return_value = [mock_skill]
    
    demonstrate_skill_lifecycle(library)
    
    library.add_skill.assert_called_once()
    library.get_skill.assert_called_with("sample-skill-001")
    library.list_skills.assert_called()
    library.improve_skill.assert_called()
    library.reflect.assert_called()

@patch('examples.basic_usage.logger')
@patch('examples.basic_usage.SkillLibrary')
def test_main_success(mock_skill_library_class, mock_logger):
    mock_library_instance = Mock()
    mock_skill_library_class.return_value = mock_library_instance
    
    main()
    
    mock_skill_library_class.assert_called_once()
    mock_logger.info.assert_called()
    mock_logger.error.assert_not_called()

@patch('examples.basic_usage.logger')
@patch('examples.basic_usage.SkillLibrary')
def test_main_exception_handling(mock_skill_library_class, mock_logger):
    mock_skill_library_class.side_effect = Exception("Library init failed")
    
    with pytest.raises(Exception):
        main()
    
    mock_logger.error.assert_called()