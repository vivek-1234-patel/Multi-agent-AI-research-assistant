from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for recent information and return titles, URLs and snippets."""
    try:
        response = tavily.search(
            query=query,
            topic="news",
            time_range="month",
            search_depth="advanced",
            max_results=5,
        )
    except Exception as e:
        return f"Web search failed: {e}"

    results = response.get("results", [])
    if not results:
        return "No results found."

    output = []
    for result in results:
        output.append(
            f"Title: {result.get('title', 'No title')}\n"
            f"URL: {result.get('url', '')}\n"
            f"Snippet: {result.get('content', '')[:300]}\n"
        )
    return "\n----\n".join(output)


@tool
def web_scrape(url: str) -> str:
    """Scrape the main text content of a web page given its URL."""
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        return text[:4000]  # 1000 was too small for a useful summary
    except requests.RequestException as e:
        return f"Failed to retrieve the web page: {e}"
    except Exception as e:
        return f"An error occurred while scraping the web page: {e}"