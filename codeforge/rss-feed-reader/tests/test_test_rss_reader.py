import pytest
from unittest.mock import patch
from src.rss_parser import parse_feed
from src.models import Feed


def test_parse_rss_feed_invalid_content():
    """Test parsing with invalid XML content"""
    with pytest.raises(Exception):
        parse_feed("http://example.com", "invalid xml content")


def test_parse_rss_feed_missing_title():
    """Test RSS feed parsing when title is missing"""
    rss_content = '''<rss version="2.0">
        <channel>
            <link>http://example.com</link>
            <item>
                <title>Test Article</title>
                <link>http://example.com/article</link>
                <description>Test description</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert feed.title == ""
    assert feed.link == "http://example.com"


def test_parse_rss_feed_missing_link():
    """Test RSS feed parsing when link is missing"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <item>
                <title>Test Article</title>
                <link>http://example.com/article</link>
                <description>Test description</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert feed.title == "Test Feed"
    assert feed.link == ""


def test_parse_rss_feed_empty_entries():
    """Test RSS feed with no entries"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert feed.title == "Test Feed"
    assert feed.link == "http://example.com"
    assert len(feed.entries) == 0


def test_parse_rss_feed_entry_missing_description():
    """Test RSS feed entry with missing description"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Test Article</title>
                <link>http://example.com/article</link>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 1
    assert feed.entries[0].title == "Test Article"
    assert feed.entries[0].link == "http://example.com/article"
    assert feed.entries[0].description == ""


def test_parse_rss_feed_entry_missing_title():
    """Test RSS feed entry with missing title"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <link>http://example.com/article</link>
                <description>Test description</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 1
    assert feed.entries[0].title == ""
    assert feed.entries[0].description == "Test description"


def test_parse_rss_feed_entry_missing_link():
    """Test RSS feed entry with missing link"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Test Article</title>
                <description>Test description</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 1
    assert feed.entries[0].title == "Test Article"
    assert feed.entries[0].link == ""


def test_parse_rss_feed_multiple_entries():
    """Test RSS feed with multiple entries"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>First Article</title>
                <link>http://example.com/article1</link>
                <description>First description</description>
            </item>
            <item>
                <title>Second Article</title>
                <link>http://example.com/article2</link>
                <description>Second description</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 2
    assert feed.entries[0].title == "First Article"
    assert feed.entries[1].title == "Second Article"


def test_parse_rss_feed_cdata_content():
    """Test RSS feed with CDATA content"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>CDATA Article</title>
                <link>http://example.com/article</link>
                <description><![CDATA[This is <b>CDATA</b> content]]></description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert "CDATA" in feed.entries[0].description


def test_parse_rss_feed_html_entities():
    """Test RSS feed with HTML entities"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Article &amp; Title</title>
                <link>http://example.com/article</link>
                <description>Article &lt;content&gt;</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert feed.entries[0].title == "Article & Title"
    assert "&lt;" in feed.entries[0].description


def test_parse_rss_feed_empty():
    """Test parsing of completely empty RSS content"""
    with pytest.raises(Exception):
        parse_feed("http://example.com", "")


def test_parse_rss_feed_malformed_xml():
    """Test parsing of malformed XML"""
    malformed_rss = "<rss><channel><title>Test</title></channel></rss>"
    with pytest.raises(Exception):
        parse_feed("http://example.com", malformed_rss)


def test_parse_rss_feed_no_channel():
    """Test parsing RSS without channel element"""
    rss_content = "<rss version='2.0'></rss>"
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 0


def test_parse_rss_feed_no_items():
    """Test parsing RSS with channel but no items"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 0


def test_parse_rss_feed_special_characters():
    """Test RSS feed with special characters in content"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Special chars: &amp; &lt; &gt; " '</title>
                <link>http://example.com/article</link>
                <description>Special chars: &amp; &lt; &gt; " '</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert "Special chars:" in feed.entries[0].title
    assert "&" in feed.entries[0].description


def test_parse_rss_feed_unicode():
    """Test RSS feed with unicode characters"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Unicode: café naïve résumé</title>
                <link>http://example.com/article</link>
                <description>Unicode content: café naïve résumé</description>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert "café naïve résumé" in feed.entries[0].title


def test_parse_rss_feed_namespaced():
    """Test RSS feed with XML namespaces"""
    rss_content = '''<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
        <channel>
            <title>Test Namespaced Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Namespaced Item</title>
                <link>http://example.com/article</link>
                <description>Namespaced content</description>
                <content:encoded>Full content</content:encoded>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    # Should parse successfully, ignoring unknown namespaces
    assert feed.title == "Test Namespaced Feed"


def test_parse_rss_feed_with_category():
    """Test RSS feed with category elements"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Article with Category</title>
                <link>http://example.com/article</link>
                <description>Test description</description>
                <category>Technology</category>
                <category>News</category>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 1
    assert feed.entries[0].title == "Article with Category"


def test_parse_rss_feed_with_pubdate():
    """Test RSS feed with publication dates"""
    rss_content = '''<rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <link>http://example.com</link>
            <item>
                <title>Article with Date</title>
                <link>http://example.com/article</link>
                <description>Test description</description>
                <pubDate>Mon, 01 Jan 2024 00:00:00 +0000</pubDate>
            </item>
        </channel>
    </rss>'''
    
    feed = parse_feed("http://example.com", rss_content)
    assert isinstance(feed, Feed)
    assert len(feed.entries) == 1
    assert feed.entries[0].title == "Article with Date"