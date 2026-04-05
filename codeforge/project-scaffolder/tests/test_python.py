import pytest
from src.scaffolder.templates.python import (
    python_cli_template,
    python_web_template,
    python_lib_template
)

class TestPythonTemplates:
    def test_python_cli_template_structure(self):
        """Test that python_cli_template returns the expected structure."""
        template = python_cli_template()
        assert isinstance(template, dict)
        assert template["template_name"] == "python-cli"
        assert template["display_name"] == "Python CLI Application"
        assert template["description"] == "A command-line interface application template"
        assert "src/__init__.py" in template["files"]
        assert "src/main.py" in template["files"]
        assert "src/cli.py" in template["files"]

    def test_python_web_template_structure(self):
        """Test that python_web_template returns the expected structure."""
        template = python_web_template()
        assert isinstance(template, dict)
        assert template["template_name"] == "python-web"
        assert template["display_name"] == "Python Web Application"
        assert template["description"] == "A web application template using FastAPI"
        assert "src/__init__.py" in template["files"]
        assert "src/main.py" in template["files"]

    def test_python_lib_template_structure(self):
        """Test that python_lib_template returns the expected structure."""
        template = python_lib_template()
        assert isinstance(template, dict)
        assert template["template_name"] == "python-lib"
        assert template["display_name"] == "Python Library"
        assert template["description"] == "A Python library package template"
        assert "src/__init__.py" in template["files"]

    def test_template_functions_return_distinct_templates(self):
        """Test that each template function returns a unique template."""
        cli_template = python_cli_template()
        web_template = python_web_template()
        lib_template = python_lib_template()

        assert cli_template["template_name"] != web_template["template_name"]
        assert web_template["template_name"] != lib_template["template_name"]
        assert cli_template["template_name"] != lib_template["template_name"]

    def test_cli_template_main_py_content(self):
        """Test that CLI template main.py contains expected Typer app structure."""
        template = python_cli_template()
        main_content = template["files"]["src/main.py"]
        assert "import typer" in main_content
        assert "app = typer.Typer()" in main_content
        assert "def hello(name: str" in main_content
        assert "def goodbye(name: str" in main_content

    def test_cli_template_cli_py_content(self):
        """Test that CLI template cli.py contains expected structure."""
        template = python_cli_template()
        cli_content = template["files"]["src/cli.py"]
        assert "import typer" in cli_content
        assert "app = typer.Typer()" in cli_content
        assert "main()" in cli_content

    def test_web_template_main_py_content(self):
        """Test that web template main.py contains expected FastAPI structure."""
        template = python_web_template()
        main_content = template["files"]["src/main.py"]
        assert "from fastapi import FastAPI" in main_content
        assert "app = FastAPI()" in main_content
        assert "class Message(BaseModel):" in main_content

    def test_lib_template_init_py_content(self):
        """Test that lib template __init__.py contains expected content."""
        template = python_lib_template()
        init_content = template["files"]["src/__init__.py"]
        assert "__version__" in init_content

    def test_all_templates_have_required_fields(self):
        """Test that all templates have required fields."""
        templates = [
            python_cli_template(),
            python_web_template(),
            python_lib_template()
        ]
        
        for template in templates:
            assert "template_name" in template
            assert "display_name" in template
            assert "description" in template
            assert "files" in template
            assert isinstance(template["files"], dict)

    def test_template_names_are_unique(self):
        """Test that template names are unique identifiers."""
        cli = python_cli_template()
        web = python_web_template()
        lib = python_lib_template()
        
        assert cli["template_name"] == "python-cli"
        assert web["template_name"] == "python-web"
        assert lib["template_name"] == "python-lib"

    def test_template_descriptions_are_distinct(self):
        """Test that template descriptions are unique."""
        cli = python_cli_template()
        web = python_web_template()
        lib = python_lib_template()
        
        assert cli["description"] != web["description"]
        assert web["description"] != lib["description"]
        assert cli["description"] != lib["description"]

    def test_files_dict_not_empty(self):
        """Test that files dictionary is not empty for all templates."""
        templates = [
            python_cli_template(),
            python_web_template(),
            python_lib_template()
        ]
        
        for template in templates:
            assert len(template["files"]) > 0

    def test_cli_template_has_main_and_cli_files(self):
        """Test that CLI template has expected file structure."""
        template = python_cli_template()
        files = template["files"]
        assert "src/__init__.py" in files
        assert "src/main.py" in files
        assert "src/cli.py" in files

    def test_web_template_has_main_file(self):
        """Test that web template has expected file structure."""
        template = python_web_template()
        files = template["files"]
        assert "src/__init__.py" in files
        assert "src/main.py" in files

    def test_lib_template_has_init_file(self):
        """Test that lib template has expected file structure."""
        template = python_lib_template()
        files = template["files"]
        assert "src/__init__.py" in files

    def test_no_extra_files_in_templates(self):
        """Test that no unexpected files exist in templates."""
        cli = python_cli_template()
        web = python_web_template()
        lib = python_lib_template()
        
        # Check that files match exactly what's expected
        assert set(cli["files"].keys()) == {"src/__init__.py", "src/main.py", "src/cli.py"}
        assert set(web["files"].keys()) == {"src/__init__.py", "src/main.py"}
        assert set(lib["files"].keys()) == {"src/__init__.py"}

    def test_template_file_content_types(self):
        """Test that all file contents are strings."""
        templates = [
            python_cli_template(),
            python_web_template(),
            python_lib_template()
        ]
        
        for template in templates:
            for filename, content in template["files"].items():
                assert isinstance(content, str)

    def test_template_names_follow_convention(self):
        """Test that template names follow expected naming convention."""
        cli = python_cli_template()
        web = python_web_template()
        lib = python_lib_template()
        
        assert cli["template_name"].startswith("python-")
        assert web["template_name"].startswith("python-")
        assert lib["template_name"].startswith("python-")