import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.scaffolding.templates.library import generate_library_template

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_success(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    result = generate_library_template("testlib", "/tmp/test")
    
    assert result is True
    mock_generate_structure.assert_called_once()
    mock_get_config.assert_called_once()
    mock_save_config.assert_called_once()

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_generation_failure(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = False
    mock_get_config.return_value = {}
    
    result = generate_library_template("testlib", "/tmp/test")
    
    assert result is False
    mock_generate_structure.assert_called_once()
    mock_get_config.assert_called_once()
    mock_save_config.assert_not_called()

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_exception_handling(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.side_effect = Exception("Generation failed")
    mock_get_config.return_value = {}
    
    result = generate_library_template("testlib", "/tmp/test")
    
    assert result is False

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_with_various_names(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    # Test with different project names
    test_names = ["simple", "with-dash", "with_underscore", "with123", "UPPERCASE"]
    
    for name in test_names:
        mock_generate_structure.reset_mock()
        mock_get_config.reset_mock()
        mock_save_config.reset_mock()
        
        result = generate_library_template(name, "/tmp/test")
        
        assert result is True
        mock_generate_structure.assert_called_once()
        mock_get_config.assert_called_once()
        mock_save_config.assert_called_once()

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_empty_project_name(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    result = generate_library_template("", "/tmp/test")
    
    assert result is True
    mock_generate_structure.assert_called_once()
    # Verify that the structure still gets generated even with empty name
    # (the system should handle this gracefully)

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_config_saved(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    config_dict = {}
    mock_get_config.return_value = config_dict
    
    generate_library_template("testlib", "/tmp/test")
    
    # Check that config is properly updated
    assert config_dict.get('project_type') == 'library'
    assert config_dict.get('project_name') == 'testlib'

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_structure_content(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    generate_library_template("testlib", "/tmp/test")
    
    # Verify the structure was called with correct parameters
    mock_generate_structure.assert_called_once()
    call_args = mock_generate_structure.call_args[0]
    project_structure = call_args[0]
    
    # Verify key elements of the structure
    assert "testlib" in project_structure
    assert "README.md" in project_structure["testlib"]
    assert "setup.py" in project_structure["testlib"]
    assert "src" in project_structure["testlib"]

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_fails_when_structure_fails(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = False
    mock_get_config.return_value = {}
    
    result = generate_library_template("testlib", "/tmp/test")
    
    assert result is False
    mock_get_config.assert_called_once()
    mock_save_config.assert_not_called()

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_no_side_effects_on_exception(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.side_effect = Exception("Intentional test error")
    mock_get_config.return_value = {}
    
    result = generate_library_template("testlib", "/tmp/test")
    
    assert result is False
    mock_save_config.assert_not_called()

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_with_special_characters_in_name(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    special_names = ["project-name", "project.name", "project_name", "project123"]
    
    for name in special_names:
        mock_generate_structure.reset_mock()
        mock_get_config.reset_mock()
        mock_save_config.reset_mock()
        
        result = generate_library_template(name, "/tmp/test")
        
        assert result is True
        mock_generate_structure.assert_called_once()

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_config_is_updated(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    config_dict = {}
    mock_get_config.return_value = config_dict
    
    generate_library_template("testlib", "/tmp/test")
    
    assert config_dict['project_type'] == 'library'
    assert config_dict['project_name'] == 'testlib'

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_empty_name_still_works(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    result = generate_library_template("", "/tmp/test")
    
    assert result is True

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_structure_with_long_name(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    # Test with a long project name
    long_name = "a" * 100
    result = generate_library_template(long_name, "/tmp/test")
    
    assert result is True

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_structure_check(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    mock_get_config.return_value = {}
    
    generate_library_template("testlib", "/tmp/test")
    
    # Check that the structure contains expected files
    call_args = mock_generate_structure.call_args[0][0]
    structure = call_args["testlib"]
    assert "README.md" in structure
    assert "setup.py" in structure
    assert "src" in structure
    assert "tests" in structure

@patch('src.scaffolding.templates.library.generate_project_structure')
@patch('src.scaffolding.templates.library.get_project_config')
@patch('src.scaffolding.templates.library.save_config')
def test_generate_library_template_config_persistence(mock_save_config, mock_get_config, mock_generate_structure):
    mock_generate_structure.return_value = True
    config_dict = {}
    mock_get_config.return_value = config_dict
    
    generate_library_template("testlib", "/tmp/test")
    
    # Verify config was updated and saved
    assert mock_get_config.called
    assert mock_save_config.called
    saved_config = mock_save_config.call_args[0][0]
    assert saved_config['project_type'] == 'library'
    assert saved_config['project_name'] == 'testlib'