"""
Configuration module — loads environment variables and exposes settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY", "")

    OPENAI_MODEL: str = "gpt-4o"
    CHROMA_DB_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db"
    )
    CHROMA_COLLECTION: str = "our_product_docs"
    OUTPUT_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

    # Ensure output dir exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)


settings = Settings()
