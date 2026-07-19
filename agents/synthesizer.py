"""
Enterprise AI Assistant
Response Synthesizer
"""

from __future__ import annotations

from llm.client import get_llm


class Synthesizer:
    """
    Combines responses from different agents
    and creates the final answer with sources.
    """


    def __init__(self):

        self.llm = get_llm()



    # ---------------------------------------------------------
    # Combine Responses
    # ---------------------------------------------------------

    def synthesize(
        self,
        query: str,
        context,
        sources
    ) -> str:

        """
        Generate final response using available sources.
        """


        prompt = f"""
You are the final response generator for an Enterprise AI Assistant.

Create the best possible answer for the user.

Rules:
- Answer only using the provided information.
- Keep the answer clear and professional.
- Do not hallucinate.
- Add a Sources section at the end.
- Mention the source type clearly.

User Question:

{query}


Available Information:

{context}


Sources:

{sources}


Final Answer Format:

# Answer

<response>

## Sources

- <source names>

"""


        response = self.llm.invoke(
            prompt
        )


        return response.content



synthesizer = Synthesizer()