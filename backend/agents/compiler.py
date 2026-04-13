"""
compiler.py — Agent 5: The Compiler

Synthesizes all gathered intelligence into the final Sales Battle Card.
Generates objection handlers, battle card snippets, and an elevator pitch.
"""

from datetime import datetime

from langchain_openai import ChatOpenAI

from backend.config import settings
from backend.schemas import BattleCard, PipelineInputs, PipelineState, TacticsData
from backend.schemas import (
    ClassifierOutput,
    CompanyData,
    ComparisonData,
    ProductData,
    ReviewData,
)


def compiler_node(state: PipelineState) -> dict:
    """
    Agent 5: Compile the final Battle Card.

    Reads: ALL state fields
    Writes: state["tactics"], state["battle_card"]
    """
    inputs = state.get("inputs", {})
    classifier = state.get("classifier", {})
    company_data = state.get("company_data", {})
    product_data = state.get("product_data", {})
    reviews = state.get("reviews", {})
    comparison = state.get("comparison", {})

    product_name = inputs.get("target_product", "")
    company_name = inputs.get("name", "")

    # ── Step 1: Generate tactics via LLM ───────────────────────
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0.2,  # Slightly creative for tactical responses
    )
    structured_llm = llm.with_structured_output(TacticsData)

    # Build a summary of all intelligence for context
    wins_summary = ""
    losses_summary = ""
    for w in comparison.get("wins", []):
        if isinstance(w, dict):
            wins_summary += f"  - {w.get('area', '?')}: {w.get('our_position', '')}\n"
    for l in comparison.get("losses", []):
        if isinstance(l, dict):
            losses_summary += f"  - {l.get('area', '?')}: {l.get('competitor_position', '')}\n"

    neg_reviews = ""
    for r in reviews.get("top_negative_reviews", [])[:5]:
        if isinstance(r, dict):
            neg_reviews += f"  - [{r.get('key_theme', '')}] {r.get('verbatim_quote', '')}\n"

    pricing_info = ""
    for tier in product_data.get("pricing_tiers", []):
        if isinstance(tier, dict):
            pricing_info += f"  - {tier.get('tier_name', '?')}: {tier.get('price', '?')}\n"

    frictions = ""
    for f in product_data.get("hidden_frictions", []):
        if isinstance(f, dict):
            frictions += f"  - {f.get('friction', '')}\n"

    prompt = f"""You are an elite sales strategist. Using ALL the competitive intelligence below,
generate tactical sales materials for reps selling AGAINST "{product_name}" by "{company_name}".

CRITICAL RULES:
1. Generate 5-8 objection handlers. Each must have:
   - A realistic objection a prospect might raise (e.g., "But {company_name} is cheaper")
   - A compelling response that uses SPECIFIC data points from the intelligence
   - Supporting data with exact numbers/quotes when available
2. Generate 6-10 battle card snippets — short, punchy talking points organized by category.
3. Write a 30-second elevator pitch that positions our product favorably against this competitor.
4. Be specific! Use actual pricing numbers, review quotes, and feature comparisons.
5. Tone: confident but not aggressive, data-driven, consultative.

=== COMPETITOR COMPANY ===
HQ: {company_data.get('headquarters', 'Not Found')}
Size: {company_data.get('employee_count', 'Not Found')}
Funding: {company_data.get('total_funding', 'Not Found')}

=== COMPETITOR PRICING ===
{pricing_info or 'Not Found'}

=== COMPETITOR HIDDEN FRICTIONS ===
{frictions or 'None found'}

=== OUR WINS vs COMPETITOR ===
{wins_summary or 'No comparison data available'}

=== OUR LOSSES vs COMPETITOR ===
{losses_summary or 'No comparison data available'}

=== TOP NEGATIVE REVIEWS OF COMPETITOR ===
{neg_reviews or 'No reviews available'}

=== REVIEW SENTIMENT ===
Overall: {reviews.get('overall_sentiment', 'N/A')} ({reviews.get('sentiment_label', 'N/A')})

Generate the sales tactics now. Make them actionable and data-rich.
"""

    try:
        tactics_result = structured_llm.invoke(prompt)
        tactics_dict = tactics_result.model_dump()
    except Exception as e:
        tactics_dict = TacticsData().model_dump()
        state_errors = state.get("errors", [])
        state_errors.append(f"Compiler tactics error: {str(e)}")

    # ── Step 2: Assemble the final Battle Card ─────────────────
    try:
        battle_card = BattleCard(
            generated_at=datetime.now().isoformat(),
            pipeline_version="1.0.0",
            inputs=PipelineInputs(**inputs),
            classifier=ClassifierOutput(**classifier),
            company_data=CompanyData(**company_data),
            product_data=ProductData(**product_data),
            reviews=ReviewData(**reviews),
            comparison=ComparisonData(**comparison),
            tactics=TacticsData(**tactics_dict),
        )
        battle_card_dict = battle_card.model_dump()
    except Exception as e:
        # If assembly fails, return what we have
        battle_card_dict = {
            "generated_at": datetime.now().isoformat(),
            "pipeline_version": "1.0.0",
            "inputs": inputs,
            "classifier": classifier,
            "company_data": company_data,
            "product_data": product_data,
            "reviews": reviews,
            "comparison": comparison,
            "tactics": tactics_dict,
            "assembly_error": str(e),
        }

    return {
        "tactics": tactics_dict,
        "battle_card": battle_card_dict,
    }
