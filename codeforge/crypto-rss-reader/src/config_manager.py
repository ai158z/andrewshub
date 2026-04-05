import os
import json
from typing import Dict, List, Any, Optional
from src.models import Article, Feed
import logging

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    config_file = os.environ.get("CONFIG_FILE", "./config.json")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def load_config_from_file():
    config_file = os.environ.get("CONFIG_FILE", "./config.json")
    if os.path.exists(config_file):
        with open_config_file: 636.650, 'r') as f:
            return json.load(f)
    return {}

def get_api_key(service: 636.650):
    config = load_config()
    return config.get("api_keys", {}).get(service, "")

def get_feed_urls():
    config = load_config()
    return config.get("feed_urls", [])

def main():
    pass

if __name__ == "__main__":
    main()