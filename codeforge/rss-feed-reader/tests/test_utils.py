import pytest
import re

def test_is_valid_url_with_valid_urls():
    from src.utils import is_valid_url
    assert is_valid_url("http://example.com") is True
    assert is_valid_url("https://example.com") is True
    assert is_valid_url("https://www.example.com/path?query=1") is True

def test_is_valid_url_with_invalid_urls():
    from src.utils import is_valid_url
    assert is_valid_url("") is False
    assert is_valid_url("not a url") is False
    assert is_valid_url("http://") is False
    assert is_valid_url("example.com") is False

def test_is_valid_url_with_non_string_input():
    from src.utils import is_valid_url
    assert is_valid_url(None) is False
    assert is_valid_url(123) is False

def test_sanitize_text_with_valid_input():
    from src.utils import sanitize_text
    result = sanitize_text("  Hello   world!  ")
    assert result == "Hello world!"

def test_sanitize_text_removes_extra_whitespace():
    from src.utils import sanitize_text
    result = sanitize_text("  multiple   spaces   here  ")
    assert result == "multiple spaces here"

def test_sanitize_text_removes_special_characters():
    from src.utils import sanitize_text
    result = sanitize_text("Hello\x00\x01World")
    assert result == "HelloWorld"

def test_sanitize_text_removes_urls():
    from src.utils import sanitize_text
    result = sanitize_text("Visit http://example.com for more info")
    assert "http://example.com" not in result

def test_sanitize_text_removes_html_tags():
    from src.utils import sanitize_text
    result = sanitize_text("<p>Hello <b>World</b></p>")
    assert "<p>" not in result
    assert "<b>" not in result
    assert "Hello World" in result

def test_sanitize_text_with_non_string_input():
    from src.utils import sanitize_text
    with pytest.raises(TypeError):
        sanitize_text(123)

def test_sanitize_text_strips_and_compacts_whitespace():
    from src.utils import sanitize_text
    result = sanitize_text("  \n\t  Hello    World  \n\t  ")
    assert result == "Hello World"

def test_sanitize_text_empty_string():
    from src.utils import sanitize_text
    result = sanitize_text("")
    assert result == ""

def test_sanitize_text_none_input():
    from src.utils import sanitize_text
    result = sanitize_text("   ")
    assert result == ""

def test_is_valid_url_edge_case_empty_string():
    from src.utils import is_valid_url
    assert is_valid_url("") is False

def test_is_valid_url_edge_case_none():
    from src.utils import is_valid_url
    assert is_valid_url(None) is False

def test_is_valid_url_edge_case_no_scheme():
    from src.utils import is_valid_url
    assert is_valid_url("example.com") is False

def test_is_valid_url_edge_case_ftp():
    from src.utils import is_valid_url
    assert is_valid_url("ftp://files.example.com") is True

def test_sanitize_text_preserves_valid_characters():
    from src.utils import sanitize_text
    result = sanitize_text("Normal text with numbers 123 and symbols !@#")
    assert result == "Normal text with numbers 123 and symbols !@#"

def test_sanitize_text_removes_unicode():
    from src.utils import sanitize_text
    result = sanitize_text("Text with unicode: \u00A9 \u00AE \u2122")
    # Should remove unicode characters outside of \x20-\x7E
    assert "\u00A9" not in result
    assert "\u00AE" not in result
    assert "\u2122" not in result

def test_sanitize_text_complete_example():
    from src.utils import sanitize_text
    result = sanitize_text("  Visit <a>http://bad.com</a> or   contact   us\tat info@example.com  ")
    # After sanitization, should have no URLs, no HTML, no extra spaces
    assert "http://bad.com" not in result
    assert "<a>" not in result
    assert result == "Visit or contact us at info@example.com"