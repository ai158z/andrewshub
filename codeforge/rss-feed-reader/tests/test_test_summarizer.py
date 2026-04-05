import pytest
from src.summarizer import summarize_text


def test_summarize_short_text():
    """Test that short text returns the original text when summarized."""
    short_text = "This is a short text."
    summary = summarize_text(short_text)
    assert summary == short_text


def test_summarize_long_text():
    """Test that long text is properly summarized."""
    long_text = "This is a significantly longer text. " * 100
    summary = summarize_text(long_text)
    assert len(summary) < len(long_text)
    assert len(summary) > 0
    assert "significantly" in summary or "longer" in summary


def test_summarize_empty_string():
    """Test summarizing an empty string."""
    assert summarize_text("") == ""


def test_summarize_none_input():
    """Test that None input raises appropriate error."""
    with pytest.raises((TypeError, ValueError)):
        summarize_text(None)


def test_summarize_single_sentence():
    """Test summarizing text with a single sentence."""
    text = "This is a single sentence."
    summary = summarize_text(text)
    assert summary == text


def test_summarize_text_with_special_characters():
    """Test summarizing text with special characters."""
    text = "Hello! How are you? This costs $5.99."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_summarize_text_with_newlines():
    """Test summarizing text containing newlines."""
    text = "First line.\nSecond line.\nThird line."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert "First line" in summary or "Second line" in summary or "Third line" in summary


def test_summarize_very_long_text():
    """Test summarizing very long text produces much shorter output."""
    text = "Word. " * 1000
    summary = summarize_text(text)
    assert len(summary) < len(text)
    assert len(summary) > 0


def test_summarize_text_with_only_spaces():
    """Test text with only spaces."""
    text = "     "
    summary = summarize_text(text)
    assert summary == text


def test_summarize_text_with_only_punctuation():
    """Test text with only punctuation."""
    text = "!@#$%^&*()"
    summary = summarize_text(text)
    assert len(summary) > 0


def test_summarize_multilingual_text():
    """Test summarizing text in different languages."""
    text = "This is English. Esto es español. C'est français."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_summarize_text_with_numbers():
    """Test summarizing text containing numbers."""
    text = "The price is 100 dollars and 50 cents."
    summary = summarize_text(text)
    assert "100" in summary or "50" in summary


def test_summarize_text_maintains_context():
    """Test that summary maintains some context from original."""
    text = "The weather today is sunny. The temperature is 75 degrees."
    summary = summarize_text(text)
    assert "weather" in summary or "temperature" in summary or "sunny" in summary


def test_summarize_repeated_sentences():
    """Test summarizing text with repeated content."""
    text = "This is repeated. This is repeated. This is repeated."
    summary = summarize_text(text)
    assert len(summary) > 0
    assert "This is repeated" in summary


def test_summarize_text_with_urls():
    """Test summarizing text containing URLs."""
    text = "Visit https://example.com for more information."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_summarize_text_with_email():
    """Test summarizing text containing email addresses."""
    text = "Contact us at info@example.com for help."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_summarize_text_with_paragraph_breaks():
    """Test summarizing text with multiple paragraphs."""
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_summarize_text_with_quotes():
    """Test summarizing text with quotation marks."""
    text = 'He said "Hello world" to everyone.'
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_summarize_text_consistency():
    """Test that summarization is consistent across calls."""
    text = "Consistency test text. " * 20
    summary1 = summarize_text(text)
    summary2 = summarize_text(text)
    assert summary1 == summary2


def test_summarize_text_length_boundaries():
    """Test boundary conditions for text length."""
    # Test exactly at some common boundary lengths
    short = "A" * 100
    medium = "B" * 500
    long = "C" * 1000
    
    # All should produce valid string results
    assert isinstance(summarize_text(short), str)
    assert isinstance(summarize_text(medium), str)
    assert isinstance(summarize_text(long), str)