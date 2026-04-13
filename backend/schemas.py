"""
schemas.py — All Pydantic models for the Sales Intelligence Pipeline.

This file defines:
  1. Input models (what the user provides)
  2. Intermediate agent output models (what each agent produces)
  3. The final BattleCard composite output
  4. The LangGraph PipelineState (TypedDict for state tracking)
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field
from typing_extensions import TypedDict


# ─────────────────────────────────────────────
# 1. ENUMS
# ─────────────────────────────────────────────

class CategoryEnum(str, enum.Enum):
    """Supported product/company categories."""
    SOFTWARE = "Software"
    PHYSICAL = "Physical"
    COURSE = "Course"
    ENTERTAINMENT = "Entertainment"


# ─────────────────────────────────────────────
# 2. PIPELINE INPUTS
# ─────────────────────────────────────────────

class PipelineInputs(BaseModel):
    """Validated user inputs to kick off the pipeline."""
    name: str = Field(
        ...,
        description="Competitor company or brand name.",
        examples=["Slack", "Dyson"],
    )
    url: str = Field(
        ...,
        description="URL of the competitor's main product page.",
        examples=["https://slack.com/pricing"],
    )
    target_product: str = Field(
        ...,
        description="The specific product to research.",
        examples=["Slack Pro", "Dyson V15 Detect"],
    )
    category: CategoryEnum = Field(
        ...,
        description="Product category — determines which review sources the pipeline uses.",
    )
    focus_area: Optional[str] = Field(
        default=None,
        description="Optional focus area for the analysis (e.g., 'enterprise security', 'battery life').",
    )


# ─────────────────────────────────────────────
# 3. AGENT 0 — CLASSIFIER OUTPUT
# ─────────────────────────────────────────────

class ClassifierOutput(BaseModel):
    """Output of Agent 0: which tool sources to prioritize."""
    category_label: str = Field(
        ...,
        description="Confirmed category label (e.g., 'Software', 'Physical').",
    )
    recommended_sources: list[str] = Field(
        ...,
        description="Ordered list of review/data sources to use (e.g., ['G2', 'Capterra', 'Reddit/r/SaaS']).",
    )
    search_queries: list[str] = Field(
        ...,
        description="Pre-generated search queries tailored to the category and product.",
    )


# ─────────────────────────────────────────────
# 4. AGENT 1 — CORPORATE PROFILER OUTPUT
# ─────────────────────────────────────────────

class FundingRound(BaseModel):
    """A single funding round."""
    round_name: str = Field(
        default="Not Found",
        description="Funding round label (e.g., 'Series B', 'Seed').",
    )
    amount: str = Field(
        default="Not Found",
        description="Amount raised (e.g., '$50M').",
    )
    date: str = Field(
        default="Not Found",
        description="Date of the round.",
    )
    lead_investors: list[str] = Field(
        default_factory=list,
        description="Names of lead investors.",
    )


class NewsItem(BaseModel):
    """A recent news headline about the company."""
    title: str = Field(..., description="Headline text.")
    source: str = Field(default="Not Found", description="Publication name.")
    date: str = Field(default="Not Found", description="Publication date.")
    url: str = Field(default="", description="Link to the article.")
    summary: str = Field(default="", description="One-sentence summary.")


class CompanyData(BaseModel):
    """Comprehensive corporate intelligence on the competitor."""
    headquarters: str = Field(
        default="Not Found",
        description="Company HQ location (city, state/country).",
    )
    employee_count: str = Field(
        default="Not Found",
        description="Approximate number of employees (e.g., '5,000+').",
    )
    year_founded: str = Field(
        default="Not Found",
        description="Year the company was founded.",
    )
    total_funding: str = Field(
        default="Not Found",
        description="Total funding raised across all rounds.",
    )
    funding_rounds: list[FundingRound] = Field(
        default_factory=list,
        description="Detailed breakdown of each funding round.",
    )
    recent_news: list[NewsItem] = Field(
        default_factory=list,
        description="5 most recent news items about the company.",
    )
    all_products: list[str] = Field(
        default_factory=list,
        description="Complete list of all products/services the company offers.",
    )
    website_description: str = Field(
        default="Not Found",
        description="One-paragraph description of the company from their website.",
    )


# ─────────────────────────────────────────────
# 5. AGENT 2 — PRODUCT SPECIALIST OUTPUT
# ─────────────────────────────────────────────

class PricingTier(BaseModel):
    """A single pricing tier for a product."""
    tier_name: str = Field(..., description="Name of the tier (e.g., 'Pro', 'Enterprise').")
    price: str = Field(..., description="Price point (e.g., '$12.50/user/month').")
    billing_model: str = Field(
        default="Not Found",
        description="Subscription, one-time, freemium, etc.",
    )
    key_features: list[str] = Field(
        default_factory=list,
        description="Notable features included in this tier.",
    )
    limitations: list[str] = Field(
        default_factory=list,
        description="Limitations or caps of this tier.",
    )


class HiddenFriction(BaseModel):
    """A 'hidden' cost or friction point not obvious from marketing."""
    friction: str = Field(
        ...,
        description="The hidden friction (e.g., 'API access costs extra $99/month').",
    )
    source: str = Field(
        default="Product page",
        description="Where this was discovered.",
    )


class ProductData(BaseModel):
    """Deep product intelligence — pricing, specs, frictions."""
    pricing_tiers: list[PricingTier] = Field(
        default_factory=list,
        description="All pricing tiers with details.",
    )
    has_free_tier: bool = Field(
        default=False,
        description="Whether a free tier or trial exists.",
    )
    free_trial_duration: str = Field(
        default="Not Found",
        description="Duration of free trial if any.",
    )
    key_specifications: dict[str, str] = Field(
        default_factory=dict,
        description="Technical specifications as key-value pairs.",
    )
    delivery_onboarding: str = Field(
        default="Not Found",
        description="How the product is delivered/onboarded (e.g., 'cloud-hosted, 2-week onboarding').",
    )
    warranty_sla: str = Field(
        default="Not Found",
        description="Warranty or SLA details.",
    )
    hidden_frictions: list[HiddenFriction] = Field(
        default_factory=list,
        description="Hidden costs, frictions, or gotchas not obvious from marketing.",
    )
    integrations: list[str] = Field(
        default_factory=list,
        description="Key integrations or ecosystem connections.",
    )


# ─────────────────────────────────────────────
# 6. AGENT 3 — REVIEWER OUTPUT
# ─────────────────────────────────────────────

class ReviewItem(BaseModel):
    """A single review with verbatim quote."""
    source: str = Field(..., description="Where the review came from (e.g., 'Reddit', 'G2', 'Amazon').")
    author: str = Field(default="Anonymous", description="Reviewer name or handle.")
    date: str = Field(default="Not Found", description="Date of the review.")
    verbatim_quote: str = Field(
        ...,
        description="Exact quote from the reviewer — do NOT paraphrase.",
    )
    sentiment_score: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Sentiment score from -1 (very negative) to +1 (very positive).",
    )
    key_theme: str = Field(
        default="",
        description="One-word theme of this review (e.g., 'pricing', 'reliability').",
    )


class YouTubeSummary(BaseModel):
    """Summary of a YouTube review video transcript."""
    video_title: str = Field(..., description="Title of the YouTube video.")
    channel_name: str = Field(default="Not Found", description="YouTube channel name.")
    video_url: str = Field(default="", description="URL of the video.")
    key_points: list[str] = Field(
        default_factory=list,
        description="3-5 key points from the transcript.",
    )
    overall_verdict: str = Field(
        default="Not Found",
        description="The reviewer's overall verdict on the product.",
    )


class ReviewData(BaseModel):
    """Aggregated review intelligence."""
    top_positive_reviews: list[ReviewItem] = Field(
        default_factory=list,
        description="Exactly 3 most impactful positive reviews with verbatim quotes.",
        max_length=5,
    )
    top_negative_reviews: list[ReviewItem] = Field(
        default_factory=list,
        description="Exactly 10 most specific negative 'pain point' reviews.",
        max_length=15,
    )
    youtube_summaries: list[YouTubeSummary] = Field(
        default_factory=list,
        description="Summaries of up to 3 YouTube review videos.",
    )
    overall_sentiment: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Aggregated sentiment score from 0 (very negative) to 1 (very positive).",
    )
    sentiment_label: str = Field(
        default="Neutral",
        description="Human-readable sentiment label (e.g., 'Mostly Positive', 'Mixed').",
    )
    total_reviews_analyzed: int = Field(
        default=0,
        description="Total number of reviews analyzed to produce this summary.",
    )


# ─────────────────────────────────────────────
# 7. AGENT 4 — RAG STRATEGIST OUTPUT
# ─────────────────────────────────────────────

class ComparisonItem(BaseModel):
    """A single win or loss comparison point."""
    area: str = Field(
        ...,
        description="Feature or capability area (e.g., 'Integrations', 'Pricing').",
    )
    competitor_position: str = Field(
        ...,
        description="What the competitor offers or lacks in this area.",
    )
    our_position: str = Field(
        ...,
        description="What our product offers in this area.",
    )
    evidence: str = Field(
        default="",
        description="Supporting evidence (review quote, spec, or doc reference).",
    )
    impact: str = Field(
        default="Medium",
        description="Impact level: High, Medium, Low.",
    )


class ComparisonData(BaseModel):
    """RAG-based competitive comparison."""
    wins: list[ComparisonItem] = Field(
        default_factory=list,
        description="Areas where our product is stronger than the competitor.",
    )
    losses: list[ComparisonItem] = Field(
        default_factory=list,
        description="Areas where the competitor is stronger than our product.",
    )
    neutral: list[ComparisonItem] = Field(
        default_factory=list,
        description="Areas where both products are roughly equivalent.",
    )
    win_rate: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Percentage of comparison areas that are wins for us.",
    )
    rag_context_available: bool = Field(
        default=False,
        description="Whether internal product docs were available for comparison.",
    )


# ─────────────────────────────────────────────
# 8. AGENT 5 — COMPILER OUTPUT (TACTICS)
# ─────────────────────────────────────────────

class ObjectionHandler(BaseModel):
    """A single objection and the recommended response."""
    objection: str = Field(
        ...,
        description="Common sales objection (e.g., 'Their product is cheaper').",
    )
    response: str = Field(
        ...,
        description="Recommended response for the sales rep.",
    )
    supporting_data: str = Field(
        default="",
        description="Specific data point that backs up the response.",
    )


class BattleCardSnippet(BaseModel):
    """A quick-reference talking point for the sales rep."""
    title: str = Field(..., description="Short title (e.g., 'Price Advantage').")
    snippet: str = Field(
        ...,
        description="2-3 sentence talking point ready to use in a sales call.",
    )
    category: str = Field(
        default="General",
        description="Category: Pricing, Features, Support, Security, etc.",
    )


class TacticsData(BaseModel):
    """Sales tactics — objection handlers and quick snippets."""
    objection_handlers: list[ObjectionHandler] = Field(
        default_factory=list,
        description="5-8 objection-response pairs for common sales scenarios.",
    )
    battle_card_snippets: list[BattleCardSnippet] = Field(
        default_factory=list,
        description="Quick-reference talking points organized by category.",
    )
    elevator_pitch: str = Field(
        default="Not Found",
        description="A 30-second elevator pitch positioning our product against this competitor.",
    )


# ─────────────────────────────────────────────
# 9. FINAL COMPOSITE — BATTLE CARD
# ─────────────────────────────────────────────

class BattleCard(BaseModel):
    """
    The final output of the pipeline — a complete Sales Battle Card.
    Contains ALL intelligence gathered by all 6 agents.
    """
    # Metadata
    generated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO timestamp when this battle card was generated.",
    )
    pipeline_version: str = Field(
        default="1.0.0",
        description="Version of the pipeline that generated this card.",
    )

    # Inputs (echo back for reference)
    inputs: PipelineInputs

    # Agent outputs
    classifier: ClassifierOutput
    company_data: CompanyData
    product_data: ProductData
    reviews: ReviewData
    comparison: ComparisonData
    tactics: TacticsData


# ─────────────────────────────────────────────
# 10. LANGGRAPH PIPELINE STATE (TypedDict)
# ─────────────────────────────────────────────

class PipelineState(TypedDict, total=False):
    """
    LangGraph state container — each agent reads from and writes to this.

    Using TypedDict with total=False so agents can return partial updates.
    Each key corresponds to one agent's output section.
    """
    # User inputs (set once at the start)
    inputs: dict[str, Any]

    # Agent 0 output
    classifier: dict[str, Any]

    # Agent 1 output
    company_data: dict[str, Any]

    # Agent 2 output
    product_data: dict[str, Any]

    # Agent 3 output
    reviews: dict[str, Any]

    # Agent 4 output
    comparison: dict[str, Any]

    # Agent 5 output
    tactics: dict[str, Any]

    # Final assembled battle card
    battle_card: dict[str, Any]

    # Error tracking — any agent can append errors here
    errors: list[str]
