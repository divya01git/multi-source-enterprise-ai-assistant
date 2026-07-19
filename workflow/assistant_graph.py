"""
Enterprise AI Assistant
LangGraph Main Workflow
"""

from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from agents.planner import planner
from agents.rag_agent import rag_agent
from agents.sql_agent import sql_agent
from agents.web_agent import web_agent
from agents.synthesizer import synthesizer


# =====================================================
# STATE DEFINITION
# =====================================================

class AssistantState(TypedDict, total=False):

    query: str

    route: str

    reason: str

    context: Any

    sources: list

    answer: str


# =====================================================
# DOCUMENT INTENT DETECTION
# =====================================================

def has_explicit_document_intent(
    query: str,
) -> bool:
    """
    Detects whether the user explicitly asks for information
    from an internal document.

    Document intent takes priority over generic SQL keywords.

    Example:

        "According to the annual report, why did revenue decline?"

    contains the SQL keyword "revenue", but the actual source
    requested by the user is the annual report.

    Therefore the correct route is:

        RAG

    and not:

        SQL + RAG
    """

    query_lower = query.lower().strip()

    document_keywords = [

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

    return any(
        keyword in query_lower
        for keyword in document_keywords
    )


# =====================================================
# PLANNER NODE
# =====================================================

def planner_node(
    state: AssistantState,
):

    query = state.get(
        "query",
        "",
    )

    # -------------------------------------------------
    # DOCUMENT PRIORITY OVERRIDE
    # -------------------------------------------------
    # Explicit document references must always go to RAG.
    #
    # This prevents the LLM planner from selecting SQL because
    # the question contains words such as:
    #
    # revenue
    # employees
    # sales
    # profit
    #
    # Example:
    #
    # "According to the annual report, why did revenue decline?"
    #
    # Correct:
    #
    # RAG
    #
    # Incorrect:
    #
    # SQL + RAG
    # -------------------------------------------------

   

    # -------------------------------------------------
    # LLM PLANNER
    # -------------------------------------------------

    plan = planner.plan(
        query,
    )

    tools = plan.get(
        "tools",
        ["RAG"],
    )

    tools = [

        tool.upper()

        for tool in tools

        if isinstance(
            tool,
            str,
        )

        and tool.upper()
        in {
            "SQL",
            "RAG",
            "WEB",
        }

    ]

    if not tools:

        tools = [
            "RAG",
        ]

    state["route"] = " + ".join(
        tools
    )

    state["reason"] = plan.get(
        "reason",
        "",
    )

    state["context"] = []

    state["sources"] = []

    return state


# =====================================================
# TOOL EXECUTION NODE
# =====================================================

def tools_node(
    state: AssistantState,
):

    query = state.get(
        "query",
        "",
    )

    route = state.get(
        "route",
        "RAG",
    )

    selected_tools = [

        tool.strip().upper()

        for tool in route.split(
            "+"
        )

    ]

    contexts = []

    sources = []

    # -------------------------------------------------
    # RAG
    # -------------------------------------------------

    if "RAG" in selected_tools:

        rag_result = rag_agent.run(
            query,
        )

        contexts.append(

            f"""
DOCUMENT KNOWLEDGE:

{rag_result}
"""

        )

        sources.append(

            "📄 Company Documents (RAG) — Annual_Report.pdf"

        )

    # -------------------------------------------------
    # SQL
    # -------------------------------------------------

    if "SQL" in selected_tools:

        sql_result = sql_agent.run(
            query,
        )

        contexts.append(

            f"""
DATABASE RESULT:

{sql_result}
"""

        )

        sources.append(

            "🗄️ Company Database (SQL)"

        )

        if isinstance(
            sql_result,
            dict,
        ):

            sql_query = sql_result.get(
                "sql",
                "",
            )

            if sql_query:

                sources.append(

                    f"""
🔍 SQL Query:

{sql_query}
"""

                )

    # -------------------------------------------------
    # WEB
    # -------------------------------------------------

    if "WEB" in selected_tools:

        web_result = web_agent.run(
            query,
        )

        # -------------------------------------------------
        # Web Answer
        # -------------------------------------------------

        if isinstance(
            web_result,
            dict,
        ):

            web_answer = web_result.get(
                "answer",
                "",
            )

            web_results = web_result.get(
                "results",
                [],
            )

        else:

            web_answer = str(
                web_result
            )

            web_results = []

        contexts.append(

            f"""
WEB INFORMATION:

{web_answer}
"""

        )

        # -------------------------------------------------
        # Web Source Header
        # -------------------------------------------------

        sources.append(

            "🌐 Web Search"

        )

        # -------------------------------------------------
        # Actual Web Sources
        # -------------------------------------------------

        for item in web_results:

            if not isinstance(
                item,
                dict,
            ):

                continue

            title = item.get(
                "title",
                "",
            ).strip()

            url = item.get(
                "url",
                "",
            ).strip()

            if title and url:

                sources.append(

                    f"🔗 {title}\n{url}"

                )

            elif url:

                sources.append(

                    f"🔗 {url}"

                )

            elif title:

                sources.append(

                    f"🔗 {title}"

                )

    state["context"] = contexts

    state["sources"] = sources

    return state


# =====================================================
# SYNTHESIZER NODE
# =====================================================

def synthesizer_node(
    state: AssistantState,
):

    query = state.get(
        "query",
        "",
    )

    context = state.get(
        "context",
        [],
    )

    sources = state.get(
        "sources",
        [],
    )

    combined_context = "\n\n".join(
        context
    )

    answer = synthesizer.synthesize(
        query,
        combined_context,
        sources,
    )

    state["answer"] = answer

    return state


# =====================================================
# ROUTER
# =====================================================

def route_selector(
    state: AssistantState,
):

    return "tools"


# =====================================================
# BUILD GRAPH
# =====================================================

workflow = StateGraph(
    AssistantState
)

workflow.add_node(
    "planner",
    planner_node,
)

workflow.add_node(
    "tools",
    tools_node,
)

workflow.add_node(
    "synthesizer",
    synthesizer_node,
)

workflow.set_entry_point(
    "planner",
)

workflow.add_conditional_edges(
    "planner",
    route_selector,
    {
        "tools": "tools",
    },
)

workflow.add_edge(
    "tools",
    "synthesizer",
)

workflow.add_edge(
    "synthesizer",
    END,
)

assistant_graph = workflow.compile()


# =====================================================
# PUBLIC RUNNER
# =====================================================

def run_assistant(
    query: str,
) -> dict:

    """
    Executes the LangGraph workflow.

    Returns:

    {
        "answer": "...",
        "route": "...",
        "reason": "...",
        "sources": [...]
    }
    """

    result = assistant_graph.invoke(
        {
            "query": query,
        }
    )

    return {

        "answer": result.get(
            "answer",
            "No response generated.",
        ),

        "route": result.get(
            "route",
            "RAG",
        ),

        "reason": result.get(
            "reason",
            "",
        ),

        "sources": result.get(
            "sources",
            [],
        ),

    }