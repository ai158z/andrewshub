import click
import sys
import os
import logging
from typing import Optional
import json
from datetime import datetime
import feedparser
from dataclasses import dataclass
from src.feed_fetcher import fetch_feed
from src.summarizer import summarize_text
from src.utils import is_valid_url, sanitize_text


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.argument('url', type=click.STRING)
@click.option('--timeout', default=10, type=click.INT, help='Fetch timeout in seconds')
@click.option('--ratio', default=0.3, type=click.FLOAT, help='Summary ratio')
def main(url: str, timeout: int, ratio: float) -> None:
    """Main entry point for the RSS feed reader CLI."""
    if not is_valid_url(url):
        click.echo("Invalid URL provided.")
        return
    
    try:
        content = fetch_feed(url, timeout)
        summary = summarize_text(content, ratio)
        click.echo(summary)
    except Exception as e:
        print(f"Error: {e}")
        return


@dataclass
class Feed:
    entries: list


def parse_feed(url: str, content: str) -> Feed:
    """Parse a feed from URL and content."""
    try:
        feed_data = feedparser.parse(content if content else url)
        entries = []
        for entry in feed_data.entries:
            entries.append({
                'title': entry.get('title'),
                'description': entry.get('description'),
                'link': entry.get('link')
            })
        return Feed(entries=entries)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def configure():
    """Configure the command line interface."""
    pass


if __name__ == '__main__':
    # Run the CLI app
    main()