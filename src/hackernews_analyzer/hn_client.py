"""
HackerNews API Client
Fetches top stories and their details from HackerNews official API.
"""

import requests
import time
from typing import List, Dict, Optional


class HNClient:
    """Client to interact with HackerNews API"""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self, delay: float = 1.0):
        """
        Initialize HN Client
        
        Args:
            delay: Seconds to wait between API calls (be respectful!)
        """
        self.delay = delay
        
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """
        Make a request to HN API with error handling
        
        Args:
            endpoint: API endpoint (e.g., '/item/123.json')
            
        Returns:
            JSON response or None if failed
        """
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", timeout=10)
            response.raise_for_status()
            time.sleep(self.delay)  # Be nice to the API
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return None
    
    def get_top_stories(self, limit: int = 30) -> List[int]:
        """
        Get IDs of top stories
        
        Args:
            limit: Number of story IDs to fetch (max 500 available)
            
        Returns:
            List of story IDs
        """
        data = self._make_request("/topstories.json")
        if data:
            return data[:limit]
        return []
    
    def get_story_details(self, story_id: int) -> Optional[Dict]:
        """
        Get details of a specific story
        
        Args:
            story_id: HackerNews story ID
            
        Returns:
            Story details including title, url, score, comments
        """
        story = self._make_request(f"/item/{story_id}.json")
        
        if not story:
            return None
            
        # Extract relevant fields
        return {
            "id": story.get("id"),
            "title": story.get("title", ""),
            "url": story.get("url", ""),
            "score": story.get("score", 0),
            "by": story.get("by", "unknown"),
            "time": story.get("time", 0),
            "descendants": story.get("descendants", 0),  # Number of comments
            "type": story.get("type", ""),
            "text": story.get("text", "")  # Some stories have text content
        }
    
    def get_top_stories_details(self, limit: int = 30) -> List[Dict]:
        """
        Get full details of top stories
        
        Args:
            limit: Number of stories to fetch
            
        Returns:
            List of story dictionaries
        """
        print(f"Fetching top {limit} stories from HackerNews...")
        story_ids = self.get_top_stories(limit)
        
        stories = []
        for i, story_id in enumerate(story_ids, 1):
            print(f"Fetching story {i}/{len(story_ids)}: ID {story_id}")
            story = self.get_story_details(story_id)
            if story:
                stories.append(story)
        
        print(f"Successfully fetched {len(stories)} stories!")
        return stories


# Quick test if running this file directly
if __name__ == "__main__":
    client = HNClient()
    stories = client.get_top_stories_details(limit=5)
    
    print("\n=== Top 5 HackerNews Stories ===")
    for story in stories:
        print(f"\nTitle: {story['title']}")
        print(f"Score: {story['score']} | Comments: {story['descendants']}")
        print(f"URL: {story['url']}")