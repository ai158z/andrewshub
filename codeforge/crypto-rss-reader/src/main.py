import argparse
import logging
import os
import sys
from typing import Dict, List, Optional

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def process_feeds(config: Dict) -> None:
    """Process RSS feeds for article extraction and alerting"""
    from src.db import initialize_db, save_articles
    from src.feeds import fetch_all_feeds, filter_articles
    from src.moonpay import is_payment_relevant, send_alert
    from src.config import config_get_feed_urls
    from src.db_feeds import db_get_feed_urls
    
    logger = logging.getLogger(__name__)
    
    # Initialize database
    initialize_db()
    
    # Get feed URLs from config or database
    feed_urls = config.get('feeds', [])
    if not feed_urls:
        config_feeds = config_get_feed_urls()
        db_feeds = db_get_feed_urls()
        feed_urls = config_feeds or db_feeds or []
    
    if not feed_urls:
        logger.warning("No feed URLs found in config or database")
        return
    
    logger.info(f"Processing {len(feed_urls)} feeds")
    
    # Fetch articles from feeds
    articles = fetch_all_feeds(feed_urls)
    
    # Filter articles
    filtered_articles = filter_articles(articles)
    
    # Save articles to database
    if filtered_articles:
        save_articles(filtered_articles, 'sqlite:///data.db')
    
    # Check for MoonPay payment relevance and send alert
    if filtered_articles and is_payment_relevant(filtered_articles[0]):
        success = send_alert(filtered_articles[0])
        if not success:
            logger.error("Failed to send MoonPay alert")
    
    logger.info("Feed processing completed")

def main() -> None:
    """Main entry point for the application"""
    from src.config import load_config
    
    parser = argparse.ArgumentParser(description='Process crypto payment feeds')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    args = parser.parse_args()
    
    try:
        config = load_config(args.config)
        process_feeds(config)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()