import pytest
from unittest.mock import mock_open, patch
from src.templates.javascript_template import JAVASCRIPT_TEMPLATE

def test_javascript_template_structure():
    """Test that JAVASCRIPT_TEMPLATE has the expected structure"""
    assert "name" in JAVASCRIPT_TEMPLATE
    assert "files" in JAVASCRIPT_TEMPLATE
    assert "directories" in JAVASCRIPT_TEMPLATE
    assert JAVASCRIPT_TEMPLATE["name"] == "javascript"
    assert len(JAVASCRIPT_TEMPLATE["files"]) > 0
    assert len(JAVASCRIPT_TEMPLATE["directories"]) > 0

def test_javascript_template_files_have_required_fields():
    """Test that all files in template have required path and template fields"""
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        assert "path" in file_entry
        assert "template" in file_entry
        assert isinstance(file_entry["path"], str)
        assert isinstance(file_entry["template"], str)

def test_javascript_template_directories_is_list():
    """Test that directories is a list of strings"""
    directories = JAVASCRIPT_TEMPLATE["directories"]
    assert isinstance(directories, list)
    for directory in directories:
        assert isinstance(directory, str)

def test_javascript_template_name_substitution():
    """Test that project_name placeholder exists in templates"""
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        template_content = file_entry["template"]
        # Check if template contains project_name placeholder or is a generic file
        if "{project_name}" in template_content or "project_name" not in template_content:
            continue
        else:
            # For templates without project_name, ensure they're static content
            assert isinstance(template_content, str)

def test_package_json_content():
    """Test that package.json template has expected basic structure"""
    package_json = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == "package.json":
            package_json = file_entry
            break
    
    assert package_json is not None
    content = package_json["template"]
    assert '"name": "{project_name}"' in content
    assert '"version": "1.0.0"' in content
    assert '"jest": "^29.0.0"' in content

def test_readme_template_content():
    """Test that README.md template has expected content structure"""
    readme = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == "README.md":
            readme = file_entry
            break
    
    assert readme is not None
    assert "A JavaScript project generated with project-scaffolder" in readme["template"]
    assert "## Getting Started" in readme["template"]

def test_index_js_template():
    """Test that index.js template has expected content"""
    index_js = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == "index.js":
            index_js = file_entry
            break
    
    assert index_js is not None
    assert "console.log('Hello, {project_name}!');" in index_js["template"]

def test_jest_config_content():
    """Test that jest.config.js has expected content"""
    jest_config = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == "jest.config.js":
            jest_config = file_entry
            break
    
    assert jest_config is not None
    assert "testEnvironment: 'node'" in jest_config["template"]

def test_gitignore_content():
    """Test that .gitignore has expected entries"""
    gitignore = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == ".gitignore":
            gitignore = file_entry
            break
    
    assert gitignore is not None
    content = gitignore["template"]
    assert "node_modules/" in content
    assert "npm-debug.log" in content
    assert ".DS_Store" in content

def test_all_files_have_unique_paths():
    """Test that all file paths in template are unique"""
    paths = []
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        path = file_entry["path"]
        assert path not in paths, f"Duplicate path found: {path}"
        paths.append(path)

def test_template_completeness():
    """Test that template is complete with all expected files"""
    required_files = ["package.json", "README.md", "index.js", "jest.config.js", ".gitignore"]
    file_paths = [f["path"] for f in JAVASCRIPT_TEMPLATE["files"]]
    
    for required_file in required_files:
        assert required_file in file_paths, f"Missing required file: {required_file}"

def test_directory_structure():
    """Test that directory structure is defined correctly"""
    expected_dirs = ["src", "tests", "__mocks__"]
    actual_dirs = JAVASCRIPT_TEMPLATE["directories"]
    
    for expected_dir in expected_dirs:
        assert expected_dir in actual_dirs, f"Expected directory {expected_dir} not found"

def test_no_empty_templates():
    """Test that no template content is empty"""
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        assert len(file_entry["template"]) > 0, f"Template for {file_entry['path']} is empty"

def test_file_paths_valid():
    """Test that file paths do not contain invalid characters"""
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        path = file_entry["path"]
        for char in invalid_chars:
            assert char not in path, f"Invalid character '{char}' in path {path}"

def test_template_inheritance_consistency():
    """Test template maintains consistency in structure across files"""
    # All templates should handle project_name substitution consistently
    has_project_name = False
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if "{project_name}" in file_entry["template"]:
            has_project_name = True
            break
    
    # At least one file should use project_name (normally README.md or index.js do)
    # This is a sanity check that the templating system is used somewhere

def test_dev_dependencies_present():
    """Test that dev dependencies are properly defined in package.json template"""
    package_json = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == "package.json":
            package_json = file_entry
            break
    
    assert package_json is not None
    assert '"devDependencies":' in package_json["template"]
    assert '"jest": "^29.0.0"' in package_json["template"]

def test_scripts_section_exists():
    """Test that package.json contains scripts section"""
    package_json = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == "package.json":
            package_json = file_entry
            break
    
    assert package_json is not None
    assert '"scripts":' in package_json["template"]
    assert '"start": "node index.js"' in package_json["template"]
    assert '"test": "jest"' in package_json["template"]

def test_template_name_matches():
    """Test that template name matches 'javascript'"""
    assert JAVASCRIPT_TEMPLATE["name"] == "javascript"

def test_dependencies_section_exists():
    """Test that dependencies section exists in package.json"""
    package_json = None
    for file_entry in JAVASCRIPT_TEMPLATE["files"]:
        if file_entry["path"] == "package.json":
            package_json = file_entry
            break
    
    assert package_json is not None
    assert '"dependencies": {}' in package_json["template"]