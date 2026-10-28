# src/practo_agent/rag.py

import pathlib

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "chroma_data"

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

COLLECTIONS = {
    "fixed": "policy_fixed_chunks",
    "sentence": "policy_sentence_chunks",
}

DEFAULT_TOP_K = 5


class PolicyRAG:
    def __init__(
        self,
        strategy: str = "sentence",
        threshold: float | None = None,
        top_k: int = DEFAULT_TOP_K,
    ):
        if strategy not in COLLECTIONS:
            raise ValueError(
                f"Unknown strategy: {strategy}"
            )

        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        self.strategy = strategy
        self.threshold = threshold
        self.top_k = top_k

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_collection(
            COLLECTIONS[strategy]
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

    def retrieve(self, query: str) -> dict:
        """Retrieve relevant chunks and their cosine similarities."""
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty")

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(
                self.top_k,
                self.collection.count(),
            ),
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        retrieved = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved.append({
                "text": document,
                "parent_document_id": (
                    metadata["parent_document_id"]
                ),
                "chunk_index": metadata["chunk_index"],
                "distance": float(distance),
                "similarity": 1.0 - float(distance),
            })

        return {
            "query": query,
            "strategy": self.strategy,
            "results": retrieved,
            "top1_similarity": (
                retrieved[0]["similarity"]
                if retrieved else None
            ),
        }

    def answer(self, query: str) -> dict:
        """Return retrieved evidence or an explicit fallback."""
        result = self.retrieve(query)
        matches = result["results"]

        if not matches:
            return {
                "query": query,
                "answer": (
                    "I don't know based on the available "
                    "policy documents."
                ),
                "grounded": False,
                "reason": "no_retrieved_chunks",
                "evidence": [],
            }

        top1 = result["top1_similarity"]

        if self.threshold is None:
            raise RuntimeError(
                "A calibrated threshold is required before "
                "answering. Run the calibration script first."
            )

        if top1 < self.threshold:
            return {
                "query": query,
                "answer": (
                    "I don't know based on the available "
                    "policy documents. Please contact the "
                    "clinic for further assistance."
                ),
                "grounded": False,
                "reason": "below_similarity_threshold",
                "top1_similarity": top1,
                "evidence": [],
            }

        # Deterministic MOCK_LLM behavior:
        # return only retrieved policy text, without adding
        # unsupported facts or pretending a real LLM was called.
        evidence = []
        seen = set()

        for match in matches:
            parent_id = match["parent_document_id"]

            if parent_id not in seen:
                evidence.append({
                    "document_id": parent_id,
                    "text": match["text"],
                    "similarity": match["similarity"],
                })
                seen.add(parent_id)

        answer_text = "\n\n".join(
            item["text"] for item in evidence
        )

        return {
            "query": query,
            "answer": answer_text,
            "grounded": True,
            "reason": "retrieved_policy_evidence",
            "top1_similarity": top1,
            "evidence": evidence,
        }