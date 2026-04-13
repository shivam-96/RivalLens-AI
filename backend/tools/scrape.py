"""
scrape.py — Firecrawl scraping wrapper for the pipeline.

Provides URL scraping with fallback error handling.
"""

from firecrawl import FirecrawlApp

from backend.config import settings


def _get_client() -> FirecrawlApp:
    return FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)


def scrape_url(url: str) -> str:
    """
    Scrape a URL and return its content as cleaned markdown.
    Falls back to an error message if scraping fails.
    """
    try:
        app = _get_client()
        result = app.scrape(url, formats=["markdown"])
        if isinstance(result, dict):
            return result.get("markdown", result.get("content", str(result)))
        # New SDK returns an object with attributes
        if hasattr(result, "markdown") and result.markdown:
            return result.markdown
        return str(result)
    except Exception as e:
        return f"[Scrape error for {url}]: {str(e)}"


def scrape_url_html(url: str) -> str:
    """
    Scrape a URL and return raw HTML for deeper parsing.
    """
    try:
        app = _get_client()
        result = app.scrape(url, formats=["html"])
        if isinstance(result, dict):
            return result.get("html", result.get("content", str(result)))
        if hasattr(result, "html") and result.html:
            return result.html
        return str(result)
    except Exception as e:
        return f"[HTML scrape error for {url}]: {str(e)}"
