# RSS Feed Reader
import feedparser
import sys
import traceback

if len(sys.argv) < 2:
    print("Usage: python3 rss_feed_reader.py <feed_url>")
    sys.exit(1)

feed_url = sys.argv[1]

try:
    feed = feedparser.parse(feed_url)
except Exception as e:
    print(f"Error parsing feed: {str(e)}")
    sys.exit(2)

if feed.bozo:
    print(f"Error parsing feed: {feed.bozo_exception}")
    sys.exit(2)

print("\n=== Feed: \n")
print(f"Title: {feed.feed.title if 'title' in feed.feed else 'Untitled'}\n")
print(f"Link: {feed.feed.link if 'link' in feed.feed else 'Unknown'}\n")
print("\nArticles:\n")

count = 0
for idx, entry in enumerate(feed.entries):
    try:
        print(f"{idx+1}. {entry.title}\n  {entry.link}\n  {entry.published}\n\n")
        count += 1
    except Exception as e:
        print(f"Error processing article {idx+1}: {str(e)}")

if count == 0:
    print("No articles found in the feed.\n")
