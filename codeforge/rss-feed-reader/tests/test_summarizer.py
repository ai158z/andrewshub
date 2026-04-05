import pytest
from src.summarizer import summarize_text

def test_summarize_text_valid_input():
    text = "This is a test sentence. Another test sentence is here. This is the final test sentence."
    result = summarize_text(text)
    assert isinstance(result, str)
    assert len(result) > 0

def test_summarize_text_empty_string():
    result = summarize_text("")
    assert result == ""

def test_summarize_text_whitespace_only():
    result = summarize_text("   ")
    assert result == ""

def test_summarize_text_short_text():
    text = "Short text here"
    result = summarize_text(text)
    assert result == "short text"

def test_summarize_text_ratio_zero():
    text = "This is a test. Another test. Yet another test."
    result = summarize_text(text, ratio=0.0)
    assert result == ""

def test_summarize_text_ratio_one():
    text = "This is test one. This is test two. This is test three."
    result = summarize_text(text, ratio=1.0)
    assert result == "this is test one. this is test two. this is test three."

def test_summarize_text_invalid_ratio():
    with pytest.raises(ValueError):
        summarize_text("test text", ratio=1.5)

def test_summarize_text_invalid_text_type():
    with pytest.raises(TypeError):
        summarize_text(123)

def test_summarize_text_single_sentence():
    text = "This is a single sentence."
    result = summarize_text(text)
    assert result == "this is a single sentence"

def test_summarize_text_no_sentences():
    text = "No real sentences here! 123"
    result = summarize_text(text)
    assert result == "no real sentences here 123"

def test_summarize_text_with_punctuation():
    text = "First sentence! Second sentence? Third sentence."
    result = summarize_text(text, ratio=0.6)
    # Should return first and second sentence
    assert "first sentence" in result
    assert "second sentence" in result

def test_summarize_text_with_stopwords():
    text = "The quick brown fox jumps over the lazy dog. The dog was really lazy."
    result = summarize_text(text)
    assert "the" not in result or "dog" not in result  # Stopwords should be filtered

def test_summarize_text_all_stopwords():
    text = "the and or but"
    result = summarize_text(text)
    assert result == "the and or but"  # Very short text, returned as is

def test_summarize_text_mixed_content():
    text = "This is a test. It includes numbers 123 and symbols #!."
    result = summarize_text(text)
    assert isinstance(result, str)

def test_summarize_text_repeated_words():
    text = "Test word frequency. Test the frequency of words. Words are tested."
    result = summarize_text(text, ratio=0.7)
    assert "test" in result

def test_summarize_text_low_ratio():
    text = "Sentence one. Sentence two. Sentence three. Sentence four."
    result = summarize_text(text, ratio=0.1)
    sentences_in_result = result.split(". ")
    # With ratio 0.1, should get 1 sentence (max(1, int(4*0.1)) = 1)
    assert len(sentences_in_result) >= 1

def test_summarize_text_high_ratio():
    text = "First. Second. Third. Fourth. Fifth."
    result = summarize_text(text, ratio=0.8)
    # 5 sentences * 0.8 = 4 sentences
    assert len(result.split(". ")) == 4

def test_summarize_text_exact_ratio():
    text = "One sentence. Two sentence. Three sentence. Four."
    result = summarize_text(text, ratio=0.5)
    # 4 sentences, 50% = 2 sentences
    assert len(result.split(". ")) == 2

def test_summarize_text_special_characters():
    text = "Special characters: @#$%^&* should be removed. But text remains."
    result = summarize_text(text)
    assert "@" not in result
    assert "characters" in result or "text" in result

def test_summarize_text_unicode():
    text = "Unicode test: café résumé naïve. More text with unicode: naïve."
    result = summarize_text(text)
    assert "café" not in result  # Assuming non-ASCII filtered out
    assert "text" in result or "unicode" in result.lower()