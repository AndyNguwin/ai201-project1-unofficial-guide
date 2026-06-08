"""Stage 2 of the RAG pipeline: Chunking.

Splits each loaded-and-cleaned document into fixed-size, overlapping chunks so
they fit comfortably under the embedding model's context limit.

Strategy (from planning.md → Chunking Strategy):
    - Chunk size: 250 tokens
    - Overlap:    50 tokens
    - Token unit: the all-MiniLM-L6-v2 tokenizer, so "tokens" here means exactly
      what the embedding model will see. 250 content tokens + the model's 2
      special tokens ([CLS]/[SEP]) = 252, safely under the 256-token limit.

Each chunk is a dict with "text", "source", and "chunk_id" metadata, ready for
the embedding + vector-storage stage.
"""

import sys

from transformers import AutoTokenizer

from ingestion import clean_document, load_document

# Tokenizer for the embedding model. Counting in *its* tokens (not characters
# or whitespace words) is what guarantees chunks stay under the 256 limit.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 250  # tokens
OVERLAP = 50      # tokens

# Loaded once and reused across all documents.
_tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)


def chunk_text(
    documents: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
) -> list[dict]:
    """Split cleaned documents into fixed-size, overlapping token chunks.

    Args:
        documents:  List of {"source", "text"} dicts (from ingestion.py).
        chunk_size: Maximum tokens per chunk.
        overlap:    Tokens shared between consecutive chunks (carries context
                    across boundaries).

    Returns:
        A list of chunk dicts, each with:
            - "text":     the chunk's text, sliced verbatim from the source
            - "source":   the originating document's file name
            - "chunk_id": unique id, "<source>::<n>" (n = chunk index in source)
    """
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    step = chunk_size - overlap  # how far the window advances each iteration
    chunks: list[dict] = []

    for doc in documents:
        text = doc["text"]
        source = doc["source"]

        # add_special_tokens=False so [CLS]/[SEP] don't eat into the 250 budget.
        # return_offsets_mapping gives each token's (start, end) char span, which
        # lets us slice the ORIGINAL text instead of decoding (which would
        # lowercase and mangle the uncased WordPiece tokens).
        encoding = _tokenizer(
            text,
            add_special_tokens=False,
            return_offsets_mapping=True,
            truncation=False,
        )
        offsets = encoding["offset_mapping"]
        n_tokens = len(offsets)
        if n_tokens == 0:
            continue

        local_index = 0
        start = 0
        while start < n_tokens:
            end = min(start + chunk_size, n_tokens)

            # Char span covering tokens [start, end): start of first token to
            # end of last token in the window.
            char_start = offsets[start][0]
            char_end = offsets[end - 1][1]
            chunk_str = text[char_start:char_end].strip()

            if chunk_str:
                chunks.append(
                    {
                        "text": chunk_str,
                        "source": source,
                        "chunk_id": f"{source}::{local_index}",
                    }
                )
                local_index += 1

            if end == n_tokens:
                break  # reached the document's end
            start += step

    return chunks


def _count_tokens(text: str) -> int:
    """Token count under the embedding model's tokenizer (for verification)."""
    return len(_tokenizer(text, add_special_tokens=False)["input_ids"])


if __name__ == "__main__":
    # Render curly quotes / dashes instead of crashing on the Windows console.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    documents = [clean_document(doc) for doc in load_document()]
    chunks = chunk_text(documents)

    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    print(f"  chunk_size={CHUNK_SIZE} tokens, overlap={OVERLAP} tokens\n")

    # Per-chunk token counts confirm nothing exceeds the cap.
    token_counts = [_count_tokens(c["text"]) for c in chunks]
    print(f"  token counts -> min {min(token_counts)}, "
          f"max {max(token_counts)}, "
          f"avg {sum(token_counts) / len(token_counts):.0f}\n")

    # Show 5 full example chunks to verify text + metadata look right. Pick
    # them from different documents AND different positions (middle of each
    # chosen doc, not always chunk ::0) for a more representative sample.
    by_source: dict[str, list[dict]] = {}
    for chunk in chunks:
        by_source.setdefault(chunk["source"], []).append(chunk)

    # Spread the 5 picks evenly across the distinct sources.
    sources = list(by_source)
    n_picks = min(5, len(sources))
    step = max(1, len(sources) // n_picks)
    chosen_sources = sources[::step][:n_picks]

    # From each chosen document, take a middle chunk rather than the first.
    examples = [
        by_source[src][len(by_source[src]) // 2] for src in chosen_sources
    ]

    for example in examples:
        print(f"--- {example['chunk_id']}  ({_count_tokens(example['text'])} tokens) ---")
        print(f"source: {example['source']}")
        print(f"text:\n{example['text']}\n")
