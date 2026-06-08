"""Stage 4 of the RAG pipeline: Retrieval.

Embeds a user query with the same model that built the vector store, then asks
ChromaDB for the top-k most similar chunks.

Approach (from planning.md → Retrieval Approach):
    - Embedding model: all-MiniLM-L6-v2 (must match the storage stage)
    - Top-k:           4

Run this file directly to type a query and see what gets retrieved. The
embedding model and collection are loaded lazily and cached, so repeated
retrieve() calls in the same process don't reload them.
"""

import sys

import chromadb
from sentence_transformers import SentenceTransformer

from chunking import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL

TOP_K = 4  # planning.md → Retrieval Approach

# Lazily initialized, then reused across retrieve() calls.
_model: SentenceTransformer | None = None
_collection = None


def _get_model() -> SentenceTransformer:
    """Load the embedding model once and cache it."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection():
    """Connect to the persisted ChromaDB collection once and cache it."""
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        try:
            _collection = client.get_collection(COLLECTION_NAME)
        except Exception as exc:  # collection missing / db not built yet
            raise RuntimeError(
                f"Collection '{COLLECTION_NAME}' not found in {CHROMA_DIR}. "
                "Run chunking.py first to embed and store the chunks."
            ) from exc
    return _collection


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Return the top-k stored chunks most relevant to a query.

    Args:
        query:  The natural-language question to search for.
        top_k:  How many chunks to return (default 4, per the spec).

    Returns:
        A list of up to top_k chunk dicts, ordered most- to least-relevant,
        each with:
            - "text":        the chunk's stored text
            - "source":      originating document file name
            - "chunk_index": position of the chunk within its source
            - "chunk_id":    unique id ("<source>::<chunk_index>")
            - "distance":    cosine distance from the query (lower = closer)
            - "similarity":  cosine similarity, 1 - distance (higher = closer)
    """
    if not query.strip():
        raise ValueError("Query is empty.")

    model = _get_model()
    collection = _get_collection()

    # Embed the query the same way the stored chunks were embedded.
    query_embedding = model.encode(
        query, normalize_embeddings=True
    ).tolist()

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # Chroma nests results one level deep (one list per query); we sent one.
    ids = result["ids"][0]
    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]

    chunks: list[dict] = []
    for chunk_id, text, metadata, distance in zip(
        ids, documents, metadatas, distances
    ):
        chunks.append(
            {
                "text": text,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "chunk_id": chunk_id,
                "distance": distance,
                "similarity": 1 - distance,  # cosine space: sim = 1 - distance
            }
        )

    return chunks


if __name__ == "__main__":
    # Render curly quotes / dashes instead of crashing on the Windows console.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    query = input("Enter your query: ").strip()
    results = retrieve(query)

    print(f"\nRetrieved {len(results)} chunk(s) for: {query!r}\n")
    for rank, chunk in enumerate(results, start=1):
        preview = chunk["text"][:250].replace("\n", " ")
        print(f"#{rank}  similarity={chunk['similarity']:.4f}  "
              f"distance={chunk['distance']:.4f}")
        print(f"    chunk_id: {chunk['chunk_id']}")
        print(f"    metadata: source={chunk['source']!r}, "
              f"chunk_index={chunk['chunk_index']}")
        print(f"    text:     {preview}…\n")
