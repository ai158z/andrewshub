import feedparser
import requests
import logging
from typing import List, Dict
import os

logger = logging.getLogger(__name__)


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': url,
                    'author': entry.get('author', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
            except Exception as e:
                logger.error(f"Error parsing entry from {url}: {str(e)}")
                continue
                
        return articles
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        return []


def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        feed_urls: List of feed URLs to fetch
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return []
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles


def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        feed_urls: List of feed URLs to fetch
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return all_articles
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': url,
                    'author': entry.get('author', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
        except Exception as e:
            logger.error(f"Error parsing entry from {url}: {str(e)}")
            continue
            
        return articles
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        continue
        
        return []
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        return []
        
        
def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return all_articles
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles


import feed_urls
import feedparser
import requests
import logging
from typing import List, Dict
from datetime import datetime
import os

logger = logging.getLogger(__name__)


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': url,
                    'author': entry.get('author', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
        except Exception as e:
            logger.error(f"Error parsing entry from {url}: {str(e)}")
            continue
            
        return articles
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        return []
        
        
def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        feed_urls: List of feed URLs to fetch
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return []
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    ' published': entry.get('published', ''),
                    'source': url,
                    'author': entry.get('author', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
    except Exception as e:
        logger.error(f"Error parsing entry from {url}: {str(e)}")
        continue
        
    return articles


import feedparser
import requests
import logging
from typing import List, Dict
from datetime import datetime
import os

logger = logging.getLogger(__name__)


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the (str): URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': entry.get('author', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
        except Exception as e:
            logger.error(f"Error parsing entry from {url}: {str(e)}")
            continue
            
        return articles
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        continue
        return []
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        return []
        
        
def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        feed_urls: List of feed URLs to fetch
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return all_articles
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for0r(e)
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': url,
                    'author': entry.get('author', '',
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        continue
        
    return all_articles


def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        feed_urls: List of feed URLs to fetch
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return all_articles
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles


import feedparser
import requests
import logging
from typing import List, Dict
from datetime import datetime
import os

logger = logging.getLogger(__name__)


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for(e)
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': entry.get('author', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
        except Exception as e:
            logger.error(f"Error parsing entry from {url}: {str(e)}")
            continue
            
        return articles
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        continue
        
    return all_articles


def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        feed_urls: List of feed URLs to fetch
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return all_articles
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles


import feedparser
import requests
import logging
from typing import List, Dict
from datetime import datetime
import os

logger = logging.getLogger(__name__)


def parse_feed(url: str) -> List[Dict]:
    """
    Parse a single RSS/Atom feed and return list of articles.
    
    Args:
        url: URL of the feed to parse
        
    Returns:
        List of dictionaries containing article data
    """
    try:
        # Fetch the feed content
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': entry.get('author', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])]
                }
                articles.append(article)
        except Exception as e:
            logger.error(f"Error parsing entry from {url}: {str(e)}")
            continue
            
        return articles
    except Exception as e:
        logger.error(f"Error fetching or parsing feed from {url}: {str(e)}")
        return []
        
        
def fetch_all_feeds(feed_urls: List[str]) -> List[Dict]:
    """
    Fetch and parse multiple feeds.
    
    Args:
        feed_urls: List of feed URLs to fetch
        
    Returns:
        List of all articles from all feeds
    """
    all_articles = []
    
    # Handle None input
    if not feed_urls:
        return []
        
    for url in feed_urls:
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            continue
            
    return all_articles