"""
LLM Analyzer - Uses local llama3.2 to analyze HackerNews stories
This module sends data to your local LLM and extracts insights.
"""

import json
import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMAnalyzer:
    """Analyzes HackerNews stories using local llama3.2"""
    
    def __init__(self):
        """
        Initialize connection to local llama3.2
        
        Uses OpenAI library but points to your local Ollama server
        """
        self.client = OpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key="not-needed"  # Ollama doesn't need API key
        )
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        
        print(f"✓ LLM Analyzer initialized: {self.model}")
    
    def _call_llm(self, system_prompt: str, user_prompt: str, use_json_mode: bool = False) -> str:
        """
        Make a call to local llama3.2
        
        Args:
            system_prompt: Instructions for the LLM (its role/behavior)
            user_prompt: The actual task/question
            use_json_mode: Whether to enforce JSON output format
            
        Returns:
            LLM's response as string
        """
        try:
            # Build request parameters
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3  # Lower = more focused/consistent responses
            }
            
            # Add JSON mode if requested and supported
            if use_json_mode:
                params["response_format"] = {"type": "json_object"}
            
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling LLM: {e}")
            # If JSON mode failed, try again without it
            if use_json_mode:
                print("⚠️  JSON mode not supported, falling back to regular mode...")
                return self._call_llm(system_prompt, user_prompt, use_json_mode=False)
            return ""
    
    def categorize_stories(self, stories: List[Dict]) -> Dict:
        """
        Categorize stories into topics (AI, Startups, Hardware, etc.)
        
        Args:
            stories: List of story dictionaries from HN
            
        Returns:
            Dictionary with categories and story counts
        """
        # Prepare story titles for the LLM
        story_list = "\n".join([
            f"{i+1}. {story['title']}"
            for i, story in enumerate(stories)
        ])
        
        system_prompt = """You are a tech categorizer. Categorize stories into these topics: AI/ML, Startups, Programming, Hardware, Security, Web, DevOps, Other.

Output ONLY this JSON format (no extra text):
{"AI/ML": [1, 3], "Startups": [2], "Programming": [4, 5]}

Use story numbers from the list. Include only categories that have stories."""

        user_prompt = f"""Categorize these stories. Output ONLY the JSON object:

{story_list}"""

        print("📊 Categorizing stories...")
        response = self._call_llm(system_prompt, user_prompt, use_json_mode=True)
        
        return self._parse_json_response(response, "categorization")
    
    def _parse_json_response(self, response: str, context: str = "") -> Dict:
        """
        Robustly parse JSON from LLM response
        
        Args:
            response: Raw LLM response
            context: Context for error messages
            
        Returns:
            Parsed JSON dict or empty dict if failed
        """
        # Clean the response
        cleaned = response.strip()
        
        # Remove markdown code blocks
        if cleaned.startswith("```json"):
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        
        # Try to extract JSON object if there's extra text
        if not cleaned.startswith("{"):
            # Find first { and last }
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            if start != -1 and end > start:
                cleaned = cleaned[start:end]
        
        # Try parsing
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse {context} response: {e}")
            print(f"Raw response:\n{response}\n")
            print(f"Cleaned response:\n{cleaned}\n")
            return {}
    
    def analyze_sentiment(self, stories: List[Dict]) -> Dict:
        """
        Analyze overall sentiment of trending topics
        
        Args:
            stories: List of story dictionaries
            
        Returns:
            Sentiment analysis results
        """
        # Create a summary of titles
        titles = [story['title'] for story in stories[:10]]  # Reduce to 10 for smaller models
        titles_text = "\n".join(f"- {title}" for title in titles)
        
        system_prompt = """You are a sentiment analyst. Analyze these headlines and respond with ONLY this JSON format (no extra text):

{"overall_sentiment": "positive", "confidence": "high", "key_observations": ["obs1", "obs2"], "trending_themes": ["theme1", "theme2"]}

Valid values:
- overall_sentiment: positive, neutral, or negative
- confidence: high, medium, or low
- key_observations: array of 2-3 short observations
- trending_themes: array of 1-2 themes"""

        user_prompt = f"""Analyze these HackerNews headlines. Output ONLY the JSON object with no additional text:

{titles_text}"""

        print("💭 Analyzing sentiment...")
        response = self._call_llm(system_prompt, user_prompt, use_json_mode=True)
        
        return self._parse_json_response(response, "sentiment")
    
    def generate_summary(self, stories: List[Dict], categories: Dict, sentiment: Dict) -> str:
        """
        Generate a human-readable summary report
        
        Args:
            stories: Raw story data
            categories: Categorization results
            sentiment: Sentiment analysis results
            
        Returns:
            Formatted summary text
        """
        # Prepare context for LLM
        story_list = "\n".join([
            f"- {story['title']} ({story['score']} points, {story['descendants']} comments)"
            for story in stories[:10]
        ])
        
        system_prompt = """You are a tech journalist writing a daily brief for busy engineers. 
Create a concise, engaging summary of today's HackerNews trends. 
Be specific, mention story titles, and highlight what's important.
Keep it under 200 words."""

        user_prompt = f"""Write a brief summary of today's HackerNews trends:

TOP STORIES:
{story_list}

CATEGORIES:
{json.dumps(categories, indent=2)}

SENTIMENT:
{json.dumps(sentiment, indent=2)}

Write a concise, engaging summary for engineers."""

        print("📝 Generating summary report...")
        summary = self._call_llm(system_prompt, user_prompt)
        return summary


# Quick test
if __name__ == "__main__":
    # Test with sample data
    test_stories = [
        {"title": "New AI model beats GPT-4", "score": 850, "descendants": 234},
        {"title": "YC W25 startups announced", "score": 450, "descendants": 123},
        {"title": "Rust 2.0 released", "score": 920, "descendants": 456},
    ]
    
    analyzer = LLMAnalyzer()
    
    print("\n=== Testing Categorization ===")
    categories = analyzer.categorize_stories(test_stories)
    print(json.dumps(categories, indent=2))
    
    print("\n=== Testing Sentiment Analysis ===")
    sentiment = analyzer.analyze_sentiment(test_stories)
    print(json.dumps(sentiment, indent=2))