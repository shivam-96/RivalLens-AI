"""
classifier.py — Agent 0: The Classifier

Analyzes the input category and determines which data sources and
search queries to use for subsequent agents.
"""

from langchain_openai import ChatOpenAI

from backend.config import settings
from backend.schemas import ClassifierOutput, PipelineState


# Source mappings by category
SOURCE_MAP = {
    "Software": [
        "G2",
        "Capterra",
        "ProductHunt",
        "Reddit/r/SaaS",
        "Reddit/r/software",
        "TrustRadius",
    ],
    "Physical": [
        "Amazon",
        "Walmart",
        "YouTube",
        "Reddit/r/BuyItForLife",
        "Reddit/r/reviews",
        "ConsumerReports",
    ],
    "Course": [
        "Udemy",
        "Coursera",
        "Reddit/r/learnprogramming",
        "Reddit/r/OnlineEducation",
        "YouTube",
        "ClassCentral",
    ],
    "Entertainment": [
        "YouTube",
        "Metacritic",
        "Reddit/r/gaming",
        "Reddit/r/movies",
        "Reddit/r/entertainment",
        "IMDb",
    ],
}


def classify_node(state: PipelineState) -> dict:
    """
    Agent 0: Classify the input and generate source recommendations.
    
    Reads: state["inputs"]
    Writes: state["classifier"]
    """
    inputs = state["inputs"]
    category = inputs.get("category", "Software")
    product = inputs.get("target_product", "")
    company = inputs.get("name", "")
    focus = inputs.get("focus_area", "")

    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )
    structured_llm = llm.with_structured_output(ClassifierOutput)

    prompt = f"""You are a research classifier for a competitive intelligence pipeline.

Given the following inputs:
- Company: {company}
- Product: {product}
- Category: {category}
- Focus Area: {focus or 'None specified'}

The default recommended sources for '{category}' are: {SOURCE_MAP.get(category, SOURCE_MAP['Software'])}

Your tasks:
1. Confirm the category label.
2. Return the recommended sources list — you may reorder or add sources based on the specific product.
3. Generate 5-8 specific search queries that subsequent agents should use to find:
   - Company funding and corporate data
   - Product pricing and technical specifications
   - User reviews (positive and negative)
   - YouTube review content
   
Make queries as specific as possible using the actual product and company names.
If a focus area is specified, include 2-3 queries specifically targeting that area.
"""

    try:
        result = structured_llm.invoke(prompt)
        return {"classifier": result.model_dump()}
    except Exception as e:
        # Fallback: return defaults without LLM
        return {
            "classifier": ClassifierOutput(
                category_label=category,
                recommended_sources=SOURCE_MAP.get(category, SOURCE_MAP["Software"]),
                search_queries=[
                    f"{company} {product} pricing",
                    f"{company} funding investors",
                    f"{product} review pros cons",
                    f"{product} YouTube review",
                    f"{company} headquarters employees",
                ],
            ).model_dump(),
            "errors": [f"Classifier LLM error (used fallback): {str(e)}"],
        }
