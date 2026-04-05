import requests
import base64
import os
from typing import List, Dict, Any
import json
from src.utils.logger import setup_logger

class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token
        self.logger = setup_logger()
        self.session = requests.Session()
        if token:
            self.session.headers.update({
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'CodeReviewAnalyzer'
            })
        elif token is None:
            # No token provided, don't set Authorization header
            pass
        else:
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def fetch_pr_diff(self, url: str) -> str:
        if not url:
            raise ValueError("URL cannot be empty")
        headers = {'Accept': 'application/vnd.github.v3.diff'}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def get_pr_files(self, url: str) -> List[Dict[str, Any]]:
        if not url:
            raise ValueError("URL cannot be empty")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def _fetch_github_data(self, url: str, accept_type: str = 'application/vnd.github.v3.diff') -> str:
        headers = {'Accept': accept_type}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.text