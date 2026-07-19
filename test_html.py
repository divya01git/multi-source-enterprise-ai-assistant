import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <div style="
        background:black;
        color:white;
        padding:30px;
        border-radius:20px;
    ">
        <h1>Hello Divya</h1>
        <p>This is HTML test</p>
    </div>
    """,
    unsafe_allow_html=True
)