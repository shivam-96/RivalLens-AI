"""
store.py — ChromaDB vector store manager.

Manages the local persistent vector store for RAG-based comparisons.
Uses sentence-transformers for local embedding generation.
"""

import chromadb
from chromadb.utils import embedding_functions

from backend.config import settings


class VectorStore:
    """Singleton-style ChromaDB manager for our product docs."""

    _instance = None
    _client = None
    _collection = None

    @classmethod
    def get_instance(cls) -> "VectorStore":
        if cls._instance is None:
            cls._instance = VectorStore()
        return cls._instance

    def __init__(self):
        self._client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self._emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            embedding_function=self._emb_fn,
        )

    @property
    def collection(self):
        return self._collection

    def add_documents(
        self,
        documents: list[str],
        metadatas: list[dict] | None = None,
        ids: list[str] | None = None,
    ) -> int:
        """
        Add documents to the vector store.
        Returns the new total count.
        """
        if not documents:
            return self.count()

        if ids is None:
            existing_count = self.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(documents))]

        if metadatas is None:
            metadatas = [{"source": "uploaded"} for _ in documents]

        self._collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
        return self.count()

    def query(self, query_text: str, n_results: int = 5) -> dict:
        """
        Query the vector store for similar documents.
        Returns ChromaDB query results dict.
        """
        if self.count() == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        return self._collection.query(
            query_texts=[query_text],
            n_results=min(n_results, self.count()),
        )

    def count(self) -> int:
        """Return the number of documents in the collection."""
        return self._collection.count()

    def reset(self):
        """Delete and recreate the collection (for testing)."""
        self._client.delete_collection(settings.CHROMA_COLLECTION)
        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            embedding_function=self._emb_fn,
        )
