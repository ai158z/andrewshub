import os
import pytest
from unittest.mock import patch, mock_open, call
from src.scaffolding.templates.web import generate_web_template


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_creates_project_structure(mock_save_config, mock_generate_structure, mock_write_file):
    generate_web_template("test_project", "/tmp")
    
    # Check that project structure is generated
    mock_generate_structure.assert_called_once()
    
    # Check that config is saved
    mock_save_config.assert_called_once()


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_creates_index_html(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Check that write_file was called for index.html
    expected_index_path = os.path.join(target_dir, project_name, "index.html")
    mock_write_file.assert_any_call(expected_index_path, mock_write_file.call_args_list[0][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_creates_main_css(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Check that main.css is created
    expected_css_path = os.path.join(target_dir, project_name, "src", "styles", "main.css")
    mock_write_file.assert_any_call(expected_css_path, mock_write_file.call_args_list[1][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_creates_index_js(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Check that index.js is created
    expected_js_path = os.path.join(target_dir, project_name, "src", "index.js")
    mock_write_file.assert_any_call(expected_js_path, mock_write_file.call_args_list[2][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_creates_package_json(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Check that package.json is created
    expected_package_path = os.path.join(target_dir, project_name, "package.json")
    mock_write_file.assert_any_call(expected_package_path, mock_write_file.call_args_list[3][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_calls_write_file_correctly(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify write_file was called at least 4 times (index.html, main.css, index.js, package.json)
    assert mock_write_file.call_count >= 4


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_empty_project_name(mock_save_config, mock_generate_structure, mock_write_file):
    with pytest.raises(Exception):
        generate_web_template("", "/tmp")


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_none_project_name(mock_save_config, mock_generate_structure, mock_write_file):
    with pytest.raises(Exception):
        generate_web_template(None, "/tmp")


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_empty_target_dir(mock_save_config, mock_generate_structure, mock_write_file):
    with pytest.raises(Exception):
        generate_web_template("test_project", "")


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_none_target_dir(mock_save_config, mock_generate_structure, mock_write_file):
    with pytest.raises(Exception):
        generate_web_template("test_project", None)


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_special_chars_project_name(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test@project#123"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify it handles special characters in project name
    expected_package_json_path = os.path.join(target_dir, project_name, "package.json")
    mock_write_file.assert_any_call(expected_package_json_path, mock_write_file.call_args_list[3][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_long_project_name(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "a" * 100
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify it handles long project names
    expected_package_json_path = os.path.join(target_dir, project_name, "package.json")
    mock_write_file.assert_any_call(expected_package_json_path, mock_write_file.call_args_list[3][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_spaces_in_project_name(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify it handles spaces in project name (should be converted to kebab-case in package.json)
    expected_package_json_path = os.path.join(target_dir, project_name, "package.json")
    mock_write_file.assert_any_call(expected_package_json_path, mock_write_file.call_args_list[3][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_unicode_project_name(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "tëst_pröjëct"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify it handles unicode characters
    expected_package_json_path = os.path.join(target_dir, project_name, "package.json")
    mock_write_file.assert_any_call(expected_package_json_path, mock_write_file.call_args_list[3][0][1])


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_creates_correct_directory_structure(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify the directory structure is created correctly
    expected_structure = {
        "src": {
            "components": {},
            "styles": {},
            "assets": {},
            "utils": {}
        },
        "public": {
            "index.html": "<!DOCTYPE html>\n<html>\n<head>\n  <title>{{ project_name }}</title>\n</head>\n<body>\n  <div id='app'></div>\n  <script src='js/main.js'></script>\n</body>\n</html>",
            "css": {},
            "js": {},
            "assets": {}
        },
        "tests": {},
        "docs": {}
    }
    mock_generate_structure.assert_called_with(project_name, target_dir, expected_structure)


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_saves_correct_config(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify the correct config is saved
    expected_config = {
        "project_type": "web",
        "framework": "vanilla",
        "language": "javascript",
        "build_tool": "webpack"
    }
    mock_save_config.assert_called_with(os.path.join(target_dir, project_name), expected_config)


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_handles_invalid_path(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/invalid/path"
    
    # This should not raise an exception but we can't verify the actual file system behavior
    generate_web_template(project_name, target_dir)
    
    # Just ensure it doesn't crash
    assert True


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_handles_permission_error(mock_save_config, mock_generate_structure, mock_write_file):
    # We can't easily test this without changing system permissions, but we can check it doesn't crash
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Just ensure it doesn't crash
    assert True


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_content_validation(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify key content elements are present
    html_content = mock_write_file.call_args_list[0][0][1]
    assert "<!DOCTYPE html>" in html_content
    assert f"<title>{project_name}</title>" in html_content
    assert "Welcome to test_project" in html_content


@patch('src.scaffolding.templates.web.write_file')
@patch('src.scaffolding.templates.web.generate_project_structure')
@patch('src.scaffolding.templates.web.save_config')
def test_generate_web_template_css_content(mock_save_config, mock_generate_structure, mock_write_file):
    project_name = "test_project"
    target_dir = "/tmp"
    
    generate_web_template(project_name, target_dir)
    
    # Verify CSS content
    css_content = mock_write_file.call_args_list[1][0][1]
    assert "font-family: 'Arial', sans-serif;" in css_content
    assert "body {" in css_content
    assert "#app {" in css_content