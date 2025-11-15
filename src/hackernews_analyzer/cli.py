"""
Interactive CLI for HackerNews Trend Analyzer
Gives users full control over what they want to analyze
"""

from typing import Dict, List, Optional


class CLI:
    """Command-line interface for user interaction"""
    
    # Pre-defined topic keywords for quick selection
    TOPICS = {
        "1": {
            "name": "ADAS / Autonomous Driving",
            "keywords": ["ADAS", "autonomous", "self-driving", "autopilot", "FSD", "lidar", "radar", "vehicle"]
        },
        "2": {
            "name": "AI / Machine Learning",
            "keywords": ["AI", "ML", "machine learning", "GPT", "LLM", "neural", "model", "training", "Claude", "OpenAI"]
        },
        "3": {
            "name": "Startups / Funding",
            "keywords": ["startup", "YC", "funding", "Series A", "raised", "venture", "VC", "investment"]
        },
        "4": {
            "name": "Programming Languages",
            "keywords": ["Python", "Rust", "Go", "JavaScript", "TypeScript", "C++", "Java"]
        },
        "5": {
            "name": "Security / Privacy",
            "keywords": ["security", "privacy", "breach", "hack", "vulnerability", "encryption", "exploit"]
        },
        "6": {
            "name": "Hardware / Chips",
            "keywords": ["chip", "processor", "GPU", "CPU", "semiconductor", "hardware", "NVIDIA", "AMD", "Intel"]
        },
        "7": {
            "name": "Web Development",
            "keywords": ["web", "frontend", "backend", "React", "Vue", "Next.js", "framework", "API"]
        }
    }
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*70)
        print("🚀 HACKERNEWS TREND ANALYZER")
        print("="*70)
        print("\nWelcome! This tool helps you analyze HackerNews trends on topics")
        print("that matter to YOU.\n")
    
    def get_analysis_mode(self) -> str:
        """
        Ask user what type of analysis they want
        
        Returns:
            'general' or 'topic'
        """
        print("\n📊 What would you like to analyze?")
        print("  1. General top stories (no filtering)")
        print("  2. Specific topic (filtered search)")
        
        while True:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            if choice == "1":
                return "general"
            elif choice == "2":
                return "topic"
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
    
    def get_story_limit(self, mode: str) -> int:
        """
        Ask user how many stories to analyze
        
        Args:
            mode: 'general' or 'topic'
            
        Returns:
            Number of stories to fetch/analyze
        """
        if mode == "general":
            print("\n📝 How many TOP stories do you want to analyze?")
            default = 20
            suggestion = "10-30 stories is usually good"
        else:
            print("\n📝 How many stories to SEARCH THROUGH?")
            print("   (We'll search these, then filter by your topic)")
            default = 100
            suggestion = "50-200 stories recommended for good coverage"
        
        print(f"   💡 {suggestion}")
        
        while True:
            user_input = input(f"\nEnter number (or press Enter for {default}): ").strip()
            
            if user_input == "":
                return default
            
            try:
                limit = int(user_input)
                if limit < 1:
                    print("❌ Please enter a positive number.")
                elif limit > 500:
                    print("⚠️  Maximum is 500 stories (API limit).")
                else:
                    return limit
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def get_topic_choice(self) -> Dict:
        """
        Let user choose a pre-defined topic or create custom
        
        Returns:
            Dictionary with 'name' and 'keywords'
        """
        print("\n🎯 Choose a topic to analyze:")
        print("\n" + "-"*70)
        
        for key, topic in self.TOPICS.items():
            print(f"  {key}. {topic['name']}")
        
        print(f"  8. Custom topic (enter your own keywords)")
        print("-"*70)
        
        while True:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice in self.TOPICS:
                selected = self.TOPICS[choice]
                print(f"\n✓ Selected: {selected['name']}")
                print(f"  Keywords: {', '.join(selected['keywords'][:5])}...")
                return selected
            
            elif choice == "8":
                return self.get_custom_keywords()
            
            else:
                print("❌ Invalid choice. Please enter 1-8.")
    
    def get_custom_keywords(self) -> Dict:
        """
        Let user enter custom keywords
        
        Returns:
            Dictionary with 'name' and 'keywords'
        """
        print("\n✏️  Enter your custom topic:")
        print("   Examples:")
        print("   - 'Rust programming'")
        print("   - 'crypto blockchain'")
        print("   - 'remote work productivity'")
        
        while True:
            topic_name = input("\nTopic name: ").strip()
            if topic_name:
                break
            print("❌ Please enter a topic name.")
        
        print("\n✏️  Enter keywords (comma-separated):")
        print("   Example: rust, cargo, rustc, programming")
        
        while True:
            keywords_input = input("\nKeywords: ").strip()
            if keywords_input:
                keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
                if keywords:
                    print(f"\n✓ Custom topic created: {topic_name}")
                    print(f"  Keywords: {', '.join(keywords)}")
                    return {
                        "name": topic_name,
                        "keywords": keywords
                    }
            print("❌ Please enter at least one keyword.")
    
    def confirm_settings(self, mode: str, limit: int, topic: Optional[Dict] = None) -> bool:
        """
        Show user their choices and confirm
        
        Args:
            mode: 'general' or 'topic'
            limit: Number of stories
            topic: Topic dictionary if mode is 'topic'
            
        Returns:
            True if user confirms, False to restart
        """
        print("\n" + "="*70)
        print("📋 ANALYSIS SETTINGS")
        print("="*70)
        
        if mode == "general":
            print(f"  Mode: General top stories")
            print(f"  Stories to analyze: {limit}")
        else:
            print(f"  Mode: Topic-focused search")
            print(f"  Topic: {topic['name']}")
            print(f"  Keywords: {', '.join(topic['keywords'])}")
            print(f"  Stories to search: {limit}")
        
        print("="*70)
        
        while True:
            confirm = input("\n✓ Proceed with analysis? (y/n): ").strip().lower()
            if confirm == "y":
                return True
            elif confirm == "n":
                return False
            else:
                print("❌ Please enter 'y' or 'n'.")
    
    def run(self) -> Dict:
        """
        Run the interactive CLI and get user preferences
        
        Returns:
            Dictionary with user's analysis configuration
        """
        self.display_welcome()
        
        while True:
            # Get analysis mode
            mode = self.get_analysis_mode()
            
            # Get story limit
            limit = self.get_story_limit(mode)
            
            # Get topic if needed
            topic = None
            if mode == "topic":
                topic = self.get_topic_choice()
            
            # Confirm settings
            if self.confirm_settings(mode, limit, topic):
                # Return configuration
                config = {
                    "mode": mode,
                    "limit": limit,
                    "topic": topic
                }
                
                print("\n🚀 Starting analysis...\n")
                return config
            else:
                print("\n🔄 Let's start over...\n")


# Test the CLI
if __name__ == "__main__":
    cli = CLI()
    config = cli.run()
    print("\n✓ Configuration:")
    print(config)