import re
from langchain_core.messages import HumanMessage
from agent import (
    build_agent_searcher,
    writer_chain,
    critique_chain,
    to_text,
)
from tools import web_scrape


def _extract_urls(text: str, limit: int = 3) -> list[str]:
    urls = re.findall(r"https?://[^\s)\]\"'<>]+", text)
    seen, unique = set(), []
    for u in urls:
        u = u.rstrip(".,;")
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique[:limit]


def run_research_pipeline(topic: str, on_step=None) -> dict:
    state = {}

    def emit(step, status, detail=""):
        if on_step:
            on_step(step, status, detail)

    # Step 1: search agent
    emit(1, "running")
    print("\n" + "=" * 50)
    print("Step 1: Search agent gathering information...")
    print("=" * 50)

    search_agent = build_agent_searcher()
    search_out = search_agent.invoke({
        "messages": [HumanMessage(content=(
            f"Find recent, reliable and detailed information on the topic: '{topic}'. "
            "Include the source URLs for each point."
        ))]
    })
    state["search_results"] = to_text(search_out["messages"][-1].content)
    emit(1, "done", state["search_results"])

    # Step 2: reader (direct scraping of URLs found in search results)
    emit(2, "running")
    print("\n" + "=" * 50)
    print("Step 2: Reader scraping top sources...")
    print("=" * 50)

    urls = _extract_urls(state["search_results"])
    if urls:
        parts = [f"Source: {u}\n{web_scrape.invoke(u)}" for u in urls]
        state["scraped_content"] = "\n\n".join(parts)
    else:
        state["scraped_content"] = "No source URLs found to scrape."
    emit(2, "done", state["scraped_content"])

    # Step 3: writer
    emit(3, "running")
    print("\n" + "=" * 50)
    print("Step 3: Writer creating the report...")
    print("=" * 50)

    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Scraped Content:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    emit(3, "done", state["report"])

    # Step 4: critique
    emit(4, "running")
    print("\n" + "=" * 50)
    print("Step 4: Critique agent evaluating the report...")
    print("=" * 50)

    state["feedback"] = critique_chain.invoke({
        "user_query": topic,
        "tool_output": research_combined,
        "ai_response": state["report"],
    })
    emit(4, "done", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("Enter the topic for research: ")
    result = run_research_pipeline(topic)
    print(result["report"])