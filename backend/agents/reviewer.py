"""
reviewer.py — Agent 3: The Reviewer

Scrapes reviews from recommended sources (Reddit, G2, Amazon, etc.),
extracts YouTube transcript summaries, and produces exactly 3 positive
and 10 negative verbatim reviews with sentiment analysis.
"""

from langchain_openai import ChatOpenAI

from backend.config import settings
from backend.schemas import PipelineState, ReviewData
from backend.tools.search import search_reviews, search_youtube_reviews


def reviewer_node(state: PipelineState) -> dict:
    """
    Agent 3: Gather and analyze product reviews.

    Reads: state["inputs"], state["classifier"]
    Writes: state["reviews"]
    """
    inputs = state["inputs"]
    product_name = inputs.get("target_product", "")
    company_name = inputs.get("name", "")
    focus = inputs.get("focus_area", "")

    classifier = state.get("classifier", {})
    sources = classifier.get("recommended_sources", ["Google", "Reddit"])

    # ── Step 1: Search reviews from recommended sources ────────
    review_results = search_reviews(product_name, sources)

    # ── Step 2: Search YouTube reviews ─────────────────────────
    youtube_results = search_youtube_reviews(product_name)

    # ── Step 3: LLM synthesis ──────────────────────────────────
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )
    structured_llm = llm.with_structured_output(ReviewData)

    prompt = f"""You are a review intelligence analyst. Analyze all reviews for
"{product_name}" by "{company_name}" and produce a structured review report.

CRITICAL RULES:
1. VERBATIM QUOTES: Each review must contain an exact or near-exact quote from the source.
   Do NOT paraphrase or summarize — use the actual reviewer's words.
2. Produce EXACTLY 3 positive reviews — choose the most impactful/specific ones.
3. Produce EXACTLY 10 negative reviews — focus on specific "pain points" that a sales
   rep can use as ammunition. Vague complaints like "it's bad" are not useful.
4. For each review: include source, author (if available), date, verbatim quote,
   sentiment score (-1 to +1), and a one-word key theme.
5. For YouTube summaries: extract 3-5 key points and the reviewer's overall verdict.
6. Calculate overall_sentiment as a float 0-1 based on the ratio of positive to
   negative reviews found. Provide a sentiment_label.
7. If you cannot find enough reviews, fill remaining slots with the best available
   and note the source as "Limited data available".
{f'8. Pay special attention to reviews mentioning: {focus}' if focus else ''}

=== REVIEW SEARCH RESULTS ===
{review_results[:8000]}

=== YOUTUBE REVIEW RESULTS ===
{youtube_results[:4000]}

Extract and structure the reviews now. Remember: VERBATIM quotes only.
"""

    try:
        result = structured_llm.invoke(prompt)
        return {"reviews": result.model_dump()}
    except Exception as e:
        return {
            "reviews": ReviewData().model_dump(),
            "errors": [f"Reviewer error: {str(e)}"],
        }
