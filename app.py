"""Gradio UI for the NewJeans RAG pipeline.

Ties the pipeline together end-to-end:
    retrieve(query) -> generate_response(query, chunks) -> grounded answer

The answer already contains inline [n] citations and a numbered "Sources" list
(from generate.py). The "Retrieved from" panel additionally shows which
documents the supporting chunks were pulled from, with their similarity scores.
"""

import gradio as gr

from generate import generate_response
from retrieval import retrieve


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
    demo.launch()
