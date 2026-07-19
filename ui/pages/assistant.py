"""
Enterprise AI Assistant
AI Assistant Page
"""

import streamlit as st

from workflow.assistant_graph import run_assistant


# =====================================================
# PAGE STYLES
# =====================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #64748B;
        margin-bottom: 25px;
    }

    .welcome {
        background: #F8FAFC;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E5E7EB;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# HELPER: DISPLAY SOURCES
# =====================================================

def display_sources(
    sources: list,
) -> None:

    if not sources:

        return

    normal_sources = []

    sql_queries = []

    for source in sources:

        if source.startswith(
            "SQL Query:"
        ):

            sql_queries.append(
                source.replace(
                    "SQL Query:",
                    "",
                    1,
                ).strip()
            )

        else:

            normal_sources.append(
                source
            )

    st.markdown(
        "### 📚 Sources"
    )

    for source in normal_sources:

        st.markdown(
            f"• {source}"
        )

    for sql_query in sql_queries:

        st.markdown(
            "🔍 **SQL Query**"
        )

        st.code(
            sql_query,
            language="sql",
        )


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =====================================================
# HEADER
# =====================================================

left, right = st.columns(
    [6, 1]
)


with left:

    st.markdown(
        """
        <div class="main-title">
            💬 Enterprise AI Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="subtitle">
            Ask questions about your documents,
            database, or the web.
        </div>
        """,
        unsafe_allow_html=True,
    )


with right:

    if st.button(
        "🗑 Clear Chat",
        width="stretch",
    ):

        st.session_state.messages = []

        st.rerun()


# =====================================================
# WELCOME SCREEN
# =====================================================

if len(
    st.session_state.messages
) == 0:

    st.html(
        """
        <div class="welcome">

            <h3>👋 Welcome!</h3>

            <p>
                Your Enterprise AI Assistant can help you with:
            </p>

            <p>
                • SQL Database Questions
                <br>
                • Enterprise Documents
                <br>
                • Current Web Research
                <br>
                • Business Insights
            </p>

            <p>
                Try asking:
            </p>

            <strong>
                "What is our total revenue?"
            </strong>

        </div>
        """
    )


# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    avatar = (

        "👤"

        if message["role"] == "user"

        else "🤖"

    )

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            route = message.get(
                "route",
                "",
            )

            reason = message.get(
                "reason",
                "",
            )

            sources = message.get(
                "sources",
                [],
            )

            if route:

                st.info(
                    f"🧠 Route: {route}\n\n"
                    f"💡 {reason}"
                )

            display_sources(
                sources
            )


# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input(
    "Ask anything..."
)


if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            query
        )

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner(
            "Analyzing your question..."
        ):

            result = run_assistant(
                query
            )

        answer = result.get(
            "answer",
            "No response generated.",
        )

        route = result.get(
            "route",
            "UNKNOWN",
        )

        reason = result.get(
            "reason",
            "",
        )

        sources = result.get(
            "sources",
            [],
        )

        st.markdown(
            answer
        )

        if route:

            st.info(
                f"🧠 Route: {route}\n\n"
                f"💡 {reason}"
            )

        display_sources(
            sources
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "route": route,
            "reason": reason,
            "sources": sources,
        }
    )