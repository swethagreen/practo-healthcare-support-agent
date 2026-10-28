
from pathlib import Path

import chromadb
import sentence_transformers

import practo_agent.chunking

import practo_agent.sentenechunking

# Project root: practo-healthcare-support-agent/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"
CHROMA_DIR = PROJECT_ROOT / "chroma_data"

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


def load_policy_documents(
    directory: Path = KNOWLEDGE_BASE_DIR,
) -> dict[str, str]:
    """Load every non-empty policy .txt file.

    Returns:
        Dictionary mapping document IDs to document text.
    """
    if not directory.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {directory}"
        )

    files = sorted(directory.glob("*.txt"))

    if not files:
        raise ValueError(
            f"No policy .txt files found in {directory}"
        )

    documents = {}

    for file_path in files:
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            raise ValueError(
                f"Policy document is empty: {file_path.name}"
            )

        # Stable parent document ID based on the filename.
        documents[file_path.stem] = text

    return documents


def index_chunks(
    collection,
    documents: dict[str, str],
    chunker,
    strategy: str,
    embedding_model: sentence_transformers.SentenceTransformer,
) -> int:
    """Chunk, embed, and upsert documents into a collection.

    Each chunk stores its parent document ID and chunk index.
    Returns the number of indexed chunks.
    """
    ids = []
    texts = []
    metadatas = []

    for document_id, document_text in sorted(
        documents.items()
    ):
        chunks = chunker(document_text)

        for chunk_index, chunk in enumerate(chunks):
            chunk = chunk.strip()

            if not chunk:
                continue

            # Unique within this strategy's collection.
            chunk_id = (
                f"{document_id}_{strategy}_{chunk_index:04d}"
            )

            ids.append(chunk_id)
            texts.append(chunk)

            metadatas.append({
                "parent_document_id": document_id,
                "chunk_index": chunk_index,
                "strategy": strategy,
            })

    if not texts:
        raise ValueError(
            f"No chunks generated for strategy: {strategy}"
        )

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).tolist()

    # Upsert ensures that repeated IDs are updated, not duplicated.
    # Process in batches to avoid oversized database requests.
    batch_size = 100

    for start in range(0, len(ids), batch_size):
        end = start + batch_size

        collection.upsert(
            ids=ids[start:end],
            documents=texts[start:end],
            embeddings=embeddings[start:end],
            metadatas=metadatas[start:end],
        )

    return len(ids)


def build_indexes():
    """Build independent fixed-size and sentence-based indexes."""
    documents = load_policy_documents()

    print(f"Loaded {len(documents)} policy documents.")

    # Load the embedding model once and reuse it for both indexes.
    embedding_model = sentence_transformers.SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Rebuild cleanly to prevent stale chunks when source documents
    # or chunking parameters change.
    collection_names = [
        "policy_fixed_chunks",
        "policy_sentence_chunks",
    ]

    for name in collection_names:
        try:
            client.delete_collection(name)
        except Exception:
            # A collection may not exist on the first run.
            pass

    fixed_collection = client.create_collection(
        name="policy_fixed_chunks",
        metadata={"hnsw:space": "cosine"},
    )

    sentence_collection = client.create_collection(
        name="policy_sentence_chunks",
        metadata={"hnsw:space": "cosine"},
    )

    # Strategy 1: fixed-size chunks with overlap.
    fixed_count = index_chunks(
        collection=fixed_collection,
        documents=documents,
        chunker=practo_agent.chunking.fixed_size_chunks,
        strategy="fixed",
        embedding_model=embedding_model,
    )

    # Strategy 2: sentence-based chunks.
    sentence_count = index_chunks(
        collection=sentence_collection,
        documents=documents,
        chunker=practo_agent.sentenechunking.sentence_chunks,
        strategy="sentence",
        embedding_model=embedding_model,
    )

    print("\nIndexing complete.")
    print(f"Policy documents: {len(documents)}")
    print(f"Fixed-size chunks: {fixed_count}")
    print(f"Sentence-based chunks: {sentence_count}")
    print(f"Fixed collection: {fixed_collection.name}")
    print(f"Sentence collection: {sentence_collection.name}")
    print(f"Persistent database: {CHROMA_DIR}")


if __name__ == "__main__":
    build_indexes()
