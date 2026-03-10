"""Rewrite query node: rephrases the question to improve retrieval."""

import logging
from typing import Any, Dict

from src.state import AgentState

logger = logging.getLogger(__name__)


def rewrite_query(state: AgentState) -> Dict[str, Any]:
    """Rewrite *state.question* to improve downstream retrieval quality.

    This is a placeholder implementation. Replace the body with a real
    LLM-based rewriting chain (e.g. using LiteLLM / LangChain).

    Args:
        state: Current agent state containing the question to rewrite and
               the current ``retry_count``.

    Returns:
        A partial state dict with the updated ``question`` and incremented
        ``retry_count``.
    """
    current_count = state.get("retry_count", 0)
    logger.info(
        "rewrite_query | attempt=%d question=%r",
        current_count + 1,
        state["question"],
    )

    # TODO: Call an LLM chain to produce a better-phrased question.
    rewritten_question = state["question"]

    return {
        "question": rewritten_question,
        "retry_count": current_count + 1,
    }
