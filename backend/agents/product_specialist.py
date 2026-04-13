"""
product_specialist.py — Agent 2: Product Specialist

Deep-dives into the specific product: pricing tiers, specs,
hidden frictions, integrations, and delivery details.
"""

from langchain_openai import ChatOpenAI

from backend.config import settings
from backend.schemas import PipelineState, ProductData
from backend.tools.scrape import scrape_url
from backend.tools.search import search_product_info


def product_specialist_node(state: PipelineState) -> dict:
    """
    Agent 2: Extract deep product intelligence.

    Reads: state["inputs"], state["classifier"]
    Writes: state["product_data"]
    """
    inputs = state["inputs"]
    product_name = inputs.get("target_product", "")
    company_name = inputs.get("name", "")
    url = inputs.get("url", "")
    focus = inputs.get("focus_area", "")

    # ── Step 1: Scrape the product URL ─────────────────────────
    scraped_content = ""
    if url:
        scraped_content = scrape_url(url)
        if len(scraped_content) > 10000:
            scraped_content = scraped_content[:10000] + "\n...[truncated]"

    # ── Step 2: Search for pricing and specs ───────────────────
    search_results = search_product_info(product_name, company_name)

    # ── Step 3: LLM extraction ─────────────────────────────────
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )
    structured_llm = llm.with_structured_output(ProductData)

    prompt = f"""You are a product intelligence specialist. Extract deep, high-density
product data for "{product_name}" by "{company_name}".

CRITICAL RULES:
- Extract SPECIFIC numbers, not vague descriptions (e.g., "$12.50/user/month" not "affordable").
- For pricing tiers: get exact names, prices, billing models, features, and limitations per tier.
- For hidden frictions: look for costs/limitations the marketing doesn't highlight, such as:
  * Extra charges for API access, premium support, or add-ons
  * Storage limits, user caps, or rate limits
  * Requirements like "requires specific hardware" or "needs additional purchase"
  * Lock-in mechanisms or difficult cancellation processes
- For specs: extract technical specifications as concrete key-value pairs.
- If data is not found, use "Not Found" — do NOT guess or hallucinate.
{f'- Pay special attention to: {focus}' if focus else ''}

=== SCRAPED PRODUCT PAGE ===
{scraped_content[:6000]}

=== WEB SEARCH RESULTS ===
{search_results[:6000]}

Extract all product data now. Be thorough with hidden frictions — sales reps need these.
"""

    try:
        result = structured_llm.invoke(prompt)
        return {"product_data": result.model_dump()}
    except Exception as e:
        return {
            "product_data": ProductData().model_dump(),
            "errors": [f"Product Specialist error: {str(e)}"],
        }
