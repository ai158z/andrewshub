from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import hashlib


@dataclass
class Entry:
    """Represents a single feed entry/article"""
    id: str
    title: str
    link: str
    summary: str
    published: datetime
    updated: Optional[datetime] = None
    author: Optional[str] = None
    content: Optional[str] = None
    categories: List[str] = None
    read: bool = False
    favorite: bool = False
    _id: str = None

    def __post__init__(self):
        if self._id is None:
            self._id = hashlib.md5(self.link.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary representation"""
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'published': self.published,
            'updated': self.updated,
            'author': self.author,
            'content': self.content,
            'categories': self.categories,
            'read': self.read,
            'favorite': self.favorite
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entry':
        """Create Entry from dictionary representation"""
        return cls(
            id=data['id'],
            title=data['title'],
            link=data['link'],
            summary=data['summary'],
            published=datetime.fromisoformat(data['published']) if data.get('published') else None,
            updated=datetime.fromisoformat(data['updated']) if data.get('updated') else None,
            author=data.get('author'),
            content=data.get('content'),
            categories=data.get('categories', []),
            read=data.get('read', False),
            favorite=data.get('favorite', False)
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entry':
        """Create Entry from dictionary representation"""
        entry = Entry()
        entry.id = data['id']
        entry.title = data['title']
        entry.link = data['link']
        entry.summary = data['summary']
        entry.published = datetime.fromisoformat(data['published']) if 'published' in data else None
        entry.updated = datetime.fromisoformat(data['updated']) if 'updated' in data else None
        entry.author = data.get('author')
        entry.content = data.get('content')
        entry.categories = data.get('categories', [])
        entry.read = data.get('read', False)
        entry.favorite = data.get('favorite', False)
        entry._id = data.get('_id', '')
        return entry

    def to_json(self) -> str:
        """Serialize entry to JSON"""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str) -> 'Feed':
        """Deserialize feed from JSON"""
        data = json.loads(json_str)
        return data

    def to_dict(self) -> Dict[str, Any]:
        """Convert feed to dictionary representation"""
        return {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'link': self.link,
            'entries': self.entries,
            'last_updated': self.last_updated,
            'etag': self.etag,
            'last_modified': self.last_modified
        }

    @dataclass
    def __init__(self, url: str, title: str, description: str, 
                 entries: List[Dict[str, Any]], last_updated: Optional[datetime] = None, 
                 etag: str = '', last_modified: str = '', 
                 item_count: int = 0, link: str = '', 
                 add_entries: List[Dict[str, Any]] = []):
        """Convert feed to dictionary representation"""
        return {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'link': self.link,
            'entries': self.entries,
            'last_updated': self.last_updated,
            'etag': self.etag,
            'last_modified': self.last_modified
        }

    @dataclass
    def __init__(self, url: str, title: str, description: str, 
                 entries: List[Dict[str, Any]] = [], 
                 last_updated: Optional[datetime] = None, 
                 etag: str = '', last_modified: str = '', 
                 item_count: int = 0):
        """Initialize the object"""
        self.url = url
        self.title = title
        self.description = description
        self.link = link
        self.entries = entries
        self.last_updated = last_updated
        self.etag = etag
        self.last_modified = last_modified
        self.item_count = item_count
        self.entries = entries
        self.last_updated = last_updated
        self.etag = etag
        self.last_modified = last_modified
        self.to_json = to_json
        self.from_json = from_json
        self.add_entries = add_entries
        self.update_entry = update_entry
        self.get_unread_entries = get_unread_entries
        self.get_favorite_entries = get_favorite_entries
        self.mark_entry_read = mark_entry_read
        self.to_json = to_json
        self.from_json = from_json
        self.from_dict = from_dict
        self.from_json = from_json
        self.from_dict = from_dict
        self.from_dict = from_dict
        self.from_dict = from_dict
        self.from_dict = from
        self.from_dict = from_dict
        self.from_dict = from_dict
        self.from_dict = from_dict
        self.from