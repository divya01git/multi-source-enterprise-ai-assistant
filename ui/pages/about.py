"""
Enterprise AI Assistant
About
"""

import streamlit as st

# ---------------------------------------------------
# CSS
# ---------------------------------------------------

st.markdown("""
<style>

.header{
    background:linear-gradient(90deg,#0F172A,#1E3A8A);
    color:white;
    padding:24px;
    border-radius:18px;
    margin-bottom:25px;
}

.feature-card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:16px;
    padding:18px;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,.05);
}

.tech-card{
    background:#F8FAFC;
    border-radius:14px;
    padding:15px;
    border:1px solid #E5E7EB;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.markdown("""
<div class="header">

<h2>ℹ Enterprise AI Assistant</h2>

<p>
An enterprise-grade Generative AI platform designed to combine structured data,
documents, and web intelligence into one intelligent assistant.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Overview
# ---------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Version", "1.0")

with c2:
    st.metric("Status", "Stable")

with c3:
    st.metric("Modules", "6")

st.divider()

# ---------------------------------------------------
# Features
# ---------------------------------------------------

st.subheader("Core Features")

col1, col2, col3 = st.columns(3)

features = [
    ("📄", "Document Intelligence", "Retrieval-Augmented Generation (RAG)"),
    ("🗄", "SQL Intelligence", "Natural language to SQL queries"),
    ("🌐", "Web Research", "AI-powered web search and summaries"),
    ("🤖", "AI Planning", "Task orchestration and intelligent reasoning"),
    ("📊", "Business Insights", "Actionable analytics and reporting"),
    ("⚡", "Fast Responses", "Optimized enterprise workflows")
]

for i, (icon, title, desc) in enumerate(features):
    with [col1, col2, col3][i % 3]:
        st.markdown(f"""
<div class="feature-card">
<h2>{icon}</h2>
<h4>{title}</h4>
<p>{desc}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# Technology Stack
# ---------------------------------------------------

st.subheader("Technology Stack")

tech = [
    "🐍 Python",
    "⚡ Streamlit",
    "🗄 SQLite",
    "🦜 LangChain",
    "🤖 OpenAI-Compatible LLM",
    "📈 Plotly"
]

cols = st.columns(3)

for i, item in enumerate(tech):
    with cols[i % 3]:
        st.markdown(
            f"<div class='tech-card'>{item}</div>",
            unsafe_allow_html=True
        )

st.divider()

# ---------------------------------------------------
# Project Information
# ---------------------------------------------------

st.subheader("Project")

st.info("""
**Enterprise AI Assistant** is a unified AI platform that enables users to:

- Query SQL databases using natural language
- Search enterprise documents with RAG
- Retrieve information from the web
- Generate AI-powered business insights
- Access multiple AI capabilities through a single interface

Built as a production-style enterprise application using modern Python and Generative AI technologies.
""")

st.success("🚀 Enterprise AI Assistant is ready for demonstration.")
