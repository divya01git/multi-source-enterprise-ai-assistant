"""
Enterprise AI Assistant
RAG Question Answering Chain
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from rag.retriever import DocumentRetriever
from llm.client import get_llm


class QAChain:

    def __init__(self):

        self.retriever = DocumentRetriever().get_retriever()

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an enterprise AI assistant.

            Answer the question using only the given context.

            Context:
            {context}

            Question:
            {question}

            Answer:
            """
        )

        self.chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
        )


    def ask(self, question: str):

        response = self.chain.invoke(question)

        return response.content


if __name__ == "__main__":

    qa = QAChain()

    answer = qa.ask(
        "Why did revenue decline?"
    )

    print("\nAnswer:")
    print(answer)