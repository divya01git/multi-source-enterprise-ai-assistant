"""
Enterprise AI Assistant
FAISS Vector Store
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, List

from langchain_community.vectorstores import FAISS

from rag.embeddings import embeddings
from rag.loader import document_loader
from rag.splitter import document_splitter
from utils.config import VECTOR_DB_PATH


class VectorStore:

    def __init__(self) -> None:

        self.index_path = Path(
            VECTOR_DB_PATH
        )


    # ---------------------------------------------------------
    # Build Vector Store from default PDF directory
    # ---------------------------------------------------------

    def build(self) -> FAISS:

        documents = (
            document_loader.load_documents()
        )

        return self.build_from_documents(
            documents
        )


    # ---------------------------------------------------------
    # Build Vector Store from uploaded PDF
    # ---------------------------------------------------------

    def build_from_file(
        self,
        file_path: str | Path,
    ) -> FAISS:

        documents = (
            document_loader.load_file(
                file_path
            )
        )

        return self.build_from_documents(
            documents
        )


    # ---------------------------------------------------------
    # Common FAISS Builder
    # ---------------------------------------------------------

    def build_from_documents(
        self,
        documents: List,
    ) -> FAISS:


        if not documents:

            raise RuntimeError(
                "No documents found."
            )


        chunks = (
            document_splitter.split(
                documents
            )
        )


        vectorstore = FAISS.from_documents(
            chunks,
            embeddings,
        )


        self.save(
            vectorstore
        )


        return vectorstore


    # ---------------------------------------------------------
    # Save FAISS Index
    # ---------------------------------------------------------

    def save(
        self,
        vectorstore: FAISS,
    ) -> None:


        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        vectorstore.save_local(
            str(self.index_path)
        )


    # ---------------------------------------------------------
    # Load FAISS Index
    # ---------------------------------------------------------

    def load(self) -> Optional[FAISS]:


        if not self.index_path.exists():

            return None


        return FAISS.load_local(
            str(self.index_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )


    # ---------------------------------------------------------
    # Get Existing or Build New
    # ---------------------------------------------------------

    def get(self) -> FAISS:


        vectorstore = self.load()


        if vectorstore is None:

            vectorstore = self.build()


        return vectorstore



# Global instance
vector_store = VectorStore()



# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":


    db = vector_store.get()


    print("=" * 60)
    print("FAISS Index Ready")
    print()


    results = db.similarity_search(
        "company revenue",
        k=1,
    )


    print(results)