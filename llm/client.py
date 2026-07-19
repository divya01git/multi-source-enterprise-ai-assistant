"""
Enterprise AI Assistant
Shared Groq LLM Client
"""

from __future__ import annotations

from functools import lru_cache

from langchain_groq import ChatGroq

from utils.config import (
    GROQ_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    validate_environment,
)


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    """
    Returns a singleton ChatGroq client.

    Using @lru_cache ensures only one client is created
    during the Streamlit application's lifetime.
    """

    validate_environment()

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )