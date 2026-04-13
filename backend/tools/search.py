"""
search.py — Tavily search wrapper for the pipeline.

Provides high-level search functions tailored to each agent's needs.
"""

from tavily import TavilyClient

from backend.config import settings


def _get_client() -> TavilyClient:
    return TavilyClient(api_key=settings.TAVILY_API_KEY)


def search_company_info(company_name: str) -> str:
    """
    Search for corporate intelligence: funding, HQ, size, products.
    Returns concatenated search result content.
    """
    client = _get_client()
    queries = [
        f"{company_name} company funding crunchbase investors headquarters",
        f"{company_name} number of employees company size founded year",
        f"{company_name} all products services offered",
    ]
    all_content = []
    for query in queries:
        try:
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
            )
            for result in response.get("results", []):
                all_content.append(
                    f"[{result.get('title', 'No title')}] ({result.get('url', '')})\n"
                    f"{result.get('content', '')}"
                )
        except Exception as e:
            all_content.append(f"[Search error for '{query}']: {str(e)}")

    return "\n\n---\n\n".join(all_content)


def search_product_info(product_name: str, company_name: str) -> str:
    """
    Search for product-specific data: pricing, specs, frictions.
    """
    client = _get_client()
    queries = [
        f"{product_name} {company_name} pricing tiers plans cost",
        f"{product_name} specifications features integrations",
        f"{product_name} hidden costs limitations gotchas",
    ]
    all_content = []
    for query in queries:
        try:
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
            )
            for result in response.get("results", []):
                all_content.append(
                    f"[{result.get('title', 'No title')}]\n{result.get('content', '')}"
                )
        except Exception as e:
            all_content.append(f"[Search error]: {str(e)}")

    return "\n\n---\n\n".join(all_content)


def search_reviews(
    product_name: str,
    sources: list[str],
) -> str:
    """
    Search for reviews from the recommended sources.
    """
    client = _get_client()
    all_content = []

    for source in sources[:5]:  # Limit to 5 source searches
        query = f"{product_name} review {source} pros cons"
        try:
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=3,
            )
            for result in response.get("results", []):
                all_content.append(
                    f"[{source} — {result.get('title', '')}]\n{result.get('content', '')}"
                )
        except Exception as e:
            all_content.append(f"[Review search error for {source}]: {str(e)}")

    return "\n\n---\n\n".join(all_content)


def search_youtube_reviews(product_name: str) -> str:
    """
    Search for YouTube review summaries and transcripts.
    """
    client = _get_client()
    try:
        response = client.search(
            query=f"{product_name} YouTube review transcript summary",
            search_depth="advanced",
            max_results=5,
        )
        contents = []
        for result in response.get("results", []):
            contents.append(
                f"[{result.get('title', '')}] ({result.get('url', '')})\n"
                f"{result.get('content', '')}"
            )
        return "\n\n---\n\n".join(contents)
    except Exception as e:
        return f"[YouTube search error]: {str(e)}"


def search_recent_news(company_name: str) -> str:
    """
    Search for recent news about the company.
    """
    client = _get_client()
    try:
        response = client.search(
            query=f"{company_name} latest news announcements 2024 2025",
            topic="news",
            max_results=5,
        )
        contents = []
        for result in response.get("results", []):
            contents.append(
                f"[{result.get('title', '')}] ({result.get('url', '')})\n"
                f"Published: {result.get('published_date', 'Unknown')}\n"
                f"{result.get('content', '')}"
            )
        return "\n\n---\n\n".join(contents)
    except Exception as e:
        return f"[News search error]: {str(e)}"
