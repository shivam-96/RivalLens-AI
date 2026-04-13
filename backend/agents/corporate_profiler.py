"""
corporate_profiler.py — Agent 1: Corporate Profiler

Uses Tavily search and Firecrawl scraping to gather comprehensive
corporate intelligence: funding, HQ, size, news, product list.
"""

from langchain_openai import ChatOpenAI

from backend.config import settings
from backend.schemas import CompanyData, PipelineState
from backend.tools.scrape import scrape_url
from backend.tools.search import search_company_info, search_recent_news


def corporate_profiler_node(state: PipelineState) -> dict:
    """
    Agent 1: Build a comprehensive corporate profile.

    Reads: state["inputs"], state["classifier"]
    Writes: state["company_data"]
    """
    inputs = state["inputs"]
    company_name = inputs.get("name", "")
    url = inputs.get("url", "")

    # ── Step 1: Gather raw intelligence ────────────────────────
    # Search for corporate data via Tavily
    search_results = search_company_info(company_name)

    # Search for recent news
    news_results = search_recent_news(company_name)

    # Scrape the company URL if provided
    scraped_content = ""
    if url:
        scraped_content = scrape_url(url)
        # Truncate if too long to fit in context
        if len(scraped_content) > 8000:
            scraped_content = scraped_content[:8000] + "\n...[truncated]"

    # ── Step 2: LLM extraction into structured data ────────────
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )
    structured_llm = llm.with_structured_output(CompanyData)

    prompt = f"""You are a corporate intelligence analyst. Extract comprehensive company data
for "{company_name}" from the following research sources.

CRITICAL RULES:
- Use ONLY the data provided below. Do NOT make up or guess any information.
- If a data point is not found in the sources, set it to "Not Found".
- For funding rounds, include specific investor names and amounts if available.
- For the product list, be exhaustive — list every product/service mentioned.
- For news items, include the actual headline, source, and date.

=== WEB SEARCH RESULTS ===
{search_results[:6000]}

=== RECENT NEWS ===
{news_results[:3000]}

=== SCRAPED WEBSITE CONTENT ===
{scraped_content[:4000]}

Extract all available corporate data now. Remember: "Not Found" is always better than guessing.
"""

    try:
        result = structured_llm.invoke(prompt)
        return {"company_data": result.model_dump()}
    except Exception as e:
        return {
            "company_data": CompanyData().model_dump(),
            "errors": [f"Corporate Profiler error: {str(e)}"],
        }
