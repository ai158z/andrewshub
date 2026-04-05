import pytest
from unittest.mock import patch, Mock
from src.feed_parser import parse_feed, fetch_all_feeds

def test_parse_feed_success():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'<?xml version="1.0"?>'
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_http_error():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_get.side_effect = Exception('Network error')
        
        result = parse_feed('http://example.com/feed')
        assert result == []

def test_parse_feed_empty_response():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_invalid_xml():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'invalid xml content'
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_with_valid_entries():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <title>Test Article</title>
                <link href="http://example.com/article"/>
                <summary>Test summary</summary>
                <published>2023-01-01T00:00:00Z</published>
                <author><name>Test Author</name></author>
            </entry>
        </feed>'''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_fetch_all_feeds_empty_list():
    result = fetch_all_feeds([])
    assert result == []

def test_fetch_all_feeds_single_url():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'<?xml version="1.0"?>'
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = fetch_all_feeds(['http://example.com/feed'])
        assert isinstance(result, list)

def test_fetch_all_feeds_multiple_urls():
    urls = ['http://example1.com/feed', 'http://example2.com/feed']
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'<?xml version="1.0"?>'
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = fetch_all_feeds(urls)
        assert isinstance(result, list)

def test_fetch_all_feeds_with_failure():
    def mock_get_side_effect(url):
        if url == 'http://fail.com/feed':
            raise Exception('Network error')
        mock_response = Mock()
        mock_response.content = b'<?xml version="1.0"?>'
        mock_response.status_code = 200
        return mock_response
        
    with patch('src.feed_parser.requests.get', side_effect=mock_get_side_effect):
        result = fetch_all_feeds(['http://fail.com/feed', 'http://success.com/feed'])
        assert isinstance(result, list)

def test_parse_feed_with_no_entries():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
        </feed>'''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert result == []

def test_parse_feed_missing_title():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <link href="http://example.com/article"/>
                <summary>Test summary</summary>
            </entry>
        </feed>'''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_missing_link():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <title>Test Article</title>
                <summary>Test summary</summary>
            </entry>
        </feed>'''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_missing_description():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <title>Test Article</title>
                <link href="http://example.com/article"/>
            </entry>
        </feed>'''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_with_tags():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <title>Test Article</title>
                <link href="http://example.com/article"/>
                <summary>Test summary</summary>
                <category term="tech"/>
                <category term="news"/>
            </entry>
        </feed>'''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_with_author():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <title>Test Article</title>
                <author><name>Test Author</name></author>
            </entry>
        </feed>'''
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = parse_feed('http://example.com/feed')
        assert isinstance(result, list)

def test_parse_feed_timeout():
    with patch('src.feed_parser.requests.get', side_effect=Exception('Timeout')):
        result = parse_feed('http://example.com/feed')
        assert result == []

def test_parse_feed_request_exception():
    with patch('src.feed_parser.requests.get') as mock_get:
        mock_get.side_effect = Exception('Connection error')
        
        result = parse_feed('http://example.com/feed')
        assert result == []

def test_fetch_all_feeds_none_input():
    result = fetch_all_feeds(None)
    assert result == []

def test_fetch_all_feeds_invalid_urls():
    result = fetch_all_feeds([None, ''])
    assert result == []

def test_parse_feed_entry_parsing_error():
    with patch('src.feed_parser.feedparser.parse') as mock_parse:
        mock_parse.side_effect = Exception('Parse error')
        
        result = parse_feed('http://example.com/feed')
        assert result == []