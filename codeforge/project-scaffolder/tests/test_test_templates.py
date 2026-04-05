import pytest
from pathlib import Path
from src.scaffolder.templates.python import python_cli_template, python_web_template, python_lib_template
from src.scaffolder.templates.javascript import js_cli_template, js_web_template, js_lib_template
from src.scaffolder.templates.rust import rust_cli_template, rust_web_template, rust_lib_template
from src.scaffolder.core import TemplateManager

@pytest.mark.parametrize("template_func", [
    python_cli_template,
    python_web_template,
    python_lib_template,
    js_cli_template,
    js_web_template,
    js_lib_template,
    rust_cli_template,
    rust_web_template,
    rust_lib_template
])
def test_template_has_required_structure(template_func):
    template = template_func()
    assert "name" in template
    assert "files" in template
    assert isinstance(template["files"], dict)
    assert isinstance(template["name"], str)
    assert len(template["name"]) > 0

@pytest.mark.parametrize("template_func", [
    python_cli_template,
    python_web_template,
    python_lib_template
])
def test_python_templates_structure(template_func):
    template = template_func()
    for file_path, content in template["files"].items():
        assert file_path is not None
        assert content is not None or isinstance(content, dict)

@pytest.mark.parametrize("template_func", [
    js_cli_template,
    js_web_template,
    js_lib_template
])
def test_javascript_templates_structure(template_func):
    template = template_func()
    for file_path, content in template["files"].items():
        assert isinstance(file_path, str)
        assert content is not None or isinstance(content, (str, dict))

@pytest.mark.parametrize("template_func", [
    rust_cli_template,
    rust_web_template,
    rust_lib_template
])
def test_rust_templates_structure(template_func):
    template = template_func()
    for file_path, content in template["files"].items():
        assert isinstance(file_path, str)
        assert content is not None

def test_template_validation_with_valid_templates():
    template_manager = TemplateManager()
    templates = [
        python_cli_template(),
        js_web_template(),
        rust_lib_template()
    ]
    
    for template in templates:
        assert template_manager.validate_template(template) is True
        assert "name" in template
        assert "files" in template
        assert isinstance(template["name"], str)
        assert isinstance(template["files"], dict)
        assert len(template["name"]) > 0
        assert " " not in template["name"]
        
        for file_path, content in template["files"].items():
            assert isinstance(file_path, str)
            assert content is not None