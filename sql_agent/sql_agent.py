"""
Enterprise AI Assistant
Text To SQL Agent
"""

from __future__ import annotations

import sqlite3
import re

from llm.client import get_llm
from utils.config import DATABASE_PATH


class SQLAgent:
    """
    Converts natural language questions
    into SQL queries and executes them.
    """

    def __init__(self):

        self.llm = get_llm()
        self.database = DATABASE_PATH


    # ---------------------------------------------------------
    # Generate SQL
    # ---------------------------------------------------------

    def generate_sql(
        self,
        query: str
    ) -> str:

        prompt = f"""
You are an expert SQLite developer.

Generate only the SQL query.
Do not add explanation.
Do not use markdown.

Database:
SQLite

Available tables:
- customers
- employees
- sales

User question:
{query}

SQL:
"""

        response = self.llm.invoke(
            prompt
        )

        sql = response.content.strip()


        # Remove markdown if model adds it
        sql = sql.replace(
            "```sql",
            ""
        ).replace(
            "```",
            ""
        ).strip()


        return sql



    # ---------------------------------------------------------
    # Execute SQL
    # ---------------------------------------------------------

    def execute_sql(
        self,
        sql: str
    ):

        try:

            connection = sqlite3.connect(
                self.database
            )

            cursor = connection.cursor()


            cursor.execute(
                sql
            )


            result = cursor.fetchall()


            connection.close()


            return result


        except Exception as e:

            return {
                "error": str(e)
            }



    # ---------------------------------------------------------
    # Final Answer
    # ---------------------------------------------------------

    def answer(
        self,
        query: str
    ) -> str:


        sql = self.generate_sql(
            query
        )


        result = self.execute_sql(
            sql
        )


        if isinstance(result, dict):

            return (
                f"Database error: "
                f"{result['error']}"
            )


        prompt = f"""
You are an enterprise database assistant.

Answer the user's question using the database result.

Rules:
- Give only the final answer.
- Do not explain SQL.
- Do not say you need more information.
- Use the provided result.

Question:
{query}

SQL Query:
{sql}

Database Result:
{result}

Answer:
"""


        response = self.llm.invoke(
            prompt
        )


        return response.content.strip()



sql_agent = SQLAgent()



if __name__ == "__main__":

    question = (
        "How many customers are there?"
    )


    print("=" * 50)

    print(
        sql_agent.answer(
            question
        )
    )