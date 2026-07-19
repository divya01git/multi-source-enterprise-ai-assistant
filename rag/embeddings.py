"""
Enterprise AI Assistant
Embedding Model
"""

from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings

from utils.config import EMBEDDING_MODEL


class EmbeddingModel:
    """
    Singleton wrapper around HuggingFace embeddings.
    """

    _embeddings = None

    @classmethod
    def get_embeddings(cls) -> HuggingFaceEmbeddings:
        """
        Returns a cached embedding model instance.
        """

        if cls._embeddings is None:

            cls._embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={
                    "device": "cpu"
                },
                encode_kwargs={
                    "normalize_embeddings": True
                },
            )

        return cls._embeddings


embeddings = EmbeddingModel.get_embeddings()


if __name__ == "__main__":

    vector = embeddings.embed_query(
        "Enterprise AI Assistant"
    )

    print("=" * 60)
    print(f"Embedding length : {len(vector)}")
    print(vector[:10])