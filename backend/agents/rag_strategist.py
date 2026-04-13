"""
rag_strategist.py — Agent 4: RAG Strategist

Compares competitor weaknesses (from Agent 3's reviews) against
our own product strengths using ChromaDB vector store.
"""

from langchain_openai import ChatOpenAI

from backend.config import settings
from backend.rag.store import VectorStore
from backend.schemas import ComparisonData, PipelineState


def rag_strategist_node(state: PipelineState) -> dict:
    """
    Agent 4: RAG-based competitive comparison.

    Reads: state["inputs"], state["reviews"], state["product_data"]
    Writes: state["comparison"]
    """
    inputs = state["inputs"]
    product_name = inputs.get("target_product", "")
    company_name = inputs.get("name", "")

    reviews = state.get("reviews", {})
    product_data = state.get("product_data", {})

    # ── Step 1: Check if RAG store has documents ───────────────
    store = VectorStore.get_instance()
    doc_count = store.count()

    if doc_count == 0:
        return {
            "comparison": ComparisonData(
                rag_context_available=False,
                wins=[],
                losses=[],
                neutral=[],
                win_rate=0.0,
            ).model_dump(),
        }

    # ── Step 2: Extract competitor pain points for querying ────
    negative_reviews = reviews.get("top_negative_reviews", [])
    hidden_frictions = product_data.get("hidden_frictions", [])

    pain_points = []
    for review in negative_reviews:
        if isinstance(review, dict):
            pain_points.append(review.get("verbatim_quote", ""))
    for friction in hidden_frictions:
        if isinstance(friction, dict):
            pain_points.append(friction.get("friction", ""))

    # ── Step 3: Query our product docs for each pain point ─────
    rag_context_parts = []
    for point in pain_points[:8]:  # Limit queries to avoid overload
        if not point:
            continue
        results = store.query(point, n_results=3)
        docs = results.get("documents", [[]])[0]
        if docs:
            rag_context_parts.append(
                f"Competitor weakness: {point}\n"
                f"Our relevant docs: {' | '.join(docs)}"
            )

    # Also do a general query
    general_results = store.query(
        f"{product_name} vs our product comparison strengths", n_results=5
    )
    general_docs = general_results.get("documents", [[]])[0]
    if general_docs:
        rag_context_parts.append(
            f"General our product info: {' | '.join(general_docs)}"
        )

    rag_context = "\n\n".join(rag_context_parts)

    # ── Step 4: LLM comparison ─────────────────────────────────
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )
    structured_llm = llm.with_structured_output(ComparisonData)

    # Build competitor summary
    competitor_pricing = product_data.get("pricing_tiers", [])
    pricing_summary = ""
    for tier in competitor_pricing:
        if isinstance(tier, dict):
            pricing_summary += f"  - {tier.get('tier_name', '?')}: {tier.get('price', '?')}\n"

    prompt = f"""You are a competitive intelligence strategist. Compare the competitor
"{product_name}" by "{company_name}" against OUR product using the RAG context below.

CRITICAL RULES:
- A "win" means OUR product is BETTER than the competitor in that area.
- A "loss" means the COMPETITOR is BETTER than us in that area.
- A "neutral" means both are roughly equivalent.
- Use specific evidence from both the competitor data and our product docs.
- Include impact level (High/Medium/Low) for each comparison point.
- Calculate win_rate as: wins / (wins + losses + neutral).
- Set rag_context_available to true.
- If evidence is insufficient for a comparison, do NOT include it.

=== COMPETITOR NEGATIVE REVIEWS ===
{chr(10).join(r.get('verbatim_quote', '') for r in negative_reviews[:10] if isinstance(r, dict))}

=== COMPETITOR HIDDEN FRICTIONS ===
{chr(10).join(f.get('friction', '') for f in hidden_frictions if isinstance(f, dict))}

=== COMPETITOR PRICING ===
{pricing_summary}

=== OUR PRODUCT DOCS (from RAG) ===
{rag_context[:6000]}

Generate the competitive comparison now.
"""

    try:
        result = structured_llm.invoke(prompt)
        return {"comparison": result.model_dump()}
    except Exception as e:
        return {
            "comparison": ComparisonData(rag_context_available=doc_count > 0).model_dump(),
            "errors": [f"RAG Strategist error: {str(e)}"],
        }
