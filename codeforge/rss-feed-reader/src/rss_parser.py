import feedparser
from typing import List
from src.models import Feed, Entry
from src.utils import sanitize_text
import logging

logger = logging.getLogger(__name__)

def parse_feed(url: str, content: str) -> Feed:
    """
    Parse RSS, Atom, or RDF feed content into a standardized Feed model.
    
    Args:
        url: The URL of the feed
        content: Raw feed content as string
        
    Returns:
        Feed: Parsed feed object with entries
        
    Raises:
        ValueError: If feed parsing fails
    """
    try:
        # Parse the feed content using feedparser
        parsed = feedparser.parse(content)
        
        if parsed.get('bozo') and parsed.get('bozo_exception'):
            logger.warning(f"Feed parsing warning for {url}: {parsed.bozo_exception}")
            
        # Extract feed metadata
        feed_title = parsed.feed.get('title', 'Untitled Feed')
        feed_description = parsed.feed.get('description', '')
        feed_link = parsed.feed.get('link', url)
        
        # Parse entries
        entries: List[Entry] = []
        for entry in parsed.entries:
            try:
                # Extract title (with fallbacks)
                title = getattr(entry, 'title', 'No Title')
                if not title or not title.strip():
                    title = 'No Title'
                
                # Extract content (try multiple possible fields)
                content_text = (
                    getattr(entry, 'content', [{}])[0].get('value', '') or
                    getattr(entry, 'summary', '') or
                    getattr(entry, 'description', '')
                )
                content_text = sanitize_text(content_text)
                
                # Extract publication date
                published = getattr(entry, 'published', None)
                if not published:
                    published = getattr(entry, 'updated', None)
                
                # Extract link (with multiple fallbacks)
                link = getattr(entry, 'link', None)
                if not link:
                    # Try to find link in enclosure or other fields
                    if hasattr(entry, 'enclosures') and entry.enclosures:
                        link = entry.enclosures[0].get('href') if entry.enclosures else None
                    if not link:
                        link = url  # Fallback to feed URL
                
                # Create Entry object
                entry_obj = Entry(
                    title=title,
                    content=content_text,
                    link=link or '',
                    published=published,
                    summary=getattr(entry, 'summary', ''),
                    author=getattr(entry, 'author', ''),
                    tags=[tag.term for tag in getattr(entry, 'tags', [])]
                )
                entries.append(entry_obj)
            except Exception as e:
                logger.error(f"Error parsing entry in feed {url}: {str(e)}")
                continue
        
        # Create and return Feed object
        return Feed(
            title=feed_title,
            description=feed_description,
            url=url,
            link=feed_link,
            entries=entries
        )
        
    except Exception as e:
        logger.error(f"Failed to parse feed from {url}: {str(e)}")
        raise ValueError(f"Failed to parse feed content: {str(e)}") from e