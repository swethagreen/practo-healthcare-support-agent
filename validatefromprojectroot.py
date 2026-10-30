from pathlib import Path
import chromadb

client = chromadb.PersistentClient(
    path=str(Path("chroma_data").resolve())
)

for name in [
    "policy_fixed_chunks",
    "policy_sentence_chunks",
]:
    collection = client.get_collection(name)

    print(f"\nCollection: {name}")
    print(f"Chunk count: {collection.count()}")

    sample = collection.get(
        limit=2,
        include=["documents", "metadatas"],
    )

    for document, metadata in zip(
        sample["documents"],
        sample["metadatas"],
    ):
        print("Parent:", metadata["parent_document_id"])
        print("Strategy:", metadata["strategy"])
        print("Text:", document[:100])
        print("Meatadata:",metadata)