"""Retrieve node: fetches candidate documents for the current question."""

import logging
from typing import Any, Dict

from src.state import AgentState

logger = logging.getLogger(__name__)


def retrieve(state: AgentState) -> Dict[str, Any]:
    """Retrieve documents relevant to *state.question* from the vector store.

    This is a placeholder implementation. Replace the body with a real
    pgvector / langchain-postgres retriever when the vector store is ready.

    Args:
        state: Current agent state containing the question to retrieve for.

    Returns:
        A partial state dict with the retrieved ``documents`` list.
    """
    logger.info("retrieve | question=%r", state["question"])

    # TODO: Instantiate a PGVector retriever and call .invoke(state["question"])
    documents = []

    return {"documents": documents}
