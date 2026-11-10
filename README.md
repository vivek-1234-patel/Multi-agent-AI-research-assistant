# 🔎 AI Research Assistant

A multi-agent AI research assistant built with **LangChain**, **Google Gemini**, **Tavily Search**, and **Streamlit**. Enter any topic, and the system will search the web, read the top sources, write a structured report, and critique its own output.

## ✨ Features

- 🔍 **Search agent**: finds recent, relevant information using the Tavily API
- 📖 **Reader step**: scrapes the top source pages and extracts their main text
- ✍️ **Writer agent**: writes a structured article (introduction, key findings, conclusion)
- 🧐 **Critique agent**: scores the report on accuracy, relevance, completeness, clarity, and reliability
- 📡 **Live progress**: see each agent's status while research is running
- 🗂️ **Session history**: revisit previous research from the sidebar
- ⬇️ **Download**: export the report and critique as a Markdown file

## 🧠 How It Works

```
Topic
  │
  ▼
[1] Search agent  ──►  Tavily search results (titles, URLs, snippets)
  │
  ▼
[2] Reader        ──►  Scrapes the top URLs found in the results
  │
  ▼
[3] Writer agent  ──►  Writes a structured report from the research
  │
  ▼
[4] Critique agent ──► Evaluates the report and suggests improvements
```

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) for the UI
- [LangChain](https://www.langchain.com/) and LangGraph for agents
- [Google Gemini](https://ai.google.dev/) via `langchain-google-genai`
- [Tavily](https://tavily.com/) for web search
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and Requests for scraping
- python-dotenv for configuration

## 📁 Project Structure

```
Multi_Agent_System/
├── app.py            # Streamlit UI
├── pipeline.py       # Research pipeline (search → read → write → critique)
├── agent.py          # LLM setup, agents, and prompt chains
├── tools.py          # Tavily search and web scraping tools
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed)
├── .gitignore        # Ignores .env, .venv, cache files
└── README.md
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/multi-agent-research.git
cd multi-agent-research
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Add your API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

- Get a Gemini API key at [Google AI Studio](https://aistudio.google.com/)
- Get a Tavily API key at [app.tavily.com](https://app.tavily.com/)

### 5. Run the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## 💬 How to Use

1. Type a research topic, for example: `Impact of AI on healthcare in India`.
2. Click **🚀 Start Research** and watch the agents work.
3. Read the report in the **Report** tab, and check the **Critique**, **Search Results**, and **Scraped Content** tabs.
4. Click **⬇️ Download report** to save it as Markdown.
5. Use the sidebar to revisit past research or clear the history.

## 🧯 Troubleshooting

- **`429 RESOURCE_EXHAUSTED`**: you've hit the Gemini free-tier rate limit. Wait a minute and try again, or enable billing in Google AI Studio.
- **`404 NOT_FOUND` for a model**: the model name is retired or unavailable. Check the available models in your AI Studio account and update `model=` in `agent.py`.
- **`503 UNAVAILABLE`**: Google's servers are temporarily overloaded. Retry after a short while.
- **`ModuleNotFoundError`**: run `python -m pip install -r requirements.txt` inside the active venv.
- **Empty scraped content**: some websites block scrapers or load content with JavaScript. This is expected for those sites.

## ⚠️ Disclaimer

This tool is for research and learning purposes. Always verify important information from the original sources. Respect each website's terms of service and `robots.txt` when scraping.

## 📄 License

This project is open source. Add a license of your choice here (for example, MIT).
