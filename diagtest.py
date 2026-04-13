"""
diagtest.py — Quick API diagnostic for all 3 services.
Run: venv\Scripts\python.exe backend/diagtest.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
TAVILY_KEY = os.getenv("TAVILY_API_KEY", "")
FIRECRAWL_KEY = os.getenv("FIRECRAWL_API_KEY", "")

print("=" * 50)
print("API KEY CHECK")
print("=" * 50)
print(f"OpenAI   : {OPENAI_KEY[:20]}..." if len(OPENAI_KEY) > 20 else f"OpenAI   : {OPENAI_KEY!r} (MISSING!)")
print(f"Tavily   : {TAVILY_KEY[:20]}..." if len(TAVILY_KEY) > 20 else f"Tavily   : {TAVILY_KEY!r} (MISSING!)")
print(f"Firecrawl: {FIRECRAWL_KEY[:20]}..." if len(FIRECRAWL_KEY) > 20 else f"Firecrawl: {FIRECRAWL_KEY!r} (MISSING!)")

# --- Test 1: OpenAI ---
print("\n[1/3] Testing OpenAI...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Reply with just: OK"}],
        max_tokens=5,
    )
    print(f"  PASS: {resp.choices[0].message.content.strip()}")
except Exception as e:
    print(f"  FAIL: {e}")

# --- Test 2: Tavily ---
print("\n[2/3] Testing Tavily Search...")
try:
    from tavily import TavilyClient
    tc = TavilyClient(api_key=TAVILY_KEY)
    res = tc.search("Udemy company headquarters", max_results=1)
    results = res.get("results", [])
    if results:
        print(f"  PASS: Got result — '{results[0].get('title', '')[:60]}'")
    else:
        print("  WARN: No results returned")
except Exception as e:
    print(f"  FAIL: {e}")

# --- Test 3: Firecrawl ---
print("\n[3/3] Testing Firecrawl Scrape...")
try:
    from firecrawl import FirecrawlApp
    fc = FirecrawlApp(api_key=FIRECRAWL_KEY)
    result = fc.scrape("https://www.udemy.com", formats=["markdown"])
    content = result.get("markdown", "") if isinstance(result, dict) else getattr(result, "markdown", str(result))
    if content and len(content) > 100:
        print(f"  PASS: Scraped {len(content)} chars. Preview: '{content[:80]}'")
    else:
        print(f"  WARN: Short/empty content: {content[:100]!r}")
except Exception as e:
    print(f"  FAIL: {e}")

print("\n" + "=" * 50)
print("DONE")
