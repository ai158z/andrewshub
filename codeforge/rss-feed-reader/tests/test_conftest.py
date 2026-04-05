import pytest
from datetime import datetime
from src.models import Feed, Entry

def test_sample_rss_content_fixture(sample_rss_content):
    # Verify the sample RSS content is valid
    assert sample_rss_content is not None
    assert isinstance(sample_rss_content, str)
    assert len(sample_rss_content) > 0

def test_sample_feed_data_fixture(sample_feed_data):
    # Test the sample feed data structure
    expected_keys = {'title', 'description', 'link', 'entries'}
    expected_entry_keys = {'title', 'link', 'description', 'date'}
    
    # Validate structure
    assert isinstance(sample_feed_data, dict)
    assert set(sample_feed_data.keys()) == expected_keys
    
    # Check entries structure
    for entry in sample_feed_data['entries']:
        assert isinstance(entry, dict)
        assert set(entry.keys()) == expected_entry_keys
        
    assert sample_feed_data['title'] is not None
    assert sample_feed_data['description'] is not None

def test_sample_rss_content_has_correct_structure(sample_rss_content):
    # Verify that sample content has valid RSS structure
    content = sample_rss_content
    assert '<rss' in content
    assert '<channel>' in content
    assert '<item>' in content
    assert '<title>Test Entry 1</title>' in content
    assert 'pubDate' in content

def test_sample_feed_with_various_fields(sample_feed_data):
    # Test feed with sample data
    feed = sample_feed_data
    assert feed['title'] == 'Test Feed'
    assert feed['description'] == 'A test feed'

def test_entries_structure(sample_entries):
    # Test that entries have the right structure
    expected_fields = ['title', 'link', 'description', 'date']
    for field in expected_fields:
        assert field in sample_entries

def test_valid_rss_structure(sample_rss_content):
    # Test that the RSS content has the correct structure
    assert '<?xml version="1.0" encoding="UTF-8"?>' in sample_rss_content
    assert '<rss version="2.0">' in sample_rss_content
    assert '<channel>' in sample_rss_content
    assert '</item>' in sample_rss_content

def test_feed_data_structure(sample_feed_data):
    # Test the structure of sample feed data
    assert isinstance(sample_feed_data, dict)
    expected_keys = {'title', 'description', 'link', 'entries'}
    assert set(sample_feed_data.keys()) == expected_keys

def test_rss_content_and_feed_data_structure(sample_rss_content, sample_feed_data):
    # Test the structure of the content and the data
    assert sample_rss_content is not None
    assert sample_feed_data is not None
    assert isinstance(sample_rss_content, str)
    assert len(sample_rss_content) > 0
    assert isinstance(sample_feed_data, dict)
    assert 'title' in sample_feed_data
    assert 'description' in sample_feed_data
    assert len(sample_feed_data) > 0

def test_sample_entries():
    # Test sample entries structure
    sample_entries = {
        'title': 'Test Entry 1',
        'link': 'https://example.com/test',
        'description': 'Test entry 1 description',
        'date': '2023-01-01'
    }
    
    expected_fields = ['title', 'link', 'description', 'date']
    for field in expected_fields:
        assert field in sample_entries
        assert sample_entries[field] is not None

def test_edge_case_empty_rss_content():
    # Test with empty content should not raise an error in fixture setup
    empty_content = ""
    assert isinstance(empty_content, str)

def test_sample_feed_entries_structure(sample_feed_data):
    # Test entries structure in sample data
    assert 'entries' in sample_feed_data
    assert isinstance(sample_feed_data['entries'], list)
    assert len(sample_feed_data['entries']) > 0
    
    # Check first entry structure
    first_entry = sample_feed_data['entries'][0]
    assert 'title' in first_entry
    assert 'link' in first_entry
    assert 'description' in first_entry
    assert 'date' in first_entry