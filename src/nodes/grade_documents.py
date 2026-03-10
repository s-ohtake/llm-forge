"""Grade documents node: scores retrieved documents for relevance."""

import logging
from typing import Any, Dict

from src.state import AgentState

logger = logging.getLogger(__name__)

# Sentinel value written to state so that the conditional edge can inspect it.
GRADE_RELEVANT = "relevant"
GRADE_NOT_RELEVANT = "not_relevant"


def grade_documents(state: AgentState) -> Dict[str, Any]:
    """Assess whether the retrieved documents are relevant to *state.question*.

    This is a placeholder implementation. Replace the grading logic with an
    LLM-based relevance check (e.g. a LiteLLM / LangChain grader chain).

    Args:
        state: Current agent state with ``question`` and ``documents``.

    Returns:
        A partial state dict.  The ``documents`` list is filtered to only
        keep passages graded as relevant.  When no documents pass the filter
        the list is left empty so the conditional edge can route to
        ``rewrite_query``.
    """
    logger.info(
        "grade_documents | question=%r docs=%d",
        state["question"],
        len(state["documents"]),
    )

    # TODO: Run each document through an LLM grader and filter out irrelevant ones.
    relevant_docs = state["documents"]

    return {"documents": relevant_docs}
