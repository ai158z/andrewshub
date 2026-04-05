from unittest.mock import patch, Mock
from src.rss_parser import parse_feed
from src.models import Feed, Entry
import pytest

def test_parse_feed_valid_rss():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<description>Test Description</description>
<link>http://example.com</link>
<item>
<title>Test Entry</title>
<description>Test content</description>
<pubDate>Mon, 01 Jan 2023 00:00:00 +0000</pubDate>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    
    assert isinstance(result, Feed)
    assert result.title == "Test Feed"
    assert len(result.entries) == 1
    assert isinstance(result.entries[0], Entry)
    assert result.entries[0].title == "Test Entry"

def test_parse_feed_with_empty_content():
    url = "http://example.com/feed"
    content = ""
    
    with pytest.raises(ValueError):
        parse_feed(url, content)

def test_parse_feed_with_malformed_xml():
    url = "http://example.com/feed"
    content = "<?xml version='1.0'?><invalid>"
    
    with pytest.raises(ValueError):
        parse_feed(url, content)

def test_parse_feed_no_entries():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Empty Feed</title>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert isinstance(result, Feed)
    assert len(result.entries) == 0

def test_parse_feed_entry_fallback_title():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<description>Entry with no title</description>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].title == "No Title"

def test_parse_feed_entry_content_fallbacks():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
<summary>Summary content</title>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    entry = result.entries[0]
    assert entry.content == "Summary content"

def test_parse_feed_entry_no_content():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].content == ""

def test_parse_feed_entry_link_fallback():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<link>http://example.com</link>
<item>
<title>Test Entry</title>
<description>Test content</description>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].link == "http://example.com"

def test_parse_feed_entry_link_from_enclosure():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
<description>Entry content</description>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    # Should fallback to feed URL when no link in entry
    assert result.entries[0].link == url

def test_parse_feed_entry_with_tags():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Tagged Entry</title>
<description>Content</description>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    entry = result.entries[0]
    assert entry.tags == []

def test_parse_feed_entry_with_published_date():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry with Date</title>
<description>Content</description>
<pubDate>Mon, 01 Jan 2023 00:00:00 +0000</pubDate>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].published is not None

def test_parse_feed_entry_with_updated_date_fallback():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
<description>Content</description>
<updated>Mon, 01 Jan 2023 00:00:00 +0000</updated>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].published is not None

def test_parse_feed_entry_no_date():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].published is None

def test_parse_feed_entry_author():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
<author>Test Author</author>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].author == "Test Author"

def test_parse_feed_entry_no_author():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].author == ""

def test_parse_feed_entry_summary():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
<summary>Test summary</summary>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].summary == "Test summary"

def test_parse_feed_entry_no_summary():
    url = "http://example.com/feed"
    content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, content)
    assert result.entries[0].summary == ""

def test_parse_feed_entry_with_content_sanitization():
    url = "http://example.com/feed"
    malicious_content = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Entry Title</title>
<description>&lt;script&gt;alert('xss')&lt;/script&gt;Test content</description>
</item>
</channel>
</rss>"""
    
    result = parse_feed(url, malicious_content)
    # Content should be sanitized (script tag removed)
    assert "<script>" not in result.entries[0].content

def test_parse_feed_with_bozo_exception_logged():
    url = "http://example.com/feed"
    content = "invalid xml content"
    
    with patch('src.rss_parser.logger') as mock_logger:
        with pytest.raises(ValueError):
            parse_feed(url, content)
        mock_logger.error.assert_called()
        mock_logger.warning.assert_called()

def test_parse_feed_fallback_to_feed_url():
    url = "http://example.com/feed"
    content = "invalid"
    
    with patch('src.rss_parser.logger'):
        with pytest.raises(ValueError):
            parse_feed(url, content)