"""
Enterprise AI Assistant
Web Search
"""

import streamlit as st
import pandas as pd

from agents.web_agent import web_agent


# -------------------------------------------------------
# CSS
# -------------------------------------------------------

st.markdown("""
<style>

.header{
    background:linear-gradient(90deg,#0F172A,#1E3A8A);
    color:white;
    padding:22px;
    border-radius:18px;
    margin-bottom:25px;
}

.result-card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:16px;
    padding:18px;
    margin-bottom:15px;
    box-shadow:0 2px 8px rgba(0,0,0,.05);
}

.result-card h4{
    margin-bottom:8px;
}

.result-card p{
    color:#475569;
    line-height:1.6;
}

.source-link{
    color:#2563EB;
    text-decoration:none;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.markdown("""
<div class="header">

<h2>🌐 Web Research</h2>

<p>
Search the web and gather the latest information with AI-powered summaries.
</p>

</div>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "web_search_history" not in st.session_state:

    st.session_state.web_search_history = []


# -------------------------------------------------------
# Metrics
# -------------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Search Engine",
        "Online"
    )


with c2:

    st.metric(
        "AI Summary",
        "Ready"
    )


with c3:

    st.metric(
        "Status",
        "Connected"
    )


st.divider()


# -------------------------------------------------------
# Search
# -------------------------------------------------------

query = st.text_input(
    "🔍 Search the web...",
    placeholder="Example: Latest AI trends in healthcare"
)


search = st.button(
    "🔎 Search",
    width="stretch"
)


# -------------------------------------------------------
# Execute Search
# -------------------------------------------------------

if search:

    if query.strip() == "":

        st.warning(
            "Please enter a search query."
        )

    else:

        with st.spinner(
            "Searching the web and generating AI summary..."
        ):

            try:

                results = web_agent.search_web(
                    query
                )


                answer = web_agent.generate_answer(
                    query,
                    results
                )


                st.session_state.web_search_history.insert(
                    0,
                    {
                        "Query": query,
                        "Status": "Completed"
                    }
                )


                st.success(
                    f'Search completed for "{query}"'
                )


                # -------------------------------------------------------
                # AI Summary
                # -------------------------------------------------------

                st.subheader(
                    "🤖 AI Summary"
                )


                st.info(
                    answer
                )


                # -------------------------------------------------------
                # Sources
                # -------------------------------------------------------

                st.subheader(
                    "🌐 Top Sources"
                )


                if not results:

                    st.warning(
                        "No web results were found."
                    )


                else:

                    for i, result in enumerate(
                        results[:3],
                        start=1
                    ):

                        title = result.get(
                            "title",
                            "Untitled Result"
                        )


                        content = result.get(
                            "content",
                            "No description available."
                        )


                        url = result.get(
                            "url",
                            ""
                        )


                        st.markdown(
                            f"""
<div class="result-card">

<h4>Result {i}: {title}</h4>

<p>
{content}
</p>

</div>
""",
                            unsafe_allow_html=True
                        )


                        if url:

                            st.markdown(
                                f"🔗 [Read full source]({url})"
                            )


            except Exception as e:

                st.error(
                    f"Web search failed: {e}"
                )


# -------------------------------------------------------
# Recent Searches
# -------------------------------------------------------

st.divider()


st.subheader(
    "🕘 Recent Searches"
)


if st.session_state.web_search_history:

    history = pd.DataFrame(
        st.session_state.web_search_history
    )


else:

    history = pd.DataFrame(
        {
            "Query": [],
            "Status": []
        }
    )


st.dataframe(
    history,
    width="stretch",
    hide_index=True
)


st.success(
    "✅ Web Research module is ready."
)