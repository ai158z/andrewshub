import re
import nltk
from collections import Counter
from typing import List, Dict
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import string

# Setup for the module
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

STOPWORDS = set(stopwords.words('english'))

def _remove_punctuation(text: str) -> str:
    """Remove punctuation from text"""
    return re.sub(r'[^\w\s]', '', text)

def _preprocess_text(text: str) -> str:
    """Preprocess text"""
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text.lower().strip())
    return text

def _calculate_word_frequencies(text: str) -> Dict[str, int]:
    """Calculate frequency of words in text (excluding stopwords)"""
    # Clean text and get word frequencies
    text = re.sub(r'\s+', ' ', text.lower().strip())
    words = word_tokenize(text)
    # Filter out stopwords and non-alphabetic words
    filtered_words = [word for word in words if word not in STOPWORDS and word.isalpha()]
    return Counter(filtered_words)

def _rank_sentences(sentences: List[str], word_frequencies: Dict[str, int]) -> List[tuple]:
    """Rank sentences based on word frequency scores"""
    sentence_scores = []
    
    # Process each sentence
    for sentence in sentences:
        score = 0
        word_count = 0
        words = word_tokenize(_preprocess_text(sentence))
        
        for word in words:
            if word in word_frequencies:
                word_count += 1
                score += word_frequencies[word]
        
        # Avoid division by zero
        if word_count > 0:
            sentence_scores.append((sentence, score / word_count))
        else:
            sentence_scores.append((sentence, 0.0))
            
    return sentence_scores

def summarize_text(text: str, ratio: float = 0.3) -> str:
    """
    Generate a text summary using basic NLP techniques.
    
    Args:
        text: Input text to summarize
        ratio: Ratio of sentences to keep (0.0 to 1.0)
        
    Returns:
        Summarized text
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
    
    if not 0.0 <= ratio <= 1.0:
        raise ValueError("Ratio must be between 0.0 and 1.0")
    
    if not text.strip():
        return ""

    # Preprocess text
    cleaned_text = _preprocess_text(text)
    
    if len(cleaned_text.split()) < 50:
        return cleaned_text

    # Tokenize into sentences
    try:
        sentences = sent_tokenize(cleaned_text)
    except Exception:
        # Fallback if sent_tokenize fails
        return cleaned_text[:int(len(cleaned_text) * ratio))
    
    if len(sentences) <= 1:
        return cleaned_text

def summarize_text(text: str, ratio: float = 0.3) -> str:
    """
    Generate a text summary using basic NLP techniques.
    
    Args:
        text: Input text to summarize
        ratio: Ratio of sentences to keep (0.0 to 1.0)
        
    Returns:
        Summarized text
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
    
    if not 0.0 <= ratio <= 1.0:
        raise ValueError("Ratio must be between 0.0 and 1.0")
    
    if not text.strip():
        return ""

    # Preprocess text
    cleaned_text = _preprocess_text(text)
    
    if len(cleaned_text.split()) < 50:
        return cleaned_text

    # Tokenize into sentences
    try:
        sentences = sent_tokenize(cleaned_text)
    except Exception:
        # Fallback if sent_tokenize fails
        return cleaned_text[:int(len(cleaned_text) * ratio)]

    if len(sentences) <= 1:
        return cleaned_text

    # Calculate word frequencies
    word_frequencies = _calculate_word_frequencies(cleaned_text)
    
    # Rank sentences
    sentence_scores = _rank_sentences(sentences, word_frequencies)
    
    # Calculate how many sentences to keep
    num_sentences_to_keep = max(1, int(len(sentences) * ratio))
    
    # Sort sentences by score and select top ones
    sentence_scores.sort(key=lambda x: x[1], reverse=True)
    selected_sentences = sentence_scores[:num_sentences_to_keep]
    
    # Maintain original order
    selected_sentences.sort(key=lambda x: sentences.index(x[0]))
    
    # Extract sentences
    summary_sentences = [sentence for sentence, _ in selected_sentences]
    
    return ' '.join(summary_sentences)

def summarize_text(text: str, ratio: float = 0.3) -> str:
    """
    Generate a text summary using basic NLP techniques.
    
    Args:
        text: Input text to summarize
        ratio: Ratio of sentences to keep (0.0 to 1.0)
        
    Returns:
        Summarized text
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
    
    if not 0.0 <= ratio <= 1.0:
        raise ValueError("Ratio must be between 0.0 and .0")
    
    if not text.strip():
        return ""

    # Preprocess text
    cleaned_text = _preprocess_text(text)
    
    if len(cleaned_text.split()) < 50:
        return ""

    # Tokenize into sentences
    try:
        sentences = sent_tokenize(cleaned_text)
    except:
        # Fallback if sent_tokenize fails
        return ""

    if len(sentences) <= 1:
        return ""

    # Calculate word frequencies
    word_frequencies = _calculate_word_frequencies(cleaned_text)
    
    # Rank sentences
    sentence_scores = _rank_sentences(sentences, word_frequencies)
    
    # Calculate how many sentences to keep
    num_sentences_to_keep = max(1, int(len(sentences) * ratio))
    
    # Sort sentences by score and select top ones
    sentence_scores = _rank_sentences(sentences, word_frequencies)
    
    # Maintain original order
    selected_sentences = sentence_scores[:num_sentences_to (sentence, score) in selected_sentences]
    
    # Extract sentences
    summary_sentences = [sentence for sentence, _ in selected_sentences]
    
    return ' '.join(summary_sentences)