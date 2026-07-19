"""
Enterprise AI Assistant
SQL Agent
"""

from __future__ import annotations

from typing import Dict

from tools.sql_tool import sql_tool


class SQLAgent:
    """
    Executes SQL-based enterprise questions.

    Workflow:
        User Question
            ↓
        SQL Tool
            ↓
        SQL Query Generation
            ↓
        SQL Validation
            ↓
        SQL Execution
            ↓
        Return Results
    """

    def run(self, question: str) -> Dict:
        """
        Executes the SQL workflow.

        Returns:
        {
            "tool": "SQL",
            "success": True,
            "question": "...",
            "sql": "...",
            "rows": [...],
            "count": 10,
            "error": ""
        }
        """

        result = sql_tool.query(question)

        return {
            "tool": "SQL",
            "success": result["success"],
            "question": question,
            "sql": result.get("sql", ""),
            "rows": result.get("rows", []),
            "count": result.get("count", 0),
            "error": result.get("error", ""),
        }


sql_agent = SQLAgent()


if __name__ == "__main__":

    questions = [
        "Show all customers",
        "Total revenue",
        "Top selling products",
        "Employees in HR department",
        "Show total revenue and total expenses",
        "Show customers and their orders",
        "Show the number of employees in each department",
    ]

    for question in questions:

        print("=" * 70)
        print(question)

        response = sql_agent.run(question)

        print(response)