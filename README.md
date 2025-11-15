# 🚀 HackerNews Trend Analyzer

An AI-powered tool that fetches, analyzes, and generates insights from HackerNews stories using a local LLM (llama3.2). Built as a learning project to explore LLM integration, web scraping, and AI-powered analysis.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Output](#output)
- [Technologies Used](#technologies-used)
- [Future Enhancements](#future-enhancements)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

This project analyzes trending stories from HackerNews using AI. It:
- Fetches top stories from HackerNews API
- Categorizes them by topic (AI/ML, Startups, Programming, Hardware, etc.)
- Analyzes sentiment and trending themes
- Generates human-readable summary reports
- Runs completely locally using llama3.2 (no API costs!)

**Perfect for:** Engineers learning LLM integration, AI enthusiasts, or anyone wanting automated tech trend analysis.

---

## ✨ Features

- **🔍 HackerNews Data Fetching**: Retrieves top stories with titles, scores, comments, and URLs
- **🧠 AI-Powered Analysis**: Uses local llama3.2 for intelligent categorization and insights
- **📊 Sentiment Analysis**: Identifies overall mood and trending themes
- **📝 Automated Reports**: Generates formatted text reports with all insights
- **💾 Data Persistence**: Saves raw data and analysis results for historical tracking
- **🆓 100% Free**: Runs entirely on your machine, no API costs
- **⚡ Structured Output**: Uses JSON mode for reliable LLM responses

---

## 🏗️ Architecture

```
┌─────────────────┐
│  HackerNews API │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   hn_client.py  │─────▶│  llm_analyzer.py │
│  (Data Fetcher) │      │  (AI Analyzer)   │
└─────────────────┘      └────────┬─────────┘
         │                         │
         │                         │
         ▼                         ▼
┌──────────────────────────────────────┐
│            main.py                   │
│         (Orchestrator)               │
└────────────┬─────────────────────────┘
             │
             ▼
    ┌────────────────┐
    │  data/raw/     │  (Raw HN stories)
    │  data/processed/│  (Analysis results)
    └────────────────┘
```

**Data Flow:**
1. **Fetch** → HackerNews API returns top stories
2. **Process** → llama3.2 analyzes and categorizes
3. **Generate** → Creates formatted reports
4. **Save** → Stores results for future reference

---

## 📦 Prerequisites

Before you begin, you'll need:

- **Python 3.10+** (Check: `python --version`)
- **Git** (for cloning the repo)
- **8GB+ RAM** (for running llama3.2 locally)
- **Windows, macOS, or Linux**

---

## 🛠️ Installation

### Step 1: Install Ollama (Local LLM Runtime)

Ollama allows you to run LLMs locally on your machine.

#### **Windows**
```bash
# Download and install from:
https://ollama.com/download/windows

# Or using winget:
winget install Ollama.Ollama
```

#### **macOS**
```bash
# Download from:
https://ollama.com/download/mac

# Or using Homebrew:
brew install ollama
```

#### **Linux**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Verify installation:**
```bash
ollama --version
```

---

### Step 2: Install llama3.2 Model

```bash
# Pull the llama3.2 model (3B parameters version)
ollama pull llama3.2

# Verify it's installed
ollama list
```

**Note:** First download will take a few minutes (~2GB). The model runs locally on your machine.

---

### Step 3: Start Ollama Server

```bash
# Start Ollama in the background
ollama serve
```

**Keep this terminal open** or run it as a background service.

**Verify it's running:**
- Open browser: `http://localhost:11434`
- You should see: "Ollama is running"

---

### Step 4: Install `uv` (Fast Python Package Manager)

`uv` is a modern, lightning-fast Python package manager (alternative to pip/conda).

#### **Windows**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### **macOS/Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation:**
```bash
uv --version
```

---

### Step 5: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/yourusername/hackernews-analyzer.git
cd hackernews-analyzer

# Initialize uv project (if not already done)
uv init

# Install dependencies
uv add requests openai python-dotenv

# Install the package in development mode
uv pip install -e .
```

---

### Step 6: Configure Environment

Create a `.env` file in the project root:

```bash
# .env
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2
```

**Note:** These are the default settings. Change only if you're using a different port or model.

---

## 🚀 Usage

### Run the Analyzer

```bash
uv run python src/hackernews_analyzer/main.py
```

### What Happens:

1. **Fetches** top 20 HackerNews stories (~30 seconds)
2. **Analyzes** with llama3.2 (~1-2 minutes)
   - Categorizes by topic
   - Analyzes sentiment
   - Generates summary
3. **Saves** results to `data/` folder
4. **Displays** formatted report in terminal

### Expected Output:

```
✓ HackerNews Trend Analyzer initialized!
✓ Data directory: /path/to/hackernews-analyzer/data

============================================================
STEP 1: FETCHING HACKERNEWS STORIES
============================================================
Fetching top 20 stories from HackerNews...
Fetching story 1/20: ID 42156789
...
Successfully fetched 20 stories!

============================================================
STEP 2: ANALYZING WITH AI
============================================================
📊 Categorizing stories...
💭 Analyzing sentiment...
📝 Generating summary report...

============================================================
STEP 3: GENERATING REPORT
============================================================

============================================================
HACKERNEWS TREND ANALYSIS REPORT
============================================================
Generated: 2024-11-15 14:30:22
Stories Analyzed: 20

============================================================
CATEGORIES
============================================================

AI/ML: 5 stories
Programming: 8 stories
Startups: 3 stories
Hardware: 2 stories
Security: 2 stories

============================================================
SENTIMENT ANALYSIS
============================================================
Overall Sentiment: positive
Confidence: high

Key Observations:
  • Strong interest in AI model improvements
  • Active discussions on programming tools
  • Community excited about new releases

Trending Themes:
  • AI advancements
  • Developer productivity

============================================================
AI-GENERATED SUMMARY
============================================================
[AI-generated summary of trends...]

============================================================
TOP STORIES
============================================================

1. New AI Model Beats GPT-4 on Benchmarks
   Score: 850 | Comments: 234
   URL: https://example.com/story1

...

✓ Report saved to: data/processed/report_20241115_143045.txt

✅ Analysis complete!
```

---

## 📁 Project Structure

```
hackernews-analyzer/
├── src/
│   └── hackernews_analyzer/
│       ├── __init__.py          # Package initialization
│       ├── hn_client.py         # HackerNews API client
│       ├── llm_analyzer.py      # LLM analysis engine
│       └── main.py              # Main orchestrator
├── data/
│   ├── raw/                     # Raw HN story data (JSON)
│   └── processed/               # Analysis results (JSON + TXT)
├── .env                         # Environment configuration
├── pyproject.toml               # Project dependencies
├── .python-version              # Python version requirement
└── README.md                    # This file
```

### Key Files Explained:

#### **`hn_client.py`** - Data Fetcher
- Connects to HackerNews API
- Fetches top story IDs
- Retrieves full story details (title, score, comments, URL)
- Implements rate limiting (1 second delay between requests)

#### **`llm_analyzer.py`** - AI Brain
- Connects to local llama3.2 via Ollama
- **Categorizes stories** into topics (AI, Startups, Programming, etc.)
- **Analyzes sentiment** (positive/negative/neutral with confidence)
- **Generates summaries** in natural language
- Uses JSON mode for structured outputs

#### **`main.py`** - Orchestrator
- Manages the complete pipeline: Fetch → Analyze → Save → Report
- Saves raw data to `data/raw/` (timestamped JSON files)
- Saves analysis to `data/processed/` (JSON + TXT reports)
- Generates formatted reports for humans

---

## 🔧 How It Works

### 1. Data Collection (`hn_client.py`)

```python
# Fetches top story IDs
story_ids = get_top_stories(limit=20)

# Gets details for each story
for story_id in story_ids:
    story = get_story_details(story_id)
    # Returns: {id, title, url, score, comments, etc.}
```

**HackerNews API:**
- Official Firebase API (free, no auth required)
- Respects rate limits with delays
- Returns JSON data

---

### 2. AI Analysis (`llm_analyzer.py`)

#### **Categorization:**
```python
# Sends story titles to llama3.2
system_prompt = "You are a tech categorizer..."
user_prompt = "Categorize these stories: [story list]"

# LLM returns structured JSON
{
  "AI/ML": [1, 5, 12],
  "Startups": [2, 8],
  ...
}
```

#### **Sentiment Analysis:**
```python
# Analyzes overall mood
{
  "overall_sentiment": "positive",
  "confidence": "high",
  "key_observations": ["obs1", "obs2"],
  "trending_themes": ["theme1", "theme2"]
}
```

#### **Summary Generation:**
```python
# Generates human-readable summary
"Today's HackerNews shows strong interest in AI 
advancements, with 5 stories discussing new models..."
```

**Key Techniques:**
- **Prompt Engineering**: Clear, specific instructions to LLM
- **JSON Mode**: `response_format={"type": "json_object"}` ensures valid JSON
- **Temperature Control**: `0.3` for consistent, focused analysis
- **Error Handling**: Graceful fallbacks if parsing fails

---

### 3. Data Persistence

**Raw Data (`data/raw/`):**
```json
// stories_20241115_143022.json
{
  "id": 42156789,
  "title": "New AI Model Released",
  "score": 850,
  "descendants": 234,
  "url": "https://..."
}
```

**Processed Analysis (`data/processed/`):**
```json
// analysis_20241115_143155.json
{
  "timestamp": "2024-11-15T14:31:55",
  "story_count": 20,
  "categories": {...},
  "sentiment": {...},
  "summary": "..."
}
```

**Why save raw data?**
- Can reprocess without re-fetching
- Historical tracking
- Debugging and iteration

---

## 📊 Output

After running the analyzer, you'll find:

### **1. Terminal Report**
Real-time formatted report with all insights

### **2. JSON Files**
- `data/raw/stories_YYYYMMDD_HHMMSS.json` - Raw HN data
- `data/processed/analysis_YYYYMMDD_HHMMSS.json` - Full analysis

### **3. Text Report**
- `data/processed/report_YYYYMMDD_HHMMSS.txt` - Human-readable report

All files are timestamped, so you never lose historical data!

---

## 🛠️ Technologies Used

- **Python 3.10+** - Core language
- **uv** - Fast package manager
- **Ollama** - Local LLM runtime
- **llama3.2** - 3B parameter language model
- **HackerNews API** - Official Firebase API
- **requests** - HTTP client
- **openai** - LLM client library (Ollama-compatible)
- **python-dotenv** - Environment configuration

---

## 🚀 Future Enhancements

### **Planned Features:**

1. **User Control**
   - Interactive CLI for topic selection
   - Search by keywords (e.g., "ADAS", "autonomous driving")
   - Customizable story limits

2. **Better Analysis**
   - Extract key technologies mentioned
   - Identify emerging topics
   - Compare trends over time (today vs. last week)
   - Track topic growth/decline

3. **Visualizations**
   - HTML dashboard with charts
   - Category distribution pie charts
   - Sentiment timeline graphs
   - Interactive story explorer

4. **Automation**
   - Daily scheduled runs
   - WhatsApp/Telegram/Email notifications
   - Automatic trend alerts

5. **Advanced Features**
   - Multi-source analysis (Reddit, Twitter, etc.)
   - Custom AI models for specific domains
   - Export to PDF/PowerPoint
   - API endpoint for programmatic access

---

## 🐛 Troubleshooting

### **Issue: "ModuleNotFoundError: No module named 'hackernews_analyzer'"**

**Solution:**
```bash
# Make sure you installed the package
uv pip install -e .

# Or update pyproject.toml with correct config
```

---

### **Issue: "Connection refused" or "Ollama not found"**

**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# Check if it's accessible
curl http://localhost:11434
```

---

### **Issue: "Failed to parse JSON response"**

**Cause:** llama3.2 didn't return valid JSON

**Solution:**
- Try running again (LLMs are probabilistic)
- Reduce story count (fewer stories = simpler task)
- Check if JSON mode is supported: `response_format={"type": "json_object"}`

---

### **Issue: Analysis is very slow**

**Causes & Solutions:**
- **CPU/RAM limited**: llama3.2 needs 8GB+ RAM
- **Too many stories**: Reduce limit to 10-15 for faster runs
- **Model size**: Use smaller model like `llama3.2:1b` (faster but less accurate)

```bash
# Install smaller model
ollama pull llama3.2:1b

# Update .env
OLLAMA_MODEL=llama3.2:1b
```

---

### **Issue: No stories found**

**Solution:**
```bash
# Test HackerNews API directly
curl https://hacker-news.firebaseio.com/v0/topstories.json

# Check your internet connection
```

---

## 📝 License

Feel free to use and modify for your projects!

---

## 🙏 Acknowledgments

- **HackerNews** for the excellent public API
- **Ollama** for making local LLMs accessible
- **Meta AI** for llama3.2 model

---

## 📧 Contact

For questions, suggestions, or collaboration:
- **GitHub Issues**: [Report a bug or request a feature]
- **Email**: ahmedezzelldeen@example.com

---

**Happy Analyzing! 🚀**

*Built as a learning project to explore LLM integration and AI-powered analysis.*