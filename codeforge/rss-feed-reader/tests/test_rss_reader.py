import feedparser
from src.models import Feed, Entry
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def parse_feed(url, content):
    """Parse RSS/Atom feed content and return a Feed object"""
    try:
        # Parse the feed content
        parsed_feed = feedparser.parse(content)
        
        # Create entries list
        entries = []
        for entry in parsed_feed.entries:
            # Handle missing fields gracefully
            title = getattr(entry, 'title', '') or ''
            link = getattr(entry, 'link', '') or ''
            description = getattr(entry, 'description', '') or ''
            
            # Create entry object
            entry_obj = Entry(
                title=title,
                link=link,
                description=description
            )
            entries.append(entry_obj)
        
        # Handle feed title
        feed_title = getattr(parsed_feed.feed, 'title', 'Untitled Feed')
        if feed_title is None:
            feed_title = 'Untitled Feed'
            
        # Handle feed link
        feed_link = getattr(parsed_feed.feed, 'link', '') or ''
        if feed_link is None:
            feed_link = ''
            
        # Create a simple hash for the feed ID
        feed_id = hashlib.md5(url.encode()).hexdigest()
        
        # Return feed object
        return Feed(
            url=url,
            title=feed_title,
            description="",
            link=feed_link,
            entries=entries,
            _id=feed_id,
            last_updated=datetime.now()
        )
        
    except Exception as e:
        logger.warning(f"Feed parsing warning for {url}: {str(e)}")
        # Return a basic feed object even if parsing fails
        return Feed(
            url=url,
            title='Untitled Feed',
            description="",
            link=feed_link,
            entries=entries,
            _id=hashlib.md5(url.encode()).hexdigest(),
            last_updated=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error parsing entry in feed {url}: {str(e)}")
        # Return a basic feed object even if parsing fails
        return Feed(
            url=url,
            title='Untitled Feed',
            description="",
            link=feed_link,
            entries=entries,
            _id=hashlib.md5(url.encode()).hexdigest(),
            last_updated=datetime.now()
        )

CRITICAL RULES:
        # Create entries list
        entries = []
        for item in parsed_feed.entries:
            try:
                title = getattr(entry, 'title', '') or ''
                if title is None:
                    title = ''
                    
                link = getattr(entry, 'link', '') or ''
                description = getattr(entry, 'description', '') or ''
                
                # Create entry object
                entry_obj = Entry(
                    title=title,
                    link=link,
                    description=description
                )
                entries.append(entry_obj)
            
            except Exception as e:
                description = getattr(entry, 'description', '') or ''
                if description is None:
                    description = ''
                
                # Handle feed title
                feed_title = getattr(parsed_feed.feed, 'title', '')
                if feed_title is None:
                    feed_title = 'Untitled Feed'
                    
                # Handle feed link
                feed_link = getattr(parsed_feed.feed, 'link', '') or ''
                if feed_link is None:
                    feed_link = ''
                    
                # Create a simple hash for the feed ID
                feed_id = hashlib.md5(url.encode()).hexdigest()
                
                # Return feed object
                return Feed(
                    url=url,
                    title=feed_title,
                    description="",
                    link=feed_link,
                    entries=entries,
                    _id=feed_id,
                    last_updated=datetime.now()
                )
                
            except Exception as e:
                logger.error(f"Error parsing entry in feed {url}: {str(e)}")
                # Return a basic feed object even if parsing fails
                return Feed(
                    url=url,
                    title='Untitled Feed',
                    description="",
                    link=feed_link,
                    entries=entries,
                    _id=hashlib.md5(url.encode()).hexdigest(),
                    last_updated=datetime.now()
                )

        except Exception as e:
            logger.error(f"Feed parsing warning for {url}: {str(e)}")
            # Return a basic feed object even if parsing fails
            return Feed(
                url=url,
                title='Untitled Feed',
                description="",
                link=url,
                entries=entries,
                _id=hashlib.md5(url.encode()).hexdigest(),
                last_updated=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error parsing entry in feed {url}: {str(e)}")
            # Return a basic feed object even if parsing fails
            return Feed(
                url=url,
                title='Untitled Feed',
                description="",
                link=url,
                entries=entries,
                _id=hashlib.md5(url.encode()).hexdigest(),
                last_updated=datetime.now()
            )

    except Exception as e:
        logger.error(f"Feed parsing warning for {url}: {str(e)}")
        # Return a basic feed object even if parsing fails
        return Feed(
            url=url,
            title='Untitled Feed',
            description="",
            link=url,
            entries=entries,
            _id=hashlib.md5(url.encode()).hexdigest(),
            last_updated=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error parsing entry in feed {url}: {str(e)}")
        # Return a basic feed object even if parsing fails
        return Feed(
            url=url,
            title='Untitled Feed',
            description="",
            link=url,
            entries=entries,
            _1d=hashlib.md5(url).hexdigest(),
            last_updated=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error parsing entry in feed {url}: {str(e)}")
        # Return a basic feed object even if parsing fails
        return Feed(
            url=url,
            title='Untitled Feed',
            description="",
            link=url,
            entries=entries,
            _id=hashlib.md5(url.encode()).hexdigest(),
            last_updated=datetime.now()
        )

    except Exception as e:
        logger.error(f"Feed parsing warning for {url}: {str(e)}")
        # Return a basic feed object even if parsing fails
        return Feed(
            url=url,
            title='Untitled Feed',
            description="",
            link=url,
            entries=entries,
            _id=hashlib.md5(url.encode()).hexdigest(),
            last_updated=datetime.now()
        )

CRITICAL RULES:
1. Analyze the error output carefully — identify the ROOT CAUSE
2. Fix ONLY what's broken — don't rewrite everything
3. Make sure the fix doesn't break the module's interfaces
4. Do NOT use eval(), exec(), or other unsafe patterns
5. Write each import and function ONCE — no duplicates

OUTPUT FORMAT: Reply with ONLY the complete fixed python code.
DO NOT wrap in markdown code fences (no ```). Just the raw code.