import pytest
from typing import Dict, List, Any
from src.models import Feed, Entry
import requests
import os

@pytest.fixture
def sample_rss_content() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Test RSS Feed</title>
    <link>http://example.com</link>
    <description>Test RSS Feed Description</description>
    <item>
        <title>Test Entry 1</title>
        <description>Test Entry Description</description>
        <link>http://example.com/test</link>
        <pubDate>Wed, 21 Nov 2023 10:00:00 +0000</pubDate>
    </item>
    <item>
        <title>Test Entry 2</title>
        <description>Another Test Entry Description</description>
        <link>http://example.com/test2</link>
        <pubDate>Wed, 21 Nov 2023 11:00:00 +0000</pubDate>
    </item>
</channel>
</rss>"""

@pytest.fixture
def sample_feed_data() -> Dict[str, Any]:
    return {
        'title': 'Test Feed',
        'description': 'A test feed',
        'link': 'http://example.com/test-feed',
        'entries': [
            {
                'title': 'Test Entry 1',
                'link': 'https://example.com/test1',
                'description': 'Test entry 1 description',
                'date': '2023-01-01'
            },
            {
                'title': 'Test Entry 2',
                'link': 'https://example.com/test2',
                'description': 'Test entry 2 description',
                'date': '2023-01-02'
            }
        ]
    }

@pytest.fixture
def sample_entries() -> Dict[str, str]:
    return {
        'title': 'Test Entry 1',
        'link': 'https://example.com/test',
        'description': 'Test entry 1 description',
        'date': '2023-01-01'
    }