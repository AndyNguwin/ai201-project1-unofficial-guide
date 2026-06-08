"""Gradio UI for the NewJeans RAG pipeline.

Ties the pipeline together end-to-end:
    retrieve(query) -> generate_response(query, chunks) -> grounded answer

The answer already contains inline [n] citations and a numbered "Sources" list
(from generate.py). The "Retrieved from" panel additionally shows which
documents the supporting chunks were pulled from, with their similarity scores.
"""

import gradio as gr

from chunking import chunk_text, embed_and_store
from generate import generate_response
from ingestion import clean_document, load_document
from retrieval import retrieve


def rebuild_vector_db() -> None:
    """Re-chunk all documents and rebuild the ChromaDB collection from scratch.

    Runs the full ingestion -> chunking -> embedding pipeline so the UI always
    reflects the current CHUNK_SIZE / OVERLAP settings in chunking.py. Because
    embed_and_store() deletes and recreates the collection, this fully replaces
    any previously stored vectors.
    """
    print("Rebuilding vector database from documents...")
    documents = [clean_document(doc) for doc in load_document()]
    chunks = chunk_text(documents)
    collection = embed_and_store(chunks)
    print(f"Vector DB ready: {collection.count()} chunks "
          f"from {len(documents)} documents.\n")


def _display_name(source: str) -> str:
    """Drop the .txt extension for cleaner display."""
    return source[:-4] if source.endswith(".txt") else source


def ask(question: str) -> dict:
    """Run the full RAG pipeline for one question.

    Returns:
        {"answer": <grounded answer str>,
         "sources": [<"document (similarity X.XX)"> strings]}
    """
    chunks = retrieve(question)
    answer = generate_response(question, chunks)

    # Distinct source documents, keeping each one's best similarity, in the
    # order they were first retrieved.
    best_sim: dict[str, float] = {}
    for chunk in chunks:
        name = _display_name(chunk["source"])
        if name not in best_sim or chunk["similarity"] > best_sim[name]:
            best_sim[name] = chunk["similarity"]

    sources = [f"{name} (similarity {sim:.2f})" for name, sim in best_sim.items()]
    return {"answer": answer, "sources": sources}


def handle_query(question):
    question = (question or "").strip()
    if not question:
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="NewJeans — Unofficial Guide") as demo:
    gr.Markdown(
        "# NewJeans — The Unofficial Guide\n"
        "Ask a question about NewJeans. Answers are grounded in the source "
        "documents, with inline [n] citations and a numbered source list."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. Who are the members of NewJeans?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    # Rebuild the vector DB so the UI reflects the current chunking config.
    rebuild_vector_db()
    demo.launch()
