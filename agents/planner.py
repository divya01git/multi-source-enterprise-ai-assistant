"""
Enterprise AI Assistant
LLM Planner Agent
"""

from __future__ import annotations

import json
import re
from typing import Dict, List

from langchain_core.output_parsers import StrOutputParser

from llm import get_llm
from utils.prompts import PLANNER_PROMPT


VALID_TOOLS = {
    "SQL",
    "RAG",
    "WEB",
}


class PlannerAgent:
    """
    Determines which tools should answer the user question.

    Supported routes:

        SQL
        RAG
        WEB
        SQL + RAG
        SQL + WEB
        RAG + WEB
        SQL + RAG + WEB
    """

    def __init__(self) -> None:

        print("🔥 NEW PLANNER FILE LOADED 🔥")

        self.llm = get_llm()

        self.chain = (
            PLANNER_PROMPT
            | self.llm
            | StrOutputParser()
        )

    # ========================================================
    # JSON EXTRACTION
    # ========================================================

    def _extract_json(self, text: str):

        text = text.strip()

        text = re.sub(
            r"```json",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = text.replace("```", "").strip()

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL,
        )

        if not match:
            return None

        try:
            return json.loads(match.group())

        except json.JSONDecodeError:
            return None

    # ========================================================
    # MAIN PLANNER
    # ========================================================

    def plan(self, question: str) -> Dict:

        print("🔥 PLANNER RUNNING FOR:")
        print(question)

        question_lower = question.lower().strip()

        detected_tools: List[str] = []
        reasons: List[str] = []

        # ====================================================
        # CONTEXT DETECTION
        # ====================================================

        document_context = any(
            keyword in question_lower
            for keyword in [

                "annual report",
                "annual reports",
                "company report",
                "financial report",

                "company document",
                "company documents",
                "internal document",
                "internal documents",

                "uploaded document",
                "uploaded pdf",
                "uploaded docx",

                "according to the report",
                "according to the annual report",
                "according to the document",

                "what does the report say",
                "what does the annual report say",
                "what does the document say",

                "based on the report",
                "based on the annual report",
                "based on the document",

                "in the report",
                "in the annual report",
                "in the document",

                "reported in the annual report",

                "mentioned in the report",
                "mentioned in the annual report",

                "company policy",
                "leave policy",
                "employee handbook",
                "company guidelines",
                "company manual",

            ]
        )

        explicit_database_context = any(
            keyword in question_lower
            for keyword in [

                "in the company database",
                "in the database",
                "from the database",
                "company database",
                "database records",
                "database data",
                "database result",

            ]
        )

        # ====================================================
        # SQL DETECTION
        # ====================================================

        sql_keywords = [

            "employee",
            "employees",
            "staff",

            "leave balance",
            "leaves left",
            "leave left",
            "leaves remaining",
            "leave remaining",
            "how many leaves",

            "casual leave",
            "sick leave",
            "earned leave",

            "leave request",
            "leave requests",
            "pending leave",
            "approved leave",
            "rejected leave",

            "attendance",
            "present",
            "absent",
            "work from home",
            "half day",

            "salary",
            "salaries",
            "department",
            "designation",
            "joining date",

            "customer",
            "customers",

            "sales",
            "revenue",
            "profit",
            "expense",
            "expenses",

            "product",
            "products",
            "inventory",

            "order",
            "orders",

            "database",
            "databases",
            "records",
            "table",
            "tables",

            "how many",
            "total",
            "average",
            "highest",
            "lowest",

        ]

        sql_detected = any(
            keyword in question_lower
            for keyword in sql_keywords
        )

        # ====================================================
        # RAG DETECTION
        # ====================================================

        rag_keywords = [

            "annual report",
            "annual reports",

            "company report",
            "financial report",

            "company document",
            "company documents",

            "internal document",
            "internal documents",

            "uploaded document",
            "uploaded pdf",
            "uploaded docx",

            "company policy",
            "leave policy",
            "leave rules",
            "leave procedure",
            "leave process",

            "how to apply for leave",
            "how can i apply for leave",

            "employee handbook",
            "company guidelines",
            "company manual",

            "company strategy",
            "internal documentation",
            "meeting minutes",

            "according to the report",
            "according to the annual report",
            "according to the document",

            "reported in the annual report",

            "what caused",
            "reason for the decline",
            "reason for revenue decline",

            "why did revenue decline",
            "why revenue declined",

            "what does the report say",
            "what does the annual report say",
            "what does the document say",

            "based on the report",
            "based on the annual report",
            "based on the document",

            "in the report",
            "in the annual report",
            "in the document",

        ]

        rag_detected = any(
            keyword in question_lower
            for keyword in rag_keywords
        )

        # ====================================================
        # WEB DETECTION
        # ====================================================

        web_keywords = [

            "latest",
            "today",
            "recent",
            "news",
            "trends",
            "trend",

            "this week",
            "this month",
            "right now",

            "online",
            "internet",
            "web",

            "what is langgraph",
            "what is langchain",

            "latest langgraph",
            "latest langchain",

            "langgraph update",
            "langchain update",

            "latest ai",
            "ai news",
            "ai trends",

            "latest ai industry trends",
            "latest ai trends",

            "technology trends",
            "tech news",

            "regulations",

            "stock price",
            "stock prices",

            "market news",
            "market trends",

        ]

        web_detected = any(
            keyword in question_lower
            for keyword in web_keywords
        )

        # ====================================================
        # ROUTING PRIORITY
        # ====================================================

        # ----------------------------------------------------
        # 1. Explicit database questions
        # ----------------------------------------------------

        if explicit_database_context:

            detected_tools.append("SQL")

            reasons.append(
                "Question explicitly requests structured "
                "enterprise database information."
            )

        # ----------------------------------------------------
        # 2. SQL questions
        # ----------------------------------------------------

        elif sql_detected and not document_context:

            detected_tools.append("SQL")

            reasons.append(
                "Question requires structured enterprise "
                "database information."
            )

        # ----------------------------------------------------
        # 3. RAG questions
        # ----------------------------------------------------

        if rag_detected:

            detected_tools.append("RAG")

            reasons.append(
                "Question requires information from internal "
                "enterprise documents."
            )

        # ----------------------------------------------------
        # 4. WEB questions
        # ----------------------------------------------------

        # Important:
        #
        # A database question containing words such as
        # "current" or "currently" must NOT be sent to WEB.
        #
        # Examples:
        #
        # Current employee leave balance → SQL
        # Current customer count → SQL
        # Current pending leave requests → SQL
        #
        # Current AI trends → WEB
        # Latest LangGraph updates → WEB

        if web_detected and not (
            sql_detected
            or explicit_database_context
        ):

            detected_tools.append("WEB")

            reasons.append(
                "Question requires current external "
                "web information."
            )

        # ====================================================
        # REMOVE DUPLICATES
        # ====================================================

        detected_tools = list(
            dict.fromkeys(detected_tools)
        )

        print("🔥 DETECTED TOOLS:")
        print(detected_tools)

        # ====================================================
        # DETERMINISTIC ROUTING
        # ====================================================

        if detected_tools:

            result = {
                "tools": detected_tools,
                "reason": " ".join(reasons),
            }

            print("🔥 FINAL PLAN:")
            print(result)

            return result

        # ====================================================
        # LLM FALLBACK
        # ====================================================

        try:

            response = self.chain.invoke(
                {
                    "question": question,
                }
            )

            plan = self._extract_json(response)

            if plan:

                tools = [
                    tool.upper()
                    for tool in plan.get("tools", [])
                    if isinstance(tool, str)
                    and tool.upper() in VALID_TOOLS
                ]

                tools = list(
                    dict.fromkeys(tools)
                )

                if tools:

                    result = {
                        "tools": tools,
                        "reason": plan.get(
                            "reason",
                            "Question routed using "
                            "the LLM planner.",
                        ),
                    }

                    print("🔥 LLM PLAN:")
                    print(result)

                    return result

        except Exception as exc:

            print("❌ PLANNER ERROR:")
            print(exc)

        # ====================================================
        # DEFAULT ROUTE
        # ====================================================

        return {
            "tools": ["RAG"],
            "reason": (
                "Question is best answered using internal "
                "enterprise documents."
            ),
        }


planner = PlannerAgent()


if __name__ == "__main__":

    questions = [

        "How many employees are there?",

        "What is the current employee leave balance?",

        "What is the current status of employee leave requests?",

        "How many customers are currently registered?",

        "What are the current AI trends?",

        "What is the latest development in LangGraph?",

        "What is the company leave policy?",

        "How do I apply for leave?",

    ]

    for question in questions:

        print("=" * 70)
        print("QUESTION:")
        print(question)

        result = planner.plan(question)

        print("RESULT:")
        print(result)