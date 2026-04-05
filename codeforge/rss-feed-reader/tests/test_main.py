import pytest
from unittest.mock import patch, MagicMock
from src.main import main, parse_feed
from src.models import Feed

def test_main_with_valid_url():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed') as mock_fetch:
            with patch('src.main.parse_feed') as mock_parse:
                with patch('src.main.summarize_text') as mock_summarize:
                    with patch('src.main.click.echo') as mock_echo:
                        mock_fetch.return_value = '<xml>test</xml>'
                        mock_parse.return_value = Feed(entries=[])
                        mock_summarize.return_value = 'Summary text'
                        main('http://valid.com', 10, 0.3)
                        mock_echo.assert_called_with('Summary text')

def test_main_with_invalid_url():
    with patch('src.main.is_valid_url', return_value=False):
        with patch('src.main.click.echo') as mock_echo:
            main('invalid-url', 10, 0.3)
            mock_echo.assert_called_with('Invalid URL provided.')

def test_main_with_fetch_exception():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed', side_effect=Exception('Network error')):
            with patch('src.main.click.echo') as mock_echo:
                main('http://valid.com', 10, 0.3)
                mock_echo.assert_called_with('Error: Network error')

def test_parse_feed_success():
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Test Title</title>
<description>Test Description</description>
<link>http://test.com</link>
</item>
</channel>
</rss>'''
    
    feed = parse_feed('http://test.com', content)
    assert feed is not None
    assert len(feed.entries) == 1

def test_parse_feed_invalid_content():
    feed = parse_feed('http://test.com', 'invalid xml')
    assert feed is None

def test_parse_feed_with_empty_content():
    feed = parse_feed('http://test.com', '')
    assert feed is None

def test_parse_feed_with_malformed_xml():
    content = '<?xml version="1.0" encoding="UTF-8"?><invalid>'
    feed = parse_feed('http://test.com', content)
    assert feed is None

def test_main_with_no_entries():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed') as mock_fetch:
            with patch('src.main.parse_feed') as mock_parse:
                with patch('src.main.summarize_text') as mock_summarize:
                    with patch('src.main.click.echo') as mock_echo:
                        mock_fetch.return_value = '<xml></xml>'
                        mock_parse.return_value = Feed(entries=[])
                        mock_summarize.return_value = 'No content summary'
                        main('http://valid.com', 10, 0.3)
                        mock_echo.assert_called_with('No content summary')

def test_main_with_timeout_parameter():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed') as mock_fetch:
            with patch('src.main.parse_feed'):
                with patch('src.main.summarize_text'):
                    with patch('src.main.click.echo'):
                        main('http://valid.com', 30, 0.3)
                        mock_fetch.assert_called_with('http://valid.com', 30)

def test_main_with_zero_timeout():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed') as mock_fetch:
            with patch('src.main.parse_feed'):
                with patch('src.main.summarify_text'):
                    with patch('src.main.click.echo'):
                        main('http://valid.com', 0, 0.3)
                        mock_fetch.assert_called_with('http://valid.com', 0)

def test_main_with_negative_timeout():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed') as mock_fetch:
            with patch('src.main.parse_feed'):
                with patch('src.main.summarize_text'):
                    with patch('src.main.click.echo'):
                        main('http://valid.com', -5, 0.3)
                        mock_fetch.assert_called_with('http://valid.com', -5)

def test_main_with_ratio_zero():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed'):
            with patch('src.main.parse_feed'):
                with patch('src.main.summarize_text') as mock_summarize:
                    with patch('src.main.click.echo'):
                        main('http://valid.com', 10, 0.0)
                        mock_summarize.assert_called_with('', 0.0)

def test_main_with_ratio_one():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed'):
            with patch('src.main.parse_feed'):
                with patch('src.main.summarize_text') as mock_summarize:
                    with patch('src.main.click.echo'):
                        main('http://valid.com', 10, 1.0)
                        mock_summarize.assert_called_with('', 1.0)

def test_main_with_ratio_greater_than_one():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed'):
            with patch('src.main.parse_feed'):
                with patch('src.main.summarize_text') as mock_summarize:
                    with patch('src.main.click.echo'):
                        main('http://valid.com', 10, 1.5)
                        mock_summarize.assert_called_with('', 1.5)

def test_main_with_ratio_negative():
    with patch('src.main.is_valid_url', return_value=True):
        with patch('src.main.fetch_feed'):
            with patch('src.main.parse_feed'):
                with patch('src.main.summarize_text') as mock_summarize:
                    with patch('src.main.click.echo'):
                        main('http://valid.com', 10, -0.5)
                        mock_summarize.assert_called_with('', -0.5)

def test_parse_feed_with_cdata():
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title><![CDATA[Test Title]]></title>
<description><![CDATA[Test Description]]></description>
<link>http://test.com</link>
</item>
</channel>
</rss>'''
    
    feed = parse_feed('http://test.com', content)
    assert feed is not None
    assert len(feed.entries) == 1
    assert feed.entries[0]['title'] == 'Test Title'

def test_parse_feed_with_namespaces():
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://search.yahoo.com/mrss/" version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Test Title</title>
<description>Test Description</description>
<link>http://test.com</link>
<dc:creator>Author</dc:creator>
</item>
</channel>
</rss>'''
    
    feed = parse_feed('http://test.com', content)
    assert feed is not None
    assert len(feed.entries) == 1

def test_parse_feed_with_multiple_items():
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
<item>
<title>Item 1</title>
<description>Description 1</description>
<link>http://test1.com</link>
</item>
<item>
<title>Item 2</title>
<description>Description 2</description>
<link>http://test2.com</link>
</item>
</channel>
</rss>'''
    
    feed = parse_feed('http://test.com', content)
    assert feed is not None
    assert len(feed.entries) == 2
    assert feed.entries[0]['title'] == 'Item 1'
    assert feed.entries[1]['title'] == 'Item 2'

def test_parse_feed_with_missing_fields():
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<item>
</item>
</channel>
</rss>'''
    
    feed = parse_feed('http://test.com', content)
    assert feed is not None
    assert len(feed.entries) == 1
    assert feed.entries[0]['title'] is None
    assert feed.entries[0]['description'] is None
    assert feed.entries[0]['link'] is None

def test_parse_feed_with_no_items():
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Test Feed</title>
</channel>
</rss>'''
    
    feed = parse_feed('http://test.com', content)
    assert feed is not None
    assert len(feed.entries) == 0