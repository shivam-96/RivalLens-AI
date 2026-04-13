"""
main.py — FastAPI application entry point.

Exposes the Sales Intelligence Pipeline via REST endpoints.
"""

import json
import os
import re
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import settings
from backend.graph import pipeline
from backend.rag.ingest import ingest_mock_product_docs, ingest_text
from backend.schemas import PipelineInputs

# ── FastAPI App ────────────────────────────────────────────────
app = FastAPI(
    title="Sales Intelligence Pipeline",
    description="Universal Sales Intelligence Pipeline — Zero Research for Sales Reps",
    version="1.0.0",
)

# CORS for frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request/Response Models ────────────────────────────────────

class UploadDocsRequest(BaseModel):
    text: str
    source: str = "manual_upload"


class UploadDocsResponse(BaseModel):
    message: str
    total_documents: int


class PipelineResponse(BaseModel):
    status: str
    battle_card: dict
    saved_to: str
    errors: list[str]


# ── Endpoints ──────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "pipeline_version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/run-pipeline", response_model=PipelineResponse)
async def run_pipeline(inputs: PipelineInputs):
    """
    Run the full Sales Intelligence Pipeline.
    
    Accepts competitor inputs, runs all 6 agents, saves the battle card
    as a JSON file, and returns the result.
    """
    try:
        # Prepare initial state
        initial_state = {
            "inputs": inputs.model_dump(),
            "errors": [],
        }

        # Run the pipeline
        result = pipeline.invoke(initial_state)

        # Extract battle card and errors
        battle_card = result.get("battle_card", {})
        errors = result.get("errors", [])

        # Save to file
        safe_name = re.sub(r'[^\w\-]', '_', inputs.name.lower())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.json"
        filepath = os.path.join(settings.OUTPUT_DIR, filename)

        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(battle_card, f, indent=2, ensure_ascii=False)

        return PipelineResponse(
            status="success",
            battle_card=battle_card,
            saved_to=filepath,
            errors=errors if errors else [],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline execution failed: {str(e)}",
        )


@app.post("/upload-docs", response_model=UploadDocsResponse)
async def upload_docs(request: UploadDocsRequest):
    """
    Upload product documentation for RAG-based comparison.
    Text is chunked and stored in ChromaDB.
    """
    try:
        total = ingest_text(request.text, source=request.source)
        return UploadDocsResponse(
            message="Documents ingested successfully",
            total_documents=total,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(e)}",
        )


@app.post("/load-mock-docs")
async def load_mock_docs():
    """
    Load mock product documentation for demo purposes.
    Seeds ChromaDB with sample 'our product' docs.
    """
    try:
        total = ingest_mock_product_docs()
        return {
            "message": "Mock product docs loaded successfully",
            "total_documents": total,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Mock docs loading failed: {str(e)}",
        )


# ── Startup Event ──────────────────────────────────────────────

@app.on_event("startup")
async def startup_event():
    """Load mock docs on startup if the store is empty."""
    from backend.rag.store import VectorStore

    store = VectorStore.get_instance()
    if store.count() == 0:
        print("[INFO] ChromaDB empty - loading mock product docs...")
        total = ingest_mock_product_docs()
        print(f"[OK] Loaded {total} document chunks into ChromaDB")
    else:
        print(f"[OK] ChromaDB ready with {store.count()} document chunks")
