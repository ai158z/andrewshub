import os
import json
from unittest.mock import patch, mock_open, call
from src.scaffolding.templates.javascript import generate_javascript_template

def test_generate_javascript_template_creates_directories(tmp_path):
    with patch("src.scaffolding.templates.javascript.os.makedirs") as mock_makedirs:
        generate_javascript_template("test-project", str(tmp_path))
        # Check that directories are created
        expected_dirs = [str(tmp_path / "src"), str(tmp_path / "tests")]
        for expected_dir in expected_dirs:
            mock_makedirs.assert_any_call(expected_dir, exist_ok=True)

def test_generate_javascript_template_creates_files_correctly(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("test-project", str(tmp_path))
        
        # Check all expected files are written
        expected_calls = [
            call(str(tmp_path / "src" / "index.js"), "console.log('Hello, world!');\n"),
            call(str(tmp_path / "tests" / "index.test.js"), "// Tests for index.test.js\n"),
            call(str(tmp_path / "package.json"), mock_write.call_args_list[3][0][1]),  # package.json content
            call(str(tmp_path / ".gitignore"), "node_modules\n.DS_Store\n*.log\n"),
            call(str(tmp_path / "README.md"), "# test-project\n\nA JavaScript project.\n")
        ]
        
        # Check that write_file was called with expected arguments
        assert mock_write.call_count == 5
        mock_write.assert_any_call(str(tmp_path / "src" / "index.js"), "console.log('Hello, world!');\n")
        mock_write.assert_any_call(str(tmp_path / "tests" / "index.test.js"), "// Tests for index.test.js\n")
        mock_write.assert_any_call(str(tmp_path / ".gitignore"), "node_modules\n.DS_Store\n*.log\n")
        mock_write.assert_any_call(str(tmp_path / "README.md"), "# test-project\n\nA JavaScript project.\n")

def test_generate_javascript_template_package_json_content(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("test-project", str(tmp_path))
        
        # Get the package.json content from the calls
        package_json_call = None
        for c in mock_write.call_args_list:
            if "package.json" in c[0][0]:
                package_json_call = c
                break
        
        # Verify package.json has correct structure
        expected_package = {
            "name": "test-project",
            "version": "1.0.0",
            "description": "",
            "main": "src/index.js",
            "scripts": {
                "test": "echo \"Error: no test specified\" && exit 1"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }
        assert json.loads(package_json_call[0][1]) == expected_package

def test_generate_javascript_template_empty_project_name(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("", str(tmp_path))
        
        # Should still create files with empty name in README
        mock_write.assert_any_call(str(tmp_path / "README.md"), "# \n\nA JavaScript project.\n")

def test_generate_javascript_template_none_project_name(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("None", str(tmp_path))
        
        # Check that it doesn't crash with "None" as project name
        mock_write.assert_any_call(str(tmp_path / "README.md"), "# None\n\nA JavaScript project.\n")

def test_generate_javascript_template_special_characters_in_name(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("test@#$%project", str(tmp_path))
        
        # Should handle special characters in project name
        mock_write.assert_any_call(str(tmp_path / "README.md"), "# test@#$%project\n\nA JavaScript project.\n")

def test_generate_javascript_template_long_project_name(tmp_path):
    long_name = "a" * 100
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template(long_name, str(tmp_path))
        
        # Should handle long project names
        expected_readme = f"# {long_name}\n\nA JavaScript project.\n"
        mock_write.assert_any_call(str(tmp_path / "README.md"), expected_readme)

def test_generate_javascript_template_invalid_target_directory():
    # Test with invalid directory path
    with patch("src.scaffolding.templates.javascript.os.makedirs", side_effect=OSError("Permission denied")):
        try:
            generate_javascript_template("test", "/invalid/path")
        except Exception:
            pass  # We expect this to fail, but we're testing the behavior

def test_generate_javascript_template_write_file_exception(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file", side_effect=Exception("Write error")):
        try:
            generate_javascript_template("test", str(tmp_path))
            assert False, "Expected exception not raised"
        except Exception:
            pass  # Expected

def test_generate_javascript_template_makedirs_exception(tmp_path):
    with patch("src.scaffolding.templates.javascript.os.makedirs", side_effect=OSError("Permission denied")):
        try:
            generate_javascript_template("test", str(tmp_path))
            assert False, "Expected exception not raised"
        except OSError:
            pass  # Expected

def test_generate_javascript_template_creates_correct_file_paths(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("test-project", str(tmp_path))
        
        expected_paths = [
            str(tmp_path / "src" / "index.js"),
            str(tmp_path / "tests" / "index.test.js"),
            str(tmp_path / "package.json"),
            str(tmp_path / ".gitignore"),
            str(tmp_path / "README.md")
        ]
        
        for path in expected_paths:
            # Check that each path was used in a write_file call
            assert any(call[0][0] == path for call in mock_write.call_args_list)

def test_generate_javascript_template_file_content_integrity(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("test-project", str(tmp_path))
        
        # Verify content integrity
        mock_write.assert_any_call(str(tmp_path / "src" / "index.js"), "console.log('Hello, world!');\n")
        mock_write.assert_any_call(str(tmp_path / "tests" / "index.test.js"), "// Tests for index.test.js\n")

def test_generate_javascript_template_gitignore_content(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("test-project", str(tmp_path))
        mock_write.assert_any_call(str(tmp_path / ".gitignore"), "node_modules\n.DS_Store\n*.log\n")

def test_generate_javascript_template_readme_content(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("my-awesome-project", str(tmp_path))
        mock_write.assert_any_call(str(tmp_path / "README.md"), "# my-awesome-project\n\nA JavaScript project.\n")

def test_generate_javascript_template_directory_structure(tmp_path):
    with patch("src.scaffolding.templates.javascript.os.makedirs") as mock_makedirs, \
         patch("src.scaffolding.templates.javascript.write_file"):
        generate_javascript_template("test-project", str(tmp_path))
        
        # Verify directories are created
        mock_makedirs.assert_any_call(str(tmp_path / "src"), exist_ok=True)
        mock_makedirs.assert_any_call(str(tmp_path / "tests"), exist_ok=True)

def test_generate_javascript_template_edge_case_spaces_in_name(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("test project", str(tmp_path))
        mock_write.assert_any_call(str(tmp_path / "README.md"), "# test project\n\nA JavaScript project.\n")

def test_generate_javascript_template_edge_case_empty_string_name(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        generate_javascript_template("", str(tmp_path))
        mock_write.assert_any_call(str(tmp_path / "README.md"), "# \n\nA JavaScript project.\n")

def test_generate_javascript_template_multiple_special_chars(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        name = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        generate_javascript_template(name, str(tmp_path))
        mock_write.assert_any_call(str(tmp_path / "README.md"), f"# {name}\n\nA JavaScript project.\n")

def test_generate_javascript_template_unicode_name(tmp_path):
    with patch("src.scaffolding.templates.javascript.write_file") as mock_write:
        unicode_name = "🚀project"
        generate_javascript_template(unicode_name, str(tmp_path))
        mock_write.assert_any_call(str(tmp_path / "README.md"), f"# 🚀project\n\nA JavaScript project.\n")