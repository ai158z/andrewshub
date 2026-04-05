import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import pytest
from src.scaffolder.generator import FileGenerator

def test_create_directory_new(tmp_path):
    generator = FileGenerator()
    new_dir = tmp_path / "new_dir"
    result = generator.create_directory(str(new_dir))
    assert result is True
    assert new_dir.exists()
    assert new_dir.is_dir()

def test_create_directory_exists(tmp_path):
    generator = FileGenerator()
    existing_dir = tmp_path / "existing"
    existing_dir.mkdir()
    result = generator.create_directory(str(existing_dir))
    assert result is False

def test_create_directory_exists_as_file(tmp_path):
    generator = FileGenerator()
    existing_file = tmp_path / "file.txt"
    existing_file.write_text("test")
    with pytest.raises(FileExistsError):
        generator.create_directory(str(existing_file))

def test_create_directory_permission_error(tmp_path):
    generator = FileGenerator()
    no_perm_path = tmp_path / "no_perm"
    no_perm_path.mkdir(mode=0o000)
    with pytest.raises(PermissionError):
        generator.create_directory(str(no_perm_path / "test"))

def test_write_file_new(tmp_path):
    generator = FileGenerator()
    file_path = tmp_path / "test.txt"
    result = generator.write_file(str(file_path), "content")
    assert result is True
    assert file_path.read_text() == "content"

def test_write_file_exists_no_overwrite(tmp_path):
    generator = FileGenerator()
    file_path = tmp_path / "test.txt"
    file_path.write_text("existing")
    result = generator.write_file(str(file_path), "new_content")
    assert result is False
    assert file_path.read_text() == "existing"

def test_write_file_overwrite(tmp_path):
    generator = FileGenerator()
    file_path = tmp_path / "test.txt"
    file_path.write_text("existing")
    result = generator.write_file(str(file_path), "new_content", overwrite=True)
    assert result is True
    assert file_path.read_text() == "new_content"

def test_write_file_create_parents(tmp_path):
    generator = FileGenerator()
    file_path = tmp_path / "new_dir" / "test.txt"
    result = generator.write_file(str(file_path), "content")
    assert result is True
    assert file_path.read_text() == "content"

def test_write_file_permission_error(tmp_path):
    generator = FileGenerator()
    protected_dir = tmp_path / "protected"
    protected_dir.mkdir(mode=0o000)
    file_path = protected_dir / "test.txt"
    with pytest.raises(PermissionError):
        generator.write_file(str(file_path), "content")

def test_copy_template_no_env():
    generator = FileGenerator()
    with pytest.raises(ValueError, match="Template directory not configured"):
        generator.copy_template("template.txt", "/tmp/output", {})

def test_copy_template_render(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "test.txt").write_text("Hello {{ name }}!")
    
    generator = FileGenerator(str(template_dir))
    with patch("src.scaffolder.generator.open", mock_open()) as mock_file:
        with patch("pathlib.Path.mkdir"):
            generator.copy_template("test.txt", "/tmp/output", {"name": "World"})
            mock_file.assert_called()
            # Check if the file handle was called with correct content
            handle = mock_file()
            handle.write.assert_called_once_with("Hello World!")

def test_generate_project_structure_no_template(tmp_path):
    generator = FileGenerator()
    structure = {
        "dir1": {
            "file1.txt": "content1",
            "file2.txt": "content2"
        },
        "file3.txt": "content3"
    }
    base_path = tmp_path / "project"
    generator.generate_project_structure(str(base_path), structure)
    
    assert (base_path / "dir1" / "file1.txt").read_text() == "content1"
    assert (base_path / "dir1" / "file2.txt").read_text() == "content2"
    assert (base_path / "file3.txt").read_text() == "content3"

def test_generate_project_structure_with_template(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "template.txt").write_text("Hello {{ name }}!")
    
    generator = FileGenerator(str(template_dir))
    structure = {
        "template.txt": "Hello {{ name }}!"
    }
    base_path = tmp_path / "output"
    context = {"name": "World"}
    generator.generate_project_structure(str(base_path), structure, context)
    output_file = base_path / "template.txt"
    assert output_file.read_text() == "Hello World!"

def test_invalid_structure_content_type(tmp_path):
    generator = FileGenerator()
    structure = {
        "invalid_item": 123  # Invalid content type
    }
    base_path = tmp_path / "project"
    with patch("src.scaffolder.generator.logger") as mock_logger:
        generator.generate_project_structure(str(base_path), structure)
        mock_logger.warning.assert_called()

def test_jinja_env_not_set_with_context(tmp_path):
    generator = FileGenerator()  # No template dir
    structure = {
        "file.txt": "Hello {{ name }}!"
    }
    base_path = tmp_path / "project"
    context = {"name": "World"}
    generator.generate_project_structure(str(base_path), structure, context)
    # Should write raw content when no template engine and context provided for string content
    assert (base_path / "file.txt").read_text() == "Hello {{ name }}!"

def test_directory_with_subdir(tmp_path):
    generator = FileGenerator()
    structure = {
        "parent_dir": {
            "child_dir": {
                "file.txt": "content"
            }
        }
    }
    base_path = tmp_path / "project"
    generator.generate_project_structure(str(base_path), structure)
    assert (base_path / "parent_dir" / "child_dir" / "file.txt").read_text() == "content"

def test_empty_string_content(tmp_path):
    generator = FileGenerator()
    structure = {
        "empty_file.txt": ""
    }
    base_path = tmp_path / "project"
    generator.generate_project_structure(str(base_path), structure)
    assert (base_path / "empty_file.txt").read_text() == ""

def test_none_context(tmp_path):
    generator = FileGenerator()
    structure = {
        "file.txt": "test content"
    }
    base_path = tmp_path / "project"
    generator.generate_project_structure(str(base_path), structure, None)
    assert (base_path / "file.txt").read_text() == "test content"