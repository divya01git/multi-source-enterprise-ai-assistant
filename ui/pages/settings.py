"""
Enterprise AI Assistant
Settings
"""

import streamlit as st

# ----------------------------------------------------
# CSS
# ----------------------------------------------------

st.markdown("""
<style>

.header{
    background:linear-gradient(90deg,#0F172A,#1E3A8A);
    color:white;
    padding:22px;
    border-radius:18px;
    margin-bottom:25px;
}

.section{
    background:white;
    padding:20px;
    border-radius:16px;
    border:1px solid #E5E7EB;
    margin-bottom:20px;
    box-shadow:0 2px 8px rgba(0,0,0,.05);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.markdown("""
<div class="header">

<h2>⚙ Enterprise Settings</h2>

<p>
Configure your Enterprise AI Assistant and system preferences.
</p>

</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# General
# ----------------------------------------------------

st.subheader("General Settings")

dark_mode = st.toggle(
    "🌙 Dark Mode",
    value=True
)

show_sources = st.toggle(
    "📄 Show Sources",
    value=True
)

verbose = st.toggle(
    "🧠 Verbose Reasoning",
    value=False
)

st.divider()

# ----------------------------------------------------
# AI Configuration
# ----------------------------------------------------

st.subheader("AI Configuration")

model = st.selectbox(
    "AI Model",
    [
        "Llama 3",
        "Gemma",
        "DeepSeek",
        "Mixtral"
    ]
)

temperature = st.slider(
    "Temperature",
    0.0,
    1.0,
    0.3
)

max_tokens = st.slider(
    "Max Tokens",
    256,
    4096,
    2048
)

st.divider()

# ----------------------------------------------------
# System Status
# ----------------------------------------------------

st.subheader("System Status")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Database",
        "Connected"
    )

with c2:
    st.metric(
        "RAG",
        "Ready"
    )

with c3:
    st.metric(
        "Web Search",
        "Online"
    )

st.divider()

# ----------------------------------------------------
# About Configuration
# ----------------------------------------------------

st.subheader("Application")

st.info("""
Enterprise AI Assistant

Version: 1.0

Environment: Development

Framework: Streamlit
""")

st.divider()

# ----------------------------------------------------
# Buttons
# ----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):
        st.success("Settings saved successfully.")

with col2:

    if st.button(
        "↺ Reset",
        use_container_width=True
    ):
        st.warning("Settings reset.")