"""StateGraph definition for the Self-Corrective RAG pipeline.

Graph topology
--------------

    [START]
       |
    retrieve
       |
    grade_documents
       |
    ┌──┴──────────────────────────┐
    │ (no relevant docs           │ (relevant docs
    │  AND retry_count < max)     │  OR retry_count >= max)
    │                             │
    rewrite_query              generate   <-- TODO: add generate node
       |                          |
    (back to retrieve)          [END]

The ``decide_next`` edge function inspects the state after grading and
routes to either ``rewrite_query`` (to loop) or ``generate`` (to finish).
"""

import logging
import os

from langgraph.graph import END, START, StateGraph

from src.nodes import grade_documents, retrieve, rewrite_query
from src.state import AgentState

logger = logging.getLogger(__name__)

MAX_RETRY_COUNT = int(os.getenv("MAX_RETRY_COUNT", "3"))

# ---------------------------------------------------------------------------
# Placeholder generate node
# ---------------------------------------------------------------------------


def generate(state: AgentState) -> dict:
    """Generate a final answer from the graded documents.

    This is a placeholder. Replace with a real LLM generation chain.
    """
    logger.info(
        "generate | question=%r docs=%d",
        state["question"],
        len(state["documents"]),
    )
    # TODO: call LLM with state["documents"] as context
    return {}


# ---------------------------------------------------------------------------
# Conditional edge
# ---------------------------------------------------------------------------


def decide_next(state: AgentState) -> str:
    """Determine the next node after document grading.

    ``grade_documents`` is responsible for filtering the document list so
    that it contains **only** passages graded as relevant.  An empty list
    therefore means no relevant documents were found for the current
    question, which is the signal to rewrite and retry retrieval.

    Returns:
        ``"rewrite_query"`` when no relevant documents remain after grading
        and the retry budget has not been exhausted, otherwise ``"generate"``.
    """
    relevant_docs = state.get("documents", [])
    retry_count = state.get("retry_count", 0)

    if not relevant_docs and retry_count < MAX_RETRY_COUNT:
        logger.info("decide_next -> rewrite_query (retry %d/%d)", retry_count, MAX_RETRY_COUNT)
        return "rewrite_query"

    logger.info("decide_next -> generate (docs=%d, retries=%d)", len(relevant_docs), retry_count)
    return "generate"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------


def build_graph() -> StateGraph:
    """Construct and compile the Self-Corrective RAG StateGraph."""
    builder = StateGraph(AgentState)

    builder.add_node("retrieve", retrieve)
    builder.add_node("grade_documents", grade_documents)
    builder.add_node("rewrite_query", rewrite_query)
    builder.add_node("generate", generate)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "grade_documents")
    builder.add_conditional_edges(
        "grade_documents",
        decide_next,
        {
            "rewrite_query": "rewrite_query",
            "generate": "generate",
        },
    )
    builder.add_edge("rewrite_query", "retrieve")
    builder.add_edge("generate", END)

    return builder.compile()


graph = build_graph()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = graph.invoke(
        {
            "question": "What is self-corrective RAG?",
            "documents": [],
            "retry_count": 0,
            "messages": [],
        }
    )
    print(result)
