"""
ingest.py — Document ingestion logic for the RAG vector store.

Chunks text documents and adds them to ChromaDB.
"""

import re
import uuid
from datetime import datetime

from backend.rag.store import VectorStore


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks of approximately chunk_size characters.
    Splits on sentence boundaries where possible.
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep overlap from end of previous chunk
            words = current_chunk.split()
            overlap_words = words[-overlap // 5:] if len(words) > overlap // 5 else []
            current_chunk = " ".join(overlap_words) + " " + sentence
        else:
            current_chunk += " " + sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def ingest_text(
    text: str,
    source: str = "manual_upload",
    chunk_size: int = 500,
) -> int:
    """
    Ingest a text document into the vector store.
    Chunks the text and adds it with metadata.
    Returns the new total document count.
    """
    store = VectorStore.get_instance()
    chunks = chunk_text(text, chunk_size=chunk_size)

    if not chunks:
        return store.count()

    batch_id = uuid.uuid4().hex[:8]
    ids = [f"{batch_id}_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "source": source,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "ingested_at": datetime.now().isoformat(),
        }
        for i in range(len(chunks))
    ]

    return store.add_documents(documents=chunks, metadatas=metadatas, ids=ids)


def ingest_mock_product_docs() -> int:
    """
    Load mock product documentation for demo purposes.
    Simulates 'our product' docs for RAG comparison.
    """
    mock_docs = [
        """
        OurProduct Pro is an enterprise-grade project management and collaboration platform
        designed for teams of 10 to 10,000. Founded in 2019, we have served over 5,000
        companies globally. Our platform runs on AWS with 99.99% uptime SLA and SOC 2
        Type II certification.
        """,
        """
        Pricing: OurProduct offers three tiers — Starter ($8/user/month), Professional
        ($15/user/month), and Enterprise (custom pricing). All plans include unlimited
        projects, 100GB storage, and real-time collaboration. No hidden fees — API access
        is included in all paid plans at no extra cost.
        """,
        """
        Key Features: Real-time document collaboration, built-in video conferencing (no
        third-party needed), AI-powered task prioritization, native integrations with
        Salesforce, HubSpot, Jira, GitHub, and 200+ other tools. Custom workflow builder
        with drag-and-drop interface. Mobile apps for iOS and Android with offline support.
        """,
        """
        Security: End-to-end encryption for all data at rest and in transit. SAML SSO,
        SCIM provisioning, custom data residency options (US, EU, APAC). GDPR, HIPAA,
        and FedRAMP compliant. Annual third-party penetration testing.
        """,
        """
        Customer Support: 24/7 live chat and email support for all plans. Dedicated
        account manager for Enterprise customers. Average first response time: 4 minutes.
        Customer satisfaction score (CSAT): 4.8/5.0. Free onboarding assistance and
        migration support from competing platforms.
        """,
        """
        Performance: Sub-200ms page load times globally via CDN. Supports real-time
        collaboration with up to 500 simultaneous editors. 99.99% uptime over the last
        12 months. Automatic daily backups with 30-day retention. Zero data loss incidents
        since launch.
        """,
        """
        Customer Reviews Highlights: "Switched from Slack + Asana to OurProduct and saved
        40% on tool costs" — TechCorp CTO. "The AI task prioritization alone saved our
        team 6 hours per week" — Marketing Director at RetailCo. "Best customer support
        I've experienced in 20 years of enterprise software" — IT Manager at FinanceCo.
        """,
        """
        Weaknesses (internal honest assessment): Our mobile app can be slow on older
        devices. The learning curve for the custom workflow builder is steep for non-technical
        users. We don't yet support on-premise deployment. Our free tier is limited to
        5 users maximum, which is less generous than some competitors.
        """,
    ]

    total = 0
    for doc in mock_docs:
        total = ingest_text(doc.strip(), source="mock_product_docs")
    return total
