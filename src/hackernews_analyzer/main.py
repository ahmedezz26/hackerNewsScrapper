"""
HackerNews Trend Analyzer - Main Application
Orchestrates data fetching, analysis, and report generation.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from hackernews_analyzer.hn_client import HNClient
from hackernews_analyzer.llm_analyzer import LLMAnalyzer


class HNTrendAnalyzer:
    """Main application that orchestrates the entire analysis pipeline"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the analyzer
        
        Args:
            data_dir: Directory to store analysis results
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize our modules
        self.hn_client = HNClient(delay=1.0)
        self.llm_analyzer = LLMAnalyzer()
        
        print("✓ HackerNews Trend Analyzer initialized!")
        print(f"✓ Data directory: {self.data_dir.absolute()}")
    
    def fetch_stories(self, limit: int = 30) -> list:
        """
        Fetch top stories from HackerNews
        
        Args:
            limit: Number of stories to fetch
            
        Returns:
            List of story dictionaries
        """
        print(f"\n{'='*60}")
        print("STEP 1: FETCHING HACKERNEWS STORIES")
        print(f"{'='*60}")
        
        stories = self.hn_client.get_top_stories_details(limit=limit)
        
        # Save raw data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_file = self.raw_dir / f"stories_{timestamp}.json"
        
        with open(raw_file, 'w') as f:
            json.dump(stories, f, indent=2)
        
        print(f"✓ Saved raw data to: {raw_file}")
        return stories
    
    def analyze_stories(self, stories: list) -> dict:
        """
        Analyze stories using LLM
        
        Args:
            stories: List of story dictionaries
            
        Returns:
            Analysis results dictionary
        """
        print(f"\n{'='*60}")
        print("STEP 2: ANALYZING WITH AI")
        print(f"{'='*60}")
        
        # Run all analyses
        categories = self.llm_analyzer.categorize_stories(stories)
        sentiment = self.llm_analyzer.analyze_sentiment(stories)
        summary = self.llm_analyzer.generate_summary(stories, categories, sentiment)
        
        # Compile results
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "story_count": len(stories),
            "categories": categories,
            "sentiment": sentiment,
            "summary": summary,
            "top_stories": [
                {
                    "title": s["title"],
                    "score": s["score"],
                    "comments": s["descendants"],
                    "url": s["url"]
                }
                for s in stories[:10]  # Include top 10
            ]
        }
        
        return analysis
    
    def save_analysis(self, analysis: dict) -> Path:
        """
        Save analysis results to file
        
        Args:
            analysis: Analysis results dictionary
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_file = self.processed_dir / f"analysis_{timestamp}.json"
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"\n✓ Saved analysis to: {analysis_file}")
        return analysis_file
    
    def generate_report(self, analysis: dict) -> str:
        """
        Generate human-readable report
        
        Args:
            analysis: Analysis results dictionary
            
        Returns:
            Formatted report string
        """
        report = f"""
{'='*60}
HACKERNEWS TREND ANALYSIS REPORT
{'='*60}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Stories Analyzed: {analysis['story_count']}

{'='*60}
CATEGORIES
{'='*60}
"""
        
        for category, story_nums in analysis['categories'].items():
            report += f"\n{category}: {len(story_nums)} stories"
        
        report += f"""

{'='*60}
SENTIMENT ANALYSIS
{'='*60}
Overall Sentiment: {analysis['sentiment'].get('overall_sentiment', 'N/A')}
Confidence: {analysis['sentiment'].get('confidence', 'N/A')}

Key Observations:
"""
        
        for obs in analysis['sentiment'].get('key_observations', []):
            report += f"  • {obs}\n"
        
        report += "\nTrending Themes:\n"
        for theme in analysis['sentiment'].get('trending_themes', []):
            report += f"  • {theme}\n"
        
        report += f"""
{'='*60}
AI-GENERATED SUMMARY
{'='*60}
{analysis['summary']}

{'='*60}
TOP STORIES
{'='*60}
"""
        
        for i, story in enumerate(analysis['top_stories'], 1):
            report += f"""
{i}. {story['title']}
   Score: {story['score']} | Comments: {story['comments']}
   URL: {story['url']}
"""
        
        report += f"\n{'='*60}\n"
        return report
    
    def run_analysis(self, story_limit: int = 30) -> dict:
        """
        Run the complete analysis pipeline
        
        Args:
            story_limit: Number of stories to analyze
            
        Returns:
            Analysis results dictionary
        """
        print("\n🚀 Starting HackerNews Trend Analysis...")
        
        # Step 1: Fetch stories
        stories = self.fetch_stories(limit=story_limit)
        
        if not stories:
            print("❌ No stories fetched. Aborting.")
            return {}
        
        # Step 2: Analyze with AI
        analysis = self.analyze_stories(stories)
        
        # Step 3: Save results
        self.save_analysis(analysis)
        
        # Step 4: Generate and display report
        print(f"\n{'='*60}")
        print("STEP 3: GENERATING REPORT")
        print(f"{'='*60}")
        
        report = self.generate_report(analysis)
        print(report)
        
        # Save report as text file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.processed_dir / f"report_{timestamp}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"✓ Report saved to: {report_file}")
        
        print("\n✅ Analysis complete!")
        return analysis


def main():
    """Entry point for the application"""
    # Create analyzer instance
    analyzer = HNTrendAnalyzer()
    
    # Run analysis on top 30 stories
    # (You can change this number - fewer = faster, more = better trends)
    analyzer.run_analysis(story_limit=20)


if __name__ == "__main__":
    main()