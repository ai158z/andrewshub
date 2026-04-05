import pytest
from unittest.mock import patch, mock_open
from src.templates.python_template import PythonTemplate


def test_render_template_with_valid_inputs():
    template = PythonTemplate()
    result = template.render("Hello {{name}}", {"name": "World"})
    assert result == "Hello World"


def test_render_template_missing_variable():
    template = PythonTemplate()
    result = template.render("Hello {{name}}", {})
    assert result == "Hello "


def test_render_template_undefined_variable():
    template = PythonTemplate()
    result = template.render("Hello {{name}}", {"other": "value"})
    assert result == "Hello "


def test_render_template_multiple_variables():
    template = PythonTemplate()
    result = template.render("Hello {{first}} {{last}}", {"first": "John", "last": "Doe"})
    assert result == "Hello John Doe"


def test_render_template_escaped_content():
    template = PythonTemplate()
    result = template.render("{{content}}", {"content": "<script>alert('xss')</script>"})
    assert result == "<script>alert('xss')</script>"


def test_render_template_none_context():
    template = PythonTemplate()
    result = template.render("Hello {{name}}", None)
    assert result == "Hello "


def test_render_template_empty_template():
    template = PythonTemplate()
    result = template.render("", {"name": "test"})
    assert result == ""


def test_render_template_no_placeholders():
    template = PythonTemplate()
    result = template.render("Hello World", {"name": "test"})
    assert result == "Hello World"


def test_render_template_special_characters():
    template = PythonTemplate()
    result = template.render("Price: ${{price}}", {"price": "19.99"})
    assert result == "Price: $19.99"


def test_render_template_nested_dictionary():
    template = PythonTemplate()
    result = template.render("{{user.name}}", {"user": {"name": "Alice"}})
    assert result == "Alice"


def test_render_template_list_in_context():
    template = PythonTemplate()
    result = template.render("Items: {{items}}", {"items": ["a", "b"]})
    assert result == "Items: ['a', 'b']"


def test_render_template_boolean_value():
    template = PythonTemplate()
    result = template.render("Active: {{active}}", {"active": True})
    assert result == "Active: True"


def test_render_template_integer_value():
    template = PythonTemplate()
    result = template.render("Count: {{count}}", {"count": 42})
    assert result == "Count: 42"


def test_render_template_float_value():
    template = PythonTemplate()
    result = template.render("Price: {{price}}", {"price": 99.99})
    assert result == "Price: 99.99"


def test_render_template_complex_template():
    template = PythonTemplate()
    template_str = "User {{user.name}} has {{user.age}} years and lives in {{location}}"
    context = {
        "user": {"name": "John", "age": 30},
        "location": "NYC"
    }
    result = template.render(template_str, context)
    assert result == "User John has 30 years and lives in NYC"


def test_render_template_with_none_value():
    template = PythonTemplate()
    result = template.render("Value: {{value}}", {"value": None})
    assert result == "Value: None"


def test_render_template_with_empty_string():
    template = PythonTemplate()
    result = template.render("{{value}}", {"value": ""})
    assert result == ""


def test_render_template_escaped_curly_braces():
    template = PythonTemplate()
    result = template.render(r"Literal \{\{name\}\}", {"name": "John"})
    assert result == r"Literal \{\{name\}\}"


def test_render_template_multiple_same_placeholders():
    template = PythonTemplate()
    result = template.render("{{name}} and {{name}}", {"name": "John"})
    assert result == "John and John"


def test_render_template_newline_characters():
    template = PythonTemplate()
    result = template.render("Line1\nLine2\n{{value}}", {"value": "Line3"})
    assert result == "Line1\nLine2\nLine3"