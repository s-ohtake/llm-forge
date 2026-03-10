"""Agent state definition for the Self-Corrective RAG pipeline."""

from typing import Annotated, List, Sequence

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import NotRequired, TypedDict


class AgentState(TypedDict):
    """State shared across all nodes in the RAG agent graph.

    Attributes:
        messages: Conversation messages managed by LangGraph's ``add_messages``
            reducer.
        question: The current user question (may be rewritten).
        documents: Retrieved documents graded as relevant; empty means no
            relevant documents were found for the current question.
            Defaults to an empty list when not supplied by the caller.
        retry_count: Number of query-rewrite iterations performed so far.
            Defaults to ``0`` when not supplied by the caller.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    question: str
    documents: NotRequired[List[Document]]
    retry_count: NotRequired[int]
