"""
Enterprise AI Assistant
Web Agent
"""

from __future__ import annotations

from typing import Any, Dict, List

from tools.web_tool import web_tool
from llm.client import get_llm


class WebAgent:
    """
    Handles web-based question answering.

    Returns both:
    - Generated answer
    - Original web search results
      including title and URL
    """

    def __init__(self):

        self.web_tool = web_tool

        self.llm = get_llm()

    # ---------------------------------------------------------
    # Search Web
    # ---------------------------------------------------------

    def search_web(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:

        """
        Retrieve web results.
        """

        return self.web_tool.search(
            query,
        )

    # ---------------------------------------------------------
    # Generate Answer
    # ---------------------------------------------------------

    def generate_answer(
        self,
        query: str,
        results: List[Dict[str, Any]],
    ) -> str:

        """
        Generate answer from web results.
        """

        if not results:

            return (
                "I could not find any web information."
            )

        context = "\n\n".join(

            [

                f"""
Title:
{item.get("title", "")}

Content:
{item.get("content", "")}

URL:
{item.get("url", "")}
"""

                for item in results

            ]

        )

        prompt = f"""
You are an Enterprise AI Assistant.

Answer the user's question using the web information below.

Rules:
- Use only the provided web information.
- Do not hallucinate.
- Keep the answer clear and concise.
- If the information is insufficient, say so clearly.

Web Information:

{context}

Question:

{query}

Provide a clear and concise answer.
"""

        response = self.llm.invoke(
            prompt,
        )

        return response.content

    # ---------------------------------------------------------
    # Main Pipeline
    # ---------------------------------------------------------

    def run(
        self,
        query: str,
    ) -> Dict[str, Any]:

        """
        Run web search and generate an answer.

        Returns:

        {
            "answer": "...",
            "results": [
                {
                    "title": "...",
                    "content": "...",
                    "url": "..."
                }
            ]
        }
        """

        results = self.search_web(
            query,
        )

        answer = self.generate_answer(
            query,
            results,
        )

        return {

            "answer": answer,

            "results": results,

        }


web_agent = WebAgent()