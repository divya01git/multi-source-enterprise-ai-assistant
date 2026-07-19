"""
Enterprise AI Assistant
SQL Tool
"""

from __future__ import annotations

import math
import re
import sqlite3
from typing import Any, Dict, List, Set, Tuple

from langchain_core.output_parsers import StrOutputParser

from llm import get_llm
from utils.config import DATABASE_PATH
from utils.prompts import SQL_PROMPT


class SQLTool:
    """
    Enterprise SQL Tool.

    Responsibilities:
    - Read the SQLite schema
    - Generate SQL using the LLM
    - Validate generated SQL
    - Prevent unsafe SQL
    - Prevent Cartesian products
    - Prevent invalid multi-table aggregate queries
    - Validate query result correctness
    - Detect suspicious aggregate results
    - Execute read-only SQL
    - Return structured results
    """

    # ---------------------------------------------------------
    # SQL Keywords
    # ---------------------------------------------------------

    SQL_KEYWORDS = {
        "select",
        "from",
        "where",
        "join",
        "inner",
        "left",
        "right",
        "full",
        "outer",
        "cross",
        "on",
        "using",
        "group",
        "by",
        "order",
        "limit",
        "offset",
        "having",
        "as",
        "and",
        "or",
        "not",
        "null",
        "is",
        "in",
        "exists",
        "between",
        "like",
        "distinct",
        "case",
        "when",
        "then",
        "else",
        "end",
        "asc",
        "desc",
        "union",
        "all",
        "with",
        "recursive",
        "count",
        "sum",
        "avg",
        "min",
        "max",
        "round",
        "coalesce",
        "cast",
        "nullif",
        "true",
        "false",
    }

    BLOCKED_KEYWORDS = {
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "pragma",
        "vacuum",
        "reindex",
        "analyze",
    }

    AGGREGATE_FUNCTIONS = {
        "count",
        "sum",
        "avg",
        "min",
        "max",
        "total",
    }

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __init__(self) -> None:

        self.db_path = DATABASE_PATH

        self.llm = get_llm()

        self.chain = (
            SQL_PROMPT
            | self.llm
            | StrOutputParser()
        )

    # ---------------------------------------------------------
    # Database Connection
    # ---------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # Read Schema
    # ---------------------------------------------------------

    def get_schema(self) -> str:
        """
        Returns the SQLite schema in a format suitable for the LLM.
        """

        conn = self._connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
                """
            )

            tables = [
                row[0]
                for row in cursor.fetchall()
            ]

            schema = []

            for table in tables:

                cursor.execute(
                    f"PRAGMA table_info({self._quote_identifier(table)})"
                )

                columns = cursor.fetchall()

                column_text = ", ".join(
                    f"{column[1]} ({column[2]})"
                    for column in columns
                )

                schema.append(
                    f"{table}: {column_text}"
                )

            return "\n".join(schema)

        finally:

            conn.close()

    # ---------------------------------------------------------
    # Schema Metadata
    # ---------------------------------------------------------

    def _get_tables(self) -> Set[str]:
        """
        Returns all user-created database tables.
        """

        conn = self._connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
                """
            )

            return {
                row[0]
                for row in cursor.fetchall()
            }

        finally:

            conn.close()

    def _get_columns(self) -> Dict[str, Set[str]]:
        """
        Returns a mapping of table names to column names.
        """

        tables = self._get_tables()

        conn = self._connect()
        cursor = conn.cursor()

        columns: Dict[str, Set[str]] = {}

        try:

            for table in tables:

                cursor.execute(
                    f"PRAGMA table_info({self._quote_identifier(table)})"
                )

                columns[table] = {
                    row[1]
                    for row in cursor.fetchall()
                }

            return columns

        finally:

            conn.close()

    def _get_foreign_keys(self) -> List[Tuple[str, str, str, str]]:
        """
        Returns foreign-key relationships.

        Format:

        (
            source_table,
            source_column,
            target_table,
            target_column
        )
        """

        tables = self._get_tables()

        conn = self._connect()
        cursor = conn.cursor()

        relationships = []

        try:

            for table in tables:

                cursor.execute(
                    f"PRAGMA foreign_key_list({self._quote_identifier(table)})"
                )

                for row in cursor.fetchall():

                    target_table = row[2]
                    source_column = row[3]
                    target_column = row[4]

                    relationships.append(
                        (
                            table,
                            source_column,
                            target_table,
                            target_column,
                        )
                    )

            return relationships

        finally:

            conn.close()

    # ---------------------------------------------------------
    # SQL Generation
    # ---------------------------------------------------------

    def generate_sql(self, question: str) -> str:
        """
        Generates SQL using the LLM.
        """

        schema = self.get_schema()

        sql = self.chain.invoke(
            {
                "schema": schema,
                "question": question,
            }
        )

        sql = sql.strip()

        if sql.startswith("```"):

            sql = sql.replace("```sql", "")
            sql = sql.replace("```SQL", "")
            sql = sql.replace("```", "")
            sql = sql.strip()

        if sql.endswith(";"):

            sql = sql[:-1]

        return sql.strip()

    # ---------------------------------------------------------
    # SQL Normalization
    # ---------------------------------------------------------

    @staticmethod
    def _normalize_sql(sql: str) -> str:
        """
        Normalizes SQL for validation.

        Removes:
        - SQL comments
        - Excessive whitespace
        """

        sql = re.sub(
            r"/\*.*?\*/",
            " ",
            sql,
            flags=re.DOTALL,
        )

        sql = re.sub(
            r"--.*?$",
            " ",
            sql,
            flags=re.MULTILINE,
        )

        sql = re.sub(
            r"\s+",
            " ",
            sql,
        )

        return sql.strip()

    @staticmethod
    def _quote_identifier(identifier: str) -> str:
        """
        Safely quotes a SQLite identifier.
        """

        escaped = identifier.replace('"', '""')

        return f'"{escaped}"'

    # ---------------------------------------------------------
    # SQL Structure Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _strip_string_literals(sql: str) -> str:
        """
        Removes string literal contents from SQL while preserving
        the surrounding structure.
        """

        return re.sub(
            r"'(?:''|[^'])*'",
            "''",
            sql,
        )

    @staticmethod
    def _extract_table_references(sql: str) -> List[str]:
        """
        Extracts table references from FROM and JOIN clauses.
        """

        table_pattern = re.compile(
            r"""
            \b
            (?:FROM|JOIN)
            \s+
            (?P<table>
                (?:"[^"]+"|`[^`]+`|\[[^\]]+\]|[A-Za-z_][A-Za-z0-9_]*)
            )
            """,
            re.IGNORECASE | re.VERBOSE,
        )

        tables = []

        for match in table_pattern.finditer(sql):

            table = match.group("table").strip()

            if table.startswith('"') and table.endswith('"'):
                table = table[1:-1]

            elif table.startswith("`") and table.endswith("`"):
                table = table[1:-1]

            elif table.startswith("[") and table.endswith("]"):
                table = table[1:-1]

            tables.append(table)

        return tables

    @staticmethod
    def _has_top_level_comma_join(sql: str) -> bool:
        """
        Detects implicit comma joins in the top-level FROM clause.
        """

        from_match = re.search(
            r"\bFROM\b",
            sql,
            flags=re.IGNORECASE,
        )

        if not from_match:
            return False

        from_clause = sql[from_match.end():]

        stop_match = re.search(
            r"\b(?:WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|OFFSET)\b",
            from_clause,
            flags=re.IGNORECASE,
        )

        if stop_match:
            from_clause = from_clause[:stop_match.start()]

        depth = 0
        in_string = False

        for character in from_clause:

            if character == "'":

                in_string = not in_string
                continue

            if in_string:
                continue

            if character == "(":

                depth += 1

            elif character == ")":

                depth = max(0, depth - 1)

            elif character == "," and depth == 0:

                return True

        return False

    @staticmethod
    def _has_cross_join(sql: str) -> bool:
        """
        Detects explicit CROSS JOIN usage.
        """

        return bool(
            re.search(
                r"\bCROSS\s+JOIN\b",
                sql,
                flags=re.IGNORECASE,
            )
        )

    @staticmethod
    def _has_join_without_condition(sql: str) -> bool:
        """
        Detects JOIN clauses without ON or USING.
        """

        join_pattern = re.compile(
            r"""
            \b
            (?:
                INNER\s+JOIN
                |
                LEFT(?:\s+OUTER)?\s+JOIN
                |
                RIGHT(?:\s+OUTER)?\s+JOIN
                |
                FULL(?:\s+OUTER)?\s+JOIN
                |
                JOIN
            )
            \s+
            [A-Za-z_][A-Za-z0-9_]*
            (?:
                \s+
                (?:AS\s+)?
                [A-Za-z_][A-Za-z0-9_]*
            )?
            (?=
                \s+
                (?:ON|USING)
                \b
                |
                \s+
                (?:INNER|LEFT|RIGHT|FULL|JOIN)
                \b
                |
                \s+
                (?:WHERE|GROUP|ORDER|LIMIT|HAVING)
                \b
                |
                $
            )
            """,
            re.IGNORECASE | re.VERBOSE,
        )

        return bool(
            join_pattern.search(sql)
        )

    # ---------------------------------------------------------
    # Aggregate Validation
    # ---------------------------------------------------------

    @classmethod
    def _contains_aggregate(cls, sql: str) -> bool:
        """
        Detects aggregate functions.
        """

        return bool(
            re.search(
                r"\b(?:COUNT|SUM|AVG|MIN|MAX|TOTAL)\s*\(",
                sql,
                flags=re.IGNORECASE,
            )
        )

    @staticmethod
    def _has_group_by(sql: str) -> bool:
        """
        Detects GROUP BY.
        """

        return bool(
            re.search(
                r"\bGROUP\s+BY\b",
                sql,
                flags=re.IGNORECASE,
            )
        )

    @staticmethod
    def _contains_count_star(sql: str) -> bool:
        """
        Detects COUNT(*).
        """

        return bool(
            re.search(
                r"\bCOUNT\s*\(\s*\*\s*\)",
                sql,
                flags=re.IGNORECASE,
            )
        )

    @staticmethod
    def _contains_count_distinct(sql: str) -> bool:
        """
        Detects COUNT(DISTINCT ...).
        """

        return bool(
            re.search(
                r"\bCOUNT\s*\(\s*DISTINCT\b",
                sql,
                flags=re.IGNORECASE,
            )
        )

    def _validate_multi_table_aggregate(
        self,
        sql: str,
        tables: List[str],
    ) -> None:
        """
        Protects aggregate queries involving multiple tables.
        """

        if not self._contains_aggregate(sql):
            return

        if len(set(tables)) <= 1:
            return

        if self._has_top_level_comma_join(sql):

            raise ValueError(
                "Unsafe aggregate query rejected: "
                "implicit comma joins can create Cartesian products "
                "and inflate aggregate results."
            )

        if self._has_cross_join(sql):

            raise ValueError(
                "Unsafe aggregate query rejected: "
                "CROSS JOIN can multiply rows and produce incorrect "
                "aggregate results."
            )

        if self._has_join_without_condition(sql):

            raise ValueError(
                "Unsafe aggregate query rejected: "
                "every JOIN in a multi-table aggregate query must "
                "have an explicit ON or USING condition."
            )

    # ---------------------------------------------------------
    # Foreign-Key Join Validation
    # ---------------------------------------------------------

    def _validate_join_relationships(
        self,
        sql: str,
        tables: List[str],
    ) -> None:
        """
        Validates that multi-table joins are connected through
        a meaningful relationship.
        """

        unique_tables = set(tables)

        if len(unique_tables) <= 1:
            return

        relationships = self._get_foreign_keys()

        if not relationships:
            return

        normalized_sql = sql.lower()

        table_pairs = set()

        for source_table, _, target_table, _ in relationships:

            if (
                source_table in unique_tables
                and target_table in unique_tables
            ):

                table_pairs.add(
                    (
                        source_table.lower(),
                        target_table.lower(),
                    )
                )

                table_pairs.add(
                    (
                        target_table.lower(),
                        source_table.lower(),
                    )
                )

        if not table_pairs:
            return

        relationship_found = False

        for source_table, target_table in table_pairs:

            if (
                source_table in normalized_sql
                and target_table in normalized_sql
            ):

                relationship_found = True
                break

        if not relationship_found:

            raise ValueError(
                "Suspicious multi-table query rejected: "
                "the selected tables do not appear to have a known "
                "foreign-key relationship."
            )

    # ---------------------------------------------------------
    # SQLite Query Validation
    # ---------------------------------------------------------

    def _validate_sqlite_query(self, sql: str) -> None:
        """
        Uses SQLite's query planner to validate:

        - SQL syntax
        - Table names
        - Column names
        - Function usage
        - JOIN structure
        """

        conn = self._connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                f"EXPLAIN QUERY PLAN {sql}"
            )

            cursor.fetchall()

        finally:

            conn.close()

    # ---------------------------------------------------------
    # Result Validation Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _is_numeric(value: Any) -> bool:
        """
        Returns True if a value is numeric.
        """

        return isinstance(
            value,
            (int, float),
        ) and not isinstance(
            value,
            bool,
        )

    @staticmethod
    def _is_finite_number(value: Any) -> bool:
        """
        Prevents NaN and infinite numeric results.
        """

        if not SQLTool._is_numeric(value):
            return False

        return math.isfinite(
            float(value)
        )

    @staticmethod
    def _extract_select_clause(sql: str) -> str:
        """
        Extracts the SELECT clause before FROM.

        This is used only for lightweight result validation.
        """

        match = re.search(
            r"^\s*SELECT\s+(.*?)\s+FROM\b",
            sql,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return ""

        return match.group(1).strip()

    @staticmethod
    def _extract_selected_aliases(sql: str) -> List[str]:
        """
        Extracts aliases from aggregate expressions.

        Example:

            SELECT COUNT(*) AS total_employees

        returns:

            ["total_employees"]
        """

        select_clause = SQLTool._extract_select_clause(
            sql
        )

        if not select_clause:
            return []

        aliases = re.findall(
            r"""
            \b(?:COUNT|SUM|AVG|MIN|MAX|TOTAL)
            \s*\([^)]*\)
            \s+
            AS
            \s+
            ([A-Za-z_][A-Za-z0-9_]*)
            """,
            select_clause,
            flags=re.IGNORECASE | re.VERBOSE,
        )

        return aliases

    @staticmethod
    def _extract_aggregate_expressions(sql: str) -> List[str]:
        """
        Extracts aggregate expressions from the SELECT clause.
        """

        select_clause = SQLTool._extract_select_clause(
            sql
        )

        if not select_clause:
            return []

        expressions = re.findall(
            r"""
            \b
            (COUNT|SUM|AVG|MIN|MAX|TOTAL)
            \s*
            \(
                [^)]*
            \)
            """,
            select_clause,
            flags=re.IGNORECASE | re.VERBOSE,
        )

        return expressions

    @staticmethod
    def _has_distinct_in_select(sql: str) -> bool:
        """
        Detects SELECT DISTINCT.
        """

        return bool(
            re.search(
                r"^\s*SELECT\s+DISTINCT\b",
                sql,
                flags=re.IGNORECASE,
            )
        )

    def _validate_result_values(
        self,
        sql: str,
        rows: List[Dict],
    ) -> None:
        """
        Validates returned values.

        Checks:

        - Numeric aggregate values are finite
        - COUNT results are never negative
        - Aggregate aliases do not contain invalid numeric values
        """

        if not rows:
            return

        aggregate_query = self._contains_aggregate(
            sql
        )

        if not aggregate_query:
            return

        for row in rows:

            for column_name, value in row.items():

                if self._is_numeric(value):

                    if not self._is_finite_number(value):

                        raise ValueError(
                            "Invalid aggregate result detected: "
                            f"column '{column_name}' contains a "
                            "non-finite numeric value."
                        )

                    if (
                        "count" in column_name.lower()
                        and value < 0
                    ):

                        raise ValueError(
                            "Invalid aggregate result detected: "
                            f"COUNT result '{column_name}' cannot "
                            "be negative."
                        )

    def _validate_aggregate_shape(
        self,
        sql: str,
        rows: List[Dict],
    ) -> None:
        """
        Validates the shape of aggregate results.

        A pure aggregate query without GROUP BY should normally
        return exactly one row.

        Example:

            SELECT COUNT(*) FROM employees

        should return one row even when the table is empty.

        This catches malformed or unexpected result structures.
        """

        if not self._contains_aggregate(sql):
            return

        if self._has_group_by(sql):
            return

        if not rows:

            raise ValueError(
                "Aggregate query returned no result row."
            )

        if len(rows) != 1:

            raise ValueError(
                "Aggregate query without GROUP BY returned "
                f"{len(rows)} rows instead of exactly one."
            )

    def _validate_join_aggregate_result(
        self,
        sql: str,
        rows: List[Dict],
    ) -> None:
        """
        Performs conservative post-execution validation for
        multi-table aggregate queries.

        The purpose is not to guess the business answer.

        Instead, it detects situations where an aggregate query
        structurally becomes suspicious because of joined rows.

        Important:

        A valid one-to-many aggregate is allowed.

        For example:

            SELECT
                p.product_name,
                SUM(o.quantity)
            FROM products p
            JOIN orders o
                ON p.product_id = o.product_id
            GROUP BY p.product_name

        is valid.

        This validation focuses on suspicious aggregate outputs
        and prevents silently accepting malformed result shapes.
        """

        tables = self._extract_table_references(
            sql
        )

        if len(set(tables)) <= 1:
            return

        if not self._contains_aggregate(sql):
            return

        if not rows:
            return

        aggregate_aliases = self._extract_selected_aliases(
            sql
        )

        for alias in aggregate_aliases:

            for row in rows:

                if alias not in row:
                    continue

                value = row[alias]

                if not self._is_numeric(value):
                    continue

                if not self._is_finite_number(value):

                    raise ValueError(
                        "Suspicious joined aggregate result: "
                        f"'{alias}' contains an invalid numeric value."
                    )

        # A multi-table aggregate without GROUP BY should already
        # have exactly one row after the aggregate-shape check.
        #
        # A grouped multi-table aggregate is allowed because one row
        # per group is expected.
        #
        # We deliberately do not reject large valid totals because
        # the correct value depends on the actual business data.

    def validate_results(
        self,
        sql: str,
        rows: List[Dict],
    ) -> None:
        """
        Performs post-execution result validation.

        Validation layers:

        1. Aggregate result shape
        2. Numeric value validity
        3. Multi-table aggregate sanity checks
        """

        self._validate_aggregate_shape(
            sql,
            rows,
        )

        self._validate_result_values(
            sql,
            rows,
        )

        self._validate_join_aggregate_result(
            sql,
            rows,
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_query(self, sql: str) -> None:
        """
        Performs layered SQL validation before execution.

        Validation layers:

        1. Basic SQL structure
        2. Read-only safety
        3. Multiple-statement prevention
        4. Cartesian-product protection
        5. Aggregate correctness protection
        6. Relationship validation
        7. SQLite syntax/schema validation
        """

        if not sql or not sql.strip():

            raise ValueError(
                "Generated SQL query is empty."
            )

        normalized = self._normalize_sql(
            sql
        )

        if not normalized:

            raise ValueError(
                "Generated SQL query is empty."
            )

        sql_without_strings = self._strip_string_literals(
            normalized
        )

        lowered = sql_without_strings.lower()

        # -----------------------------------------------------
        # Only SELECT queries are allowed.
        # -----------------------------------------------------

        if not re.match(
            r"^select\b",
            lowered,
        ):

            raise ValueError(
                "Only SELECT statements are allowed."
            )

        # -----------------------------------------------------
        # Prevent multiple SQL statements.
        # -----------------------------------------------------

        if ";" in normalized:

            raise ValueError(
                "Multiple SQL statements are not allowed."
            )

        # -----------------------------------------------------
        # Block unsafe SQL keywords.
        # -----------------------------------------------------

        keyword_pattern = re.compile(
            r"\b("
            + "|".join(
                re.escape(keyword)
                for keyword in self.BLOCKED_KEYWORDS
            )
            + r")\b",
            flags=re.IGNORECASE,
        )

        blocked_match = keyword_pattern.search(
            sql_without_strings
        )

        if blocked_match:

            raise ValueError(
                "Blocked SQL keyword detected: "
                f"{blocked_match.group(1)}"
            )

        # -----------------------------------------------------
        # Read database metadata.
        # -----------------------------------------------------

        tables = self._extract_table_references(
            sql_without_strings
        )

        known_tables = self._get_tables()

        unknown_tables = {
            table
            for table in tables
            if table not in known_tables
        }

        if unknown_tables:

            raise ValueError(
                "Unknown table(s) referenced: "
                + ", ".join(
                    sorted(unknown_tables)
                )
            )

        # -----------------------------------------------------
        # Prevent implicit Cartesian products.
        # -----------------------------------------------------

        if self._has_top_level_comma_join(
            sql_without_strings
        ):

            raise ValueError(
                "Implicit comma joins are not allowed because "
                "they can create Cartesian products."
            )

        # -----------------------------------------------------
        # Prevent explicit CROSS JOIN.
        # -----------------------------------------------------

        if self._has_cross_join(
            sql_without_strings
        ):

            raise ValueError(
                "CROSS JOIN is not allowed because it can create "
                "Cartesian products and incorrect aggregates."
            )

        # -----------------------------------------------------
        # Prevent JOIN without ON/USING.
        # -----------------------------------------------------

        if self._has_join_without_condition(
            sql_without_strings
        ):

            raise ValueError(
                "JOIN without an ON or USING condition is not allowed."
            )

        # -----------------------------------------------------
        # Validate multi-table aggregate queries.
        # -----------------------------------------------------

        self._validate_multi_table_aggregate(
            sql_without_strings,
            tables,
        )

        # -----------------------------------------------------
        # Validate table relationships.
        # -----------------------------------------------------

        self._validate_join_relationships(
            sql_without_strings,
            tables,
        )

        # -----------------------------------------------------
        # Let SQLite validate syntax and columns.
        # -----------------------------------------------------

        self._validate_sqlite_query(
            normalized
        )

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    def execute(
        self,
        sql: str,
    ) -> List[Dict]:
        """
        Validates and executes a read-only SQL query.
        """

        self.validate_query(
            sql
        )

        conn = self._connect()

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        try:

            cursor.execute(
                sql
            )

            rows = [
                dict(row)
                for row in cursor.fetchall()
            ]

            self.validate_results(
                sql,
                rows,
            )

            return rows

        finally:

            conn.close()

    # ---------------------------------------------------------
    # Main Interface
    # ---------------------------------------------------------

    def query(
        self,
        question: str,
    ) -> dict:
        """
        Complete SQL workflow.

        Flow:

            Question
                ↓
            Generate SQL
                ↓
            Validate SQL
                ↓
            Execute SQL
                ↓
            Validate Results
                ↓
            Return Results
        """

        try:

            sql = self.generate_sql(
                question
            )

            results = self.execute(
                sql
            )

            return {
                "success": True,
                "question": question,
                "sql": sql,
                "rows": results,
                "count": len(results),
                "error": "",
            }

        except Exception as exc:

            return {
                "success": False,
                "question": question,
                "sql": "",
                "rows": [],
                "count": 0,
                "error": str(exc),
            }


sql_tool = SQLTool()


if __name__ == "__main__":

    test_questions = [
        "How many employees are there?",
        "What is the total revenue?",
        "Show the top selling products.",
        "How many employees are in each department?",
        "Show customers and their orders.",
    ]

    for question in test_questions:

        print("=" * 70)
        print(question)

        response = sql_tool.query(
            question
        )

        print(response)