"""Stage 1 of the RAG pipeline: Document Ingestion.

Loads every source document (.txt) in the documents/ folder and extracts its
raw text along with metadata identifying where it came from. Each document is
returned as a dictionary with "source" and "text" fields, ready to be handed
off to the chunking stage.
"""

import html
import re
import sys
from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent / "documents"

# Inline noise removed anywhere it appears in a line (not whole-line matches).
# - Numeric reference markers:        "...models[76]" -> "...models"
# - Common bracketed editorial tags:  "[citation needed]", "[ko]", "[edit]"
_INLINE_NOISE = re.compile(
    r"\[\d+\]"  # [76], [181]
    r"|\[(?:citation needed|clarification needed|edit|note \d+|when\?"
    r"|update|ko|a|b|c|d)\]",  # editorial / language / footnote tags
    flags=re.IGNORECASE,
)

# Whole lines that are pure page furniture get dropped. These match a line only
# when the *entire* line (trimmed, lowercased) is the boilerplate — so prose that
# merely mentions a word (e.g. "the advertising industry") is left untouched.
_BOILERPLATE_EXACT = {
    "advertisement", "advertisements", "sponsored", "sponsored content",
    "share", "tweet", "pin it", "share this", "share this article",
    "copy link", "print", "save", "home", "menu", "search",
    "sign in", "log in", "login", "subscribe", "newsletter",
    "related articles", "related stories", "you may also like",
    "recommended for you", "more from this author", "trending",
    "leave a comment", "post a comment", "view all comments",
    "accept all cookies", "accept cookies", "manage cookies",
    "read more", "continue reading", "load more", "show more",
    "next", "previous", "back to top",
}

# Whole-line patterns (anchored) for boilerplate with variable text.
_BOILERPLATE_PATTERNS = [
    re.compile(r"^share on [\w ]+$", re.IGNORECASE),       # "Share on Facebook"
    re.compile(r"^\d[\d,]*\s+comments?$", re.IGNORECASE),  # "42 Comments"
    re.compile(r"^\d[\d,]*\s+shares?$", re.IGNORECASE),    # "1,203 Shares"
    re.compile(r"^read more[:.…]*.*$", re.IGNORECASE),  # "Read more: ..."
    re.compile(r"^we use cookies\b.*$", re.IGNORECASE),    # cookie banner
    re.compile(r"^(main article|see also|further information"
               r"|further reading)\s*:.*$", re.IGNORECASE),  # wiki cross-refs
    re.compile(r"^©.*$"),                                  # "© 2024 Billboard"
    re.compile(r"^all rights reserved\.?$", re.IGNORECASE),
]


def load_document(documents_dir: Path = DOCUMENTS_DIR) -> list[dict]:
    """Load the raw text and metadata of every .txt document.

    Args:
        documents_dir: Folder containing the source .txt files.

    Returns:
        A list of dictionaries, one per document, each with:
            - "source": the document's file name (its metadata / attribution)
            - "text":   the raw, unmodified text extracted from the file
    """
    documents_dir = Path(documents_dir)
    if not documents_dir.is_dir():
        raise FileNotFoundError(f"Documents folder not found: {documents_dir}")

    documents: list[dict] = []

    # Sorted so the ingestion order is stable and reproducible across runs.
    for path in sorted(documents_dir.glob("*.txt")):
        # utf-8-sig drops any byte-order mark that web copy-paste can leave behind.
        text = path.read_text(encoding="utf-8-sig")

        # Skip empty / whitespace-only files so they don't pollute later stages.
        if not text.strip():
            print(f"  [skip] {path.name} is empty")
            continue

        documents.append({"source": path.name, "text": text})

    return documents


def _is_boilerplate_line(line: str) -> bool:
    """True if a line is pure page furniture (nav, share button, ad, etc.)."""
    stripped = line.strip()
    if stripped.lower() in _BOILERPLATE_EXACT:
        return True
    return any(pattern.match(stripped) for pattern in _BOILERPLATE_PATTERNS)


def clean_document(document: dict) -> dict:
    """Clean the raw text of a single loaded document.

    Removes web boilerplate while preserving substantive content:
      - strips HTML tags and decodes HTML entities (&amp;, &#39;, &nbsp;)
      - removes inline reference markers and editorial tags ([76], [edit], [ko])
      - drops whole lines that are navigation, share/print buttons, ads,
        cookie banners, "read more" links, comment/share counts, and footers
      - normalizes whitespace (collapses runs of blank lines and spaces)

    A line is only dropped when the *entire* line is boilerplate, so prose that
    happens to contain a word like "advertising" or "share" is kept intact.

    Args:
        document: A dict with "source" and "text" (as returned by load_document).

    Returns:
        A new dict with the same "source" and a cleaned "text".
    """
    text = document["text"]

    # 1. Strip HTML tags, then decode entities (order matters so "&lt;b&gt;"
    #    style escaped markup doesn't reappear as live tags after unescaping).
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)

    # 2. Remove inline reference markers / editorial tags.
    text = _INLINE_NOISE.sub("", text)

    # 3. Drop whole-line boilerplate; collapse leftover intra-line whitespace.
    kept_lines: list[str] = []
    for line in text.splitlines():
        if _is_boilerplate_line(line):
            continue
        kept_lines.append(re.sub(r"[ \t]+", " ", line).rstrip())
    text = "\n".join(kept_lines)

    # 4. Collapse 3+ consecutive newlines into a paragraph break, then trim.
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    return {"source": document["source"], "text": text}


if __name__ == "__main__":
    # Render the curly quotes / dashes in these sources instead of crashing on
    # the default Windows console (cp1252) encoding.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    raw_docs = load_document()
    clean_docs = [clean_document(doc) for doc in raw_docs]

    print(f"Loaded and cleaned {len(clean_docs)} document(s)\n")
    print(f"  {'raw':>7}  {'clean':>7}  {'removed':>8}  source")
    # for raw, clean in zip(raw_docs, clean_docs):
    #     removed = len(raw["text"]) - len(clean["text"])
    #     print(
    #         f"  {len(raw['text']):>7,}  {len(clean['text']):>7,}  "
    #         f"{removed:>8,}  {clean['source']}"
    #     )

    # Preview a Wikipedia doc (richest in citation markers / cross-refs) so the
    # raw-vs-clean difference is visible: boilerplate gone, prose intact.
    sample_name = "Wikipedia - NewJeans.txt"
    raw_sample = next((d for d in raw_docs if sample_name in d["source"]), raw_docs[0])
    clean_sample = next((d for d in clean_docs if sample_name in d["source"]), clean_docs[0])

    print(f"\n--- RAW extraction: {raw_sample['source']} (first 600 chars) ---")
    print(raw_sample["text"][:600])

    print(f"\n--- CLEANED: {clean_sample['source']} (first 600 chars) ---")
    print(clean_sample["text"][:600])
