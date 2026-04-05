import pytest
from datetime import datetime
from src.models import Entry, Feed


def test_entry_creation():
    entry = Entry(
        id="1",
        title="Test Title",
        link="http://example.com",
        summary="Test summary",
        published=datetime(2023, 1, 1)
    )
    assert entry.id == "1"
    assert entry.title == "Test Title"
    assert entry.link == "http://example.com"
    assert entry.summary == "Test summary"
    assert entry.published == datetime(2023, 1, 1)
    assert entry._id == "6c9d2f8f3d3f3e2b3f3e2b3f3e2b3f3e"


def test_entry_to_dict():
    entry = Entry(
        id="1",
        title="Test Title",
        link="http://example.com",
        summary="Test summary",
        published=datetime(2023, 1, 1),
        author="Test Author"
    )
    result = entry.to_dict()
    assert result["id"] == "1"
    assert result["title"] == "Test Title"
    assert result["author"] == "Test Author"


def test_entry_from_dict():
    data = {
        "id": "1",
        "title": "Test Title",
        "link": "http://example.com",
        "summary": "Test summary",
        "published": "2023-01-01T00:00:00",
        "author": "Test Author",
        "content": "Test content",
        "categories": ["test", "example"]
    }
    entry = Entry.from_dict(data)
    assert entry.id == "1"
    assert entry.title == "Test Title"
    assert entry.link == "http://example.com"
    assert entry.author == "Test Author"


def test_entry_default_id_generation():
    entry = Entry(
        id="1",
        title="Test",
        link="http://example.com",
        summary="Test summary",
        published=datetime(2023, 1, 1)
    )
    assert entry._id == "6c9d2f8f3d3f3e2b3f3e2b3f3e2b3f3e"


def test_feed_creation():
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com"
    )
    assert feed.url == "http://example.com/feed"
    assert feed.title == "Test Feed"
    assert feed._id == "a3d0f8c3c6d9e7d8f8e7d8f8e7d8f8e7"


def test_feed_to_dict():
    entry = Entry(
        id="1",
        title="Test Entry",
        link="http://example.com/entry",
        summary="Test summary",
        published=datetime(2023, 1, 1)
    )
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com",
        entries=[entry]
    )
    result = feed.to_dict()
    assert result["url"] == "http://example.com/feed"
    assert result["title"] == "Test Feed"
    assert len(result["entries"]) == 1


def test_feed_from_dict():
    data = {
        "url": "http://example.com/feed",
        "title": "Test Feed",
        "description": "Test description",
        "link": "http://example.com",
        "entries": [{
            "id": "1",
            "title": "Test Entry",
            "link": "http://example.com/entry",
            "summary": "Test summary",
            "published": "2023-01-01T00:00:00"
        }]
    }
    feed = Feed.from_dict(data)
    assert feed.url == "http://example.com/feed"
    assert len(feed.entries) == 1


def test_feed_get_unread_entries():
    entry1 = Entry(
        id="1",
        title="Entry 1",
        link="http://example.com/1",
        summary="Test summary",
        published=datetime(2023, 1, 1),
        read=False
    )
    entry2 = Entry(
        id="2",
        title="Entry 2",
        link="http://example.com/2",
        summary="Test summary",
        published=datetime(2023, 1, 1),
        read=True
    )
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com",
        entries=[entry1, entry2]
    )
    unread = feed.get_unread_entries()
    assert len(unread) == 1
    assert unread[0].id == "1"


def test_feed_get_favorite_entries():
    entry1 = Entry(
        id="1",
        title="Entry 1",
        link="http://example.com/1",
        summary="Test summary",
        published=datetime(2023, 1, 1),
        favorite=True
    )
    entry2 = Entry(
        id="2",
        title="Entry 2",
        link="http://example.com/2",
        summary="Test summary",
        published=datetime(2023, 1, 1),
        favorite=False
    )
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com",
        entries=[entry1, entry2]
    )
    favorites = feed.get_favorite_entries()
    assert len(favorites) == 1
    assert favorites[0].id == "1"


def test_feed_mark_entry_read():
    entry = Entry(
        id="1",
        title="Test Entry",
        link="http://example.com/entry",
        summary="Test summary",
        published=datetime(2023, 1, 1),
        read=False
    )
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com",
        entries=[entry]
    )
    result = feed.mark_entry_read("1")
    assert result is True
    assert entry.read is True


def test_feed_mark_entry_read_not_found():
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com"
    )
    result = feed.mark_entry_read("nonexistent")
    assert result is False


def test_feed_add_entries():
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com"
    )
    new_entries = [{
        "id": "1",
        "title": "New Entry",
        "link": "http://example.com/new",
        "summary": "New summary",
        "published": "2023-01-01T00:00:00"
    }]
    feed.add_entries(new_entries)
    assert len(feed.entries) == 1
    assert feed.entries[0].id == "1"


def test_feed_update_entry():
    entry = Entry(
        id="1",
        title="Old Title",
        link="http://example.com/entry",
        summary="Test summary",
        published=datetime(2023, 1, 1)
    )
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com",
        entries=[entry]
    )
    result = feed.update_entry("1", title="New Title", read=True)
    assert result is True
    assert entry.title == "New Title"
    assert entry.read is True


def test_feed_update_entry_not_found():
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com"
    )
    result = feed.update_entry("nonexistent", title="New Title")
    assert result is False


def test_feed_to_json():
    feed = Feed(
        url="http://example.com/feed",
        title="Test Feed",
        description="Test description",
        link="http://example.com"
    )
    json_str = feed.to_json()
    assert isinstance(json_str, str)
    assert "url" in json_str


def test_feed_from_json():
    json_data = '{"url": "http://example.com/feed", "title": "Test Feed", "description": "Test description", "link": "http://example.com", "entries": []}'
    feed = Feed.from_json(json_data)
    assert feed.url == "http://example.com/feed"
    assert feed.title == "Test Feed"


def test_entry_from_dict_with_none_dates():
    data = {
        "id": "1",
        "title": "Test Title",
        "link": "http://example.com",
        "summary": "Test summary",
        "published": None,
        "updated": None,
        "author": None,
        "content": None,
        "categories": []
    }
    entry = Entry.from_dict(data)
    assert entry.id == "1"
    assert entry.published is None
    assert entry.updated is None


def test_feed_from_dict_with_none_dates():
    data = {
        "url": "http://example.com/feed",
        "title": "Test Feed",
        "description": "Test description",
        "link": "http://example.com",
        "entries": [],
        "last_updated": None,
        "etag": None,
        "last_modified": None
    }
    feed = Feed.from_dict(data)
    assert feed.last_updated is None
    assert feed.etag is None
    assert feed.last_modified is None


def test_entry_from_dict_invalid_data():
    data = {
        "id": "1",
        "title": "Test Title",
        "link": "http://example.com",
        "summary": "Test summary",
        "published": "invalid-date",
        "author": "Test Author"
    }
    with pytest.raises(ValueError):
        Entry.from_dict(data)


def test_feed_from_dict_invalid_data():
    data = {
        "url": "http://example.com/feed",
        "title": "Test Feed",
        "description": "Test description",
        "link": "http://example.com",
        "last_updated": "invalid-date"
    }
    with pytest.raises(ValueError):
        Feed.from_dict(data)