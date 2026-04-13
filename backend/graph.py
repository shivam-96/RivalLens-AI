"""
graph.py — LangGraph StateGraph definition.

Defines the sequential 6-agent pipeline:
  START → classifier → corporate_profiler → product_specialist
       → reviewer → rag_strategist → compiler → END
"""

from langgraph.graph import END, START, StateGraph

from backend.agents.classifier import classify_node
from backend.agents.compiler import compiler_node
from backend.agents.corporate_profiler import corporate_profiler_node
from backend.agents.product_specialist import product_specialist_node
from backend.agents.rag_strategist import rag_strategist_node
from backend.agents.reviewer import reviewer_node
from backend.schemas import PipelineState


def build_pipeline() -> StateGraph:
    """
    Build and compile the Sales Intelligence Pipeline graph.

    Returns a compiled LangGraph ready for .invoke() or .ainvoke().
    """
    graph = StateGraph(PipelineState)

    # ── Add nodes ──────────────────────────────────────────────
    graph.add_node("classifier", classify_node)
    graph.add_node("corporate_profiler", corporate_profiler_node)
    graph.add_node("product_specialist", product_specialist_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("rag_strategist", rag_strategist_node)
    graph.add_node("compiler", compiler_node)

    # ── Define sequential flow ─────────────────────────────────
    graph.add_edge(START, "classifier")
    graph.add_edge("classifier", "corporate_profiler")
    graph.add_edge("corporate_profiler", "product_specialist")
    graph.add_edge("product_specialist", "reviewer")
    graph.add_edge("reviewer", "rag_strategist")
    graph.add_edge("rag_strategist", "compiler")
    graph.add_edge("compiler", END)

    # ── Compile ────────────────────────────────────────────────
    compiled = graph.compile()
    return compiled


# Pre-built pipeline instance for import
pipeline = build_pipeline()
