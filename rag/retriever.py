"""
Enterprise AI Assistant
Document Retriever
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document

from rag.vector_store import vector_store


class DocumentRetriever:
    """
    Retrieves relevant document chunks from the FAISS
    vector store.

    Responsibilities:
    - Perform similarity search
    - Retrieve multiple relevant document chunks
    - Use consistent retrieval settings
    - Support semantic document question answering
    """

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    RETRIEVAL_K = 5

    # -------------------------------------------------
    # Initialization
    # -------------------------------------------------

    def __init__(self):

        self.db = vector_store.get()

    # -------------------------------------------------
    # Retriever
    # -------------------------------------------------

    def get_retriever(self):

        return self.db.as_retriever(
            search_kwargs={
                "k": self.RETRIEVAL_K,
            }
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        query: str,
    ) -> List[Document]:
        """
        Performs similarity search against the FAISS
        vector store.

        Retrieves the top relevant document chunks.
        """

        if not query or not query.strip():

            return []

        return self.db.similarity_search(
            query,
            k=self.RETRIEVAL_K,
        )