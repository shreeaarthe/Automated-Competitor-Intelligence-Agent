# MarketPulse: Automated Competitor Intelligence Agent

MarketPulse is an advanced AI agent designed to automate competitor research. Powered by **LangGraph**, **Groq (Llama 3)**, and **Tavily**, it performs deep-dive investigations into any given company to produce comprehensive intelligence reports.

## 🚀 Features

- **Query Optimization**: Breaks down user requests into targeted search queries.
- **Deep Web Search**: Uses Tavily's advanced search depth to find relevant news and financial data.
- **Smart Scraper**: Extracts full content from top sources, filtering out noise.
- **Intelligent Synthesis**: Summarizes vast amounts of data using Llama 3 (via Groq).
- **Structured Reporting**: Generates a final report containing:
  - 📰 Recent News
  - ♟️ Strategic Moves
  - ⚖️ SWOT Analysis
  - 📈 Sentiment Analysis

## 🛠️ Tech Stack

- **Framework**: LangChain & LangGraph
- **LLM**: Groq (Llama 3.3 70B Versatile)
- **Search**: Tavily API
- **Scraping**: BeautifulSoup4 / WebBaseLoader

## 📋 Prerequisites

- Python 3.9+
- API Keys for:
  - [Groq](https://console.groq.com/)
  - [Tavily](https://tavily.com/)

## ⚡ Installation

1. **Clone the repository** (or navigate to the project folder):
   ```bash
   cd Chatbot
   ```

2. **Create a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**:
   Create a `.env` file in the root directory and add your keys:
   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## ▶️ How to Run

1. Ensure your virtual environment is active.
2. Run the entry script:
   ```bash
   python main.py
   ```
3. Enter the name of the company you want to research (e.g., "NVIDIA", "Tesla", "Microsoft").
4. The agent will execute the research workflow and save the final report as `[Company_Name]_report.md`.

## 📂 Project Structure

- `main.py`: Entry point for the application.
- `graph.py`: Defines the LangGraph workflow structure.
- `nodes.py`: Contains the logic for each agent node (Optimizer, Search, Scraper, etc.).
- `requirements.txt`: Python dependencies.
