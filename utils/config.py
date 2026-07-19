"""
Enterprise AI Assistant
Configuration Loader
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

# ---------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------

# Local development:
#     Reads GROQ_API_KEY from .env
#
# Streamlit Cloud:
#     Reads GROQ_API_KEY from Streamlit Secrets

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    try:
        import streamlit as st

        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        GROQ_API_KEY = ""

# ---------------------------------------------------------------------
# Model Configuration
# ---------------------------------------------------------------------

LLM_MODEL = "llama-3.3-70b-versatile"

TEMPERATURE = 0.1

MAX_TOKENS = 2048

# ---------------------------------------------------------------------
# Embedding Configuration
# ---------------------------------------------------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------------------------------------------------
# Vector Store
# ---------------------------------------------------------------------

VECTOR_DB_PATH = str(BASE_DIR / "rag" / "faiss_index")

# ---------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------

DATABASE_PATH = str(BASE_DIR / "database" / "company.db")

DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

# ---------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------

PDF_DIRECTORY = str(BASE_DIR / "documents" / "generated")

SOURCE_DIRECTORY = str(BASE_DIR / "documents" / "source")

# ---------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------

TOP_K_DOCUMENTS = 4

# ---------------------------------------------------------------------
# Web Search
# ---------------------------------------------------------------------

WEB_SEARCH_API_KEY = os.getenv(
    "WEB_SEARCH_API_KEY",
    ""
)

if not WEB_SEARCH_API_KEY:
    try:
        import streamlit as st

        WEB_SEARCH_API_KEY = st.secrets.get(
            "WEB_SEARCH_API_KEY",
            ""
        )
    except Exception:
        WEB_SEARCH_API_KEY = ""

MAX_WEB_RESULTS = 5

# ---------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------

APP_NAME = "Enterprise AI Assistant"

VERSION = "1.0.0"

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def validate_environment() -> None:
    """
    Validate required configuration.
    """

    if not GROQ_API_KEY:
        raise RuntimeError(
            "Missing GROQ_API_KEY. "
            "Add it to the local .env file or Streamlit Cloud Secrets."
        )