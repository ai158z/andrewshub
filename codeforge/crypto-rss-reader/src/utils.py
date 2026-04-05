import re
from datetime import datetime
from typing import Dict, List
import os


def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace, fixing encoding issues, and standardizing format."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Remove extra whitespace and normalize spaces
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove unicode replacement characters and other problematic unicode
    text = text.replace('\ufffd', '')
    
    # Ensure proper encoding handling
    try:
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
    except UnicodeError:
        pass
    
    return text


def parse_date(date_str: str) -> datetime:
    """Parse a date string into a datetime object, supporting multiple common formats."""
    if not isinstance(date_str, str):
        raise TypeError("Date must be a string")
    
    if not date_str:
        raise ValueError("Date string cannot be empty")
    
    # Common date formats to try
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",  # RFC 2822 format
        "%Y-%m-%dT%H:%M:%S%z",       # ISO format with timezone
        "%Y-%m-%dT%H:%M:%S",         # ISO format without timezone
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d %b %Y %H:%M:%S",
        "%d %b %Y",
        "%B %d, %Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S.%f"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date string: {date_str}")


def is_valid_date(date_str: str) -> bool:
    """Check if a string is a valid date."""
    if not date_str:
        return False
    
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_str)) or bool(re.match(r'^\d{4}/\d{2}/\d{2}$', date_str))


def is_valid_crypto_symbol(symbol: str) -> bool:
    """Check if a string is a valid cryptocurrency symbol."""
    if not symbol:
        return False
    
    # Common crypto symbols (add more as needed)
    crypto_symbols = {
        'BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'ADA', 'DOGE', 'DOT', 'UNI', 'LINK',
        'XLM', 'USDT', 'USDC', 'SOL', 'MATIC', 'AVAX', 'ALGO', 'ATOM', 'FIL',
        'TRX', 'XMR', 'VET', 'ICP', 'THETA', 'FTT', 'HBAR', 'EOS', 'AAVE'
    }
    
    return symbol.upper() in crypto_symbols


def extract_crypto_symbols(text: str) -> List[str]:
    """Extract cryptocurrency symbols from text."""
    if not text:
        return []
    
    found_symbols = []
    # Standard crypto symbols pattern
    pattern = r'\b([A-Z]{2,6})\b'
    matches = re.findall(pattern, text, re.IGNORECASE)
    found_symbols.extend([match.upper() for match in matches if isinstance(match, str)])
    
    # Filter only valid crypto symbols
    valid_symbols = []
    for symbol in found_symbols:
        if is_valid_crypto_symbol(symbol):
            valid_symbols.append(symbol)
    
    return list(set(valid_symbols))  # Remove duplicates


def format_article_summary(article: Dict) -> str:
    """Format an article dictionary into a summary string."""
    if not article:
        return ""
    
    title = article.get('title', 'No title')
    description = article.get('summary', '')[:100] + "..." if len(article.get('summary', '')) > 100 else article.get('summary', '')
    date = article.get('published', 'Unknown date')
    
    return f"Title: {title}\nDate: {date}\nSummary: {description}"


def get_env_variable(key: str, default: str = None) -> str:
    """Get environment variable with optional default."""
    return os.environ.get(key, default)


def validate_url(url: str) -> bool:
    """Basic URL validation."""
    if not url or not isinstance(url, str):
        return False
    
    return url.startswith(('http://', 'https://')) and '.' in url


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection."""
    if not text:
        return ""

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    return sanitized.strip()


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to a maximum length with ellipsis."""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    # Try to split at word boundary
    if max_length < len("..."):
        return text[:max_length] + "..."
    
    truncated = text[:max_length]
    # Try to find the last space to avoid cutting words
    last_space = truncated.rfind(' ')
    if last_space != -1:
        return truncated[:last_space] + '...'
    else:
        return truncated + '...'