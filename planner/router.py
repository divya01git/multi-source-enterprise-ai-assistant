"""
Enterprise AI Assistant
Query Router / Planner
"""

from __future__ import annotations

from llm.client import get_llm


class QueryRouter:

    def __init__(self):

        self.llm = get_llm()

    def route(
        self,
        query: str
    ) -> str:

        query_lower = query.lower().strip()

        # -------------------------------------------------
        # Deterministic RAG Routing
        # -------------------------------------------------
        # Document-specific wording must take priority over
        # generic SQL keywords such as revenue, employees, etc.
        #
        # Example:
        #
        # "According to the annual report, why did revenue
        # decline in March?"
        #
        # Contains "revenue", but explicitly asks about a
        # company document. Therefore it must go to RAG.

        rag_context_keywords = [

            "according to the annual report",
            "according to the report",
            "according to the document",
            "according to the pdf",
            "according to the policy",
            "according to company policy",
            "according to the handbook",
            "according to the manual",

            "annual report",
            "company report",
            "financial report",
            "internal report",

            "company document",
            "company documents",
            "internal document",
            "internal documents",

            "pdf",
            "document",
            "documents",

            "policy",
            "policies",

            "guideline",
            "guidelines",

            "manual",
            "handbook",

            "what does the report say",
            "what does the document say",
            "what does the annual report say",

            "based on the report",
            "based on the document",
            "based on the annual report",

            "in the report",
            "in the document",
            "in the annual report",

            "mentioned in the report",
            "mentioned in the document",
            "mentioned in the annual report",
        ]

        if any(
            keyword in query_lower
            for keyword in rag_context_keywords
        ):

            return "RAG"

        # -------------------------------------------------
        # Deterministic Web Routing
        # -------------------------------------------------

        web_keywords = [

            "latest",
            "current",
            "today",
            "recent",
            "news",
            "trends",
            "trend",
            "2026",
        ]

        if any(
            keyword in query_lower
            for keyword in web_keywords
        ):

            return "WEB"

        # -------------------------------------------------
        # Deterministic SQL Routing
        # -------------------------------------------------

        sql_keywords = [

            "employee",
            "employees",

            "leave",
            "leaves",
            "leave balance",
            "leave request",
            "leave requests",

            "attendance",
            "present",
            "absent",

            "salary",
            "salaries",
            "department",

            "customer",
            "customers",

            "product",
            "products",

            "order",
            "orders",

            "sales",
            "revenue",
            "profit",
            "expense",
            "expenses",

            "database",
            "records",

            "how many",
            "total",
            "average",
            "count",
        ]

        if any(
            keyword in query_lower
            for keyword in sql_keywords
        ):

            return "SQL"

        # -------------------------------------------------
        # LLM Routing
        # -------------------------------------------------

        prompt = f"""
You are an AI query router.

Classify the user's query into exactly one category.

RAG:
Questions answered from company documents, annual reports,
policies, manuals, rules, guidelines, or internal documentation.

IMPORTANT:
If the user explicitly refers to a document, report, PDF,
annual report, policy, manual, or internal documentation,
choose RAG even if the question also contains words such as
revenue, employees, sales, profit, salary, or customers.

SQL:
Questions requiring structured company database information,
including employees, leave balances, leave requests, attendance,
salary, departments, customers, products, orders, sales,
revenue, expenses, profit, or database records.

WEB:
Questions requiring current, latest, recent, or external
information from the internet.

Return only one word:

RAG
SQL
WEB

User Query:
{query}
"""

        response = self.llm.invoke(
            prompt
        )

        category = (
            response.content
            .strip()
            .upper()
        )

        if category not in [
            "RAG",
            "SQL",
            "WEB",
        ]:

            return "RAG"

        return category


router = QueryRouter()