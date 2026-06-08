"""Stage 5 of the RAG pipeline: Generation.

Takes a user query plus the chunks retrieved for it and asks Groq's
llama-3.3-70b-versatile to write an answer that is *grounded* in those chunks —
i.e. it must rely only on the supplied context and cite the sources it used.

The prompts are module-level templates (SYSTEM_PROMPT / USER_PROMPT_TEMPLATE)
so the grounding instructions are easy to tweak without touching the logic.
"""

import os
import re
import sys

from dotenv import load_dotenv
from groq import Groq

# Load GROQ_API_KEY (and anything else) from the .env file next to this script.
load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"  # per the Architecture Diagram

# --- Prompt templates (edit these to change grounding behavior) -------------

# System prompt: the grounding rules the model must follow.
SYSTEM_PROMPT = """\
You are a knowledgeable assistant answering questions about the K-pop group \
NewJeans. You must answer using ONLY the information in the provided context \
passages. Follow these rules strictly:

1. Base your answer solely on the context below. Do not use outside knowledge \
or make assumptions beyond what the passages state.
2. If the context does not contain enough information to answer the question, \
say so plainly (e.g. "I don't have enough information in the provided sources \
to answer that.") rather than guessing.
3. Cite your sources inline using the bracketed numbers shown in the context, \
e.g. "NewJeans debuted in 2022 [1]." Place the [n] marker right after the \
statement it supports. You may cite more than one, e.g. [1][3]. Use only the \
numbers that appear in the context; never invent a number.
4. Do NOT write your own "Sources" or reference list at the end — only use the \
inline [n] markers. The source list is added automatically.
5. Be concise and factual. Do not repeat the question or pad the answer.\
"""

# User prompt: how the retrieved context and the question are presented.
USER_PROMPT_TEMPLATE = """\
Context passages:
{context}

Question: {question}

Answer (grounded in the context above, with source citations):\
"""


# Lazily initialized, then reused across generate_response() calls.
_client: Groq | None = None


def _get_client() -> Groq:
    """Create the Groq client once, reading the API key from the environment."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your .env file "
                "(see .env.example)."
            )
        _client = Groq(api_key=api_key)
    return _client


def _display_name(source: str) -> str:
    """Drop the .txt extension for cleaner citations."""
    return source[:-4] if source.endswith(".txt") else source


def _build_source_map(chunks: list[dict]) -> dict[str, int]:
    """Assign each DISTINCT source document a citation number, in first-seen
    order, so inline [n] markers map to documents rather than to chunks."""
    source_to_num: dict[str, int] = {}
    for chunk in chunks:
        if chunk["source"] not in source_to_num:
            source_to_num[chunk["source"]] = len(source_to_num) + 1
    return source_to_num


def _format_context(chunks: list[dict], source_to_num: dict[str, int]) -> str:
    """Render retrieved chunks into a numbered, source-labeled context block.

    Chunks from the same document share the same [n], reinforcing that the
    number refers to the document.
    """
    blocks = []
    for chunk in chunks:
        n = source_to_num[chunk["source"]]
        header = (f"[{n}] Source: {_display_name(chunk['source'])} "
                  f"(chunk {chunk['chunk_index']})")
        blocks.append(f"{header}\n{chunk['text']}")
    return "\n\n".join(blocks)


def _append_source_list(answer: str, source_to_num: dict[str, int]) -> str:
    """Append a 'Sources:' list mapping the [n] markers the model actually
    cited back to their document names."""
    num_to_source = {n: src for src, n in source_to_num.items()}

    # Collect every number cited inline, handling [1], [1][3], and [1, 3].
    cited: set[int] = set()
    for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", answer):
        for part in group.split(","):
            cited.add(int(part.strip()))

    cited_in_order = sorted(n for n in cited if n in num_to_source)
    if not cited_in_order:
        return answer  # model cited nothing (e.g. "not enough information")

    lines = [answer.rstrip(), "", "Sources:"]
    for n in cited_in_order:
        lines.append(f"[{n}] {_display_name(num_to_source[n])}")
    return "\n".join(lines)


def generate_response(
    query: str,
    retrieved_chunks: list[dict],
    model: str = GROQ_MODEL,
    temperature: float = 0.2,
) -> str:
    """Generate a grounded answer to a query from the retrieved chunks.

    Args:
        query:            The user's question.
        retrieved_chunks: Chunk dicts from retrieve() — each needs "text",
                          "source", and "chunk_index".
        model:            Groq model id (default llama-3.3-70b-versatile).
        temperature:      Low by default to keep answers grounded/deterministic.

    Returns:
        The model's answer as a string.
    """
    if not query.strip():
        raise ValueError("Query is empty.")

    # No context to ground on — don't even call the model.
    if not retrieved_chunks:
        return ("I don't have enough information in the provided sources "
                "to answer that.")

    # Number distinct documents, then build the context using those numbers.
    source_to_num = _build_source_map(retrieved_chunks)
    context = _format_context(retrieved_chunks, source_to_num)
    user_prompt = USER_PROMPT_TEMPLATE.format(context=context, question=query)

    client = _get_client()
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    answer = completion.choices[0].message.content.strip()
    # Append the numbered Sources list matching the inline [n] citations.
    return _append_source_list(answer, source_to_num)


if __name__ == "__main__":
    # Render curly quotes / dashes instead of crashing on the Windows console.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Full pipeline demo: retrieve, then generate a grounded answer.
    from retrieval import retrieve

    query = input("Enter your query: ").strip()
    chunks = retrieve(query)

    print(f"\nRetrieved {len(chunks)} chunk(s). Sources used:")
    for chunk in chunks:
        print(f"  - {chunk['source']} (chunk {chunk['chunk_index']}, "
              f"similarity={chunk['similarity']:.3f})")

    answer = generate_response(query, chunks)
    print("\n--- Grounded answer ---")
    print(answer)
