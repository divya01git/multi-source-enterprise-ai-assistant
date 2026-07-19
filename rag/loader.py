"""
Enterprise AI Assistant
RAG Document Loader
Supports PDF and DOCX documents
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
)

from utils.config import PDF_DIRECTORY


class DocumentLoader:
    """
    Loads enterprise documents for RAG pipeline.

    Supported formats:
    - PDF
    - DOCX
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
    }

    def __init__(self) -> None:

        self.document_directory = Path(PDF_DIRECTORY)

        self.document_directory.mkdir(
            parents=True,
            exist_ok=True
        )


    # ---------------------------------------------------------
    # Load all documents from directory
    # ---------------------------------------------------------

    def load_documents(self) -> List[Document]:

        documents: List[Document] = []

        if not self.document_directory.exists():
            return documents


        files = sorted(
            [
                file
                for file in self.document_directory.iterdir()
                if file.suffix.lower()
                in self.SUPPORTED_EXTENSIONS
            ]
        )


        for file in files:

            documents.extend(
                self.load_file(file)
            )


        return documents


    # ---------------------------------------------------------
    # Load single document
    # PDF + DOCX support
    # ---------------------------------------------------------

    def load_file(
        self,
        file_path: str | Path,
    ) -> List[Document]:

        documents: List[Document] = []

        file_path = Path(file_path)


        if not file_path.exists():

            print(
                f"File not found: {file_path}"
            )

            return documents


        try:

            extension = file_path.suffix.lower()


            # -------------------------
            # PDF Loader
            # -------------------------

            if extension == ".pdf":

                loader = PyPDFLoader(
                    str(file_path)
                )


            # -------------------------
            # DOCX Loader
            # -------------------------

            elif extension == ".docx":

                loader = Docx2txtLoader(
                    str(file_path)
                )


            else:

                print(
                    f"Unsupported file type: {extension}"
                )

                return documents



            loaded_docs = loader.load()



            for doc in loaded_docs:

                doc.metadata.update(
                    {
                        "source": file_path.name,
                        "file_type": extension.replace(
                            ".",
                            ""
                        ),
                    }
                )


            documents.extend(
                loaded_docs
            )


        except Exception as e:

            print(
                f"Failed to load {file_path.name}: {e}"
            )


        return documents



    # ---------------------------------------------------------
    # Count documents
    # ---------------------------------------------------------

    def document_count(self) -> int:

        if not self.document_directory.exists():

            return 0


        return len(
            [
                file
                for file in self.document_directory.iterdir()
                if file.suffix.lower()
                in self.SUPPORTED_EXTENSIONS
            ]
        )



document_loader = DocumentLoader()



# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    docs = document_loader.load_documents()


    print("=" * 60)

    print(
        f"Loaded {len(docs)} document sections"
    )


    if docs:

        print()

        print(
            "First document metadata:"
        )

        print(
            docs[0].metadata
        )


        print()

        print(
            "Content preview:"
        )

        print(
            docs[0].page_content[:500]
        )