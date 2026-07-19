"""
Enterprise AI Assistant
RAG Agent
"""

from __future__ import annotations

from rag.retriever import DocumentRetriever
from llm.client import get_llm


class RAGAgent:
    """
    Handles Retrieval Augmented Generation (RAG).

    Workflow:
    User Question
        ↓
    FAISS Retriever
        ↓
    Relevant Document Chunks
        ↓
    LLM
        ↓
    Final Answer
    """

    def __init__(self):

        self.llm = get_llm()
        self.retriever = DocumentRetriever()

    # ---------------------------------
    # Retrieve Context
    # ---------------------------------

    def get_context(
        self,
        query: str,
    ) -> str:

        documents = self.retriever.search(query)

        if not documents:
            return ""

        context_parts = []

        for doc in documents:

            context_parts.append(doc.page_content)

        return "\n\n".join(context_parts)

    # ---------------------------------
    # Generate Answer
    # ---------------------------------

    def generate_answer(
        self,
        query: str,
        context: str,
    ) -> str:

        prompt = f"""
You are an Enterprise AI Assistant.

Answer ONLY using the provided document context.

Rules:
- Do not use outside knowledge.
- If the answer is unavailable in the context, reply:
"I don't have enough information from the documents."

Document Context:

{context}

User Question:

{query}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content

    # ---------------------------------
    # Complete Pipeline
    # ---------------------------------

    def run(
        self,
        query: str,
    ) -> str:

        context = self.get_context(query)

        if not context:

            return (
                "No relevant information found "
                "in the knowledge base."
            )

        return self.generate_answer(
            query,
            context,
        )


rag_agent = RAGAgent()


if __name__ == "__main__":

    answer = rag_agent.run(
        "What is the company revenue?"
    )

    print("=" * 60)
    print(answer)