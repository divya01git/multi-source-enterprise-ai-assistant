"""
Enterprise AI Assistant
Document Splitter
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentSplitter:
    """
    Splits documents into chunks for vector embeddings.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(
        self,
        documents: List[Document],
    ) -> List[Document]:
        """
        Split loaded documents into smaller chunks.
        """

        if not documents:
            return []

        chunks = self.splitter.split_documents(documents)

        return chunks


document_splitter = DocumentSplitter()


if __name__ == "__main__":

    from rag.loader import document_loader

    docs = document_loader.load_documents()

    chunks = document_splitter.split(docs)

    print("=" * 60)
    print(f"Documents : {len(docs)}")
    print(f"Chunks    : {len(chunks)}")

    if chunks:
        print()
        print(chunks[0].metadata)
        print(chunks[0].page_content[:400])