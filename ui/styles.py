import streamlit as st


def load_css():
    st.markdown("""
    <style>

    .main .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        max-width:1400px;
    }

    .hero{
        padding:35px;
        border-radius:18px;
        background:linear-gradient(135deg,#2563eb,#1d4ed8);
        color:white;
        margin-bottom:25px;
    }

    .hero h1{
        margin:0;
        font-size:42px;
    }

    .hero p{
        font-size:18px;
        opacity:.9;
    }

    div[data-testid="stMetric"]{
        background:#f8fafc;
        border-radius:16px;
        padding:18px;
        border:1px solid #dbeafe;
    }

    section[data-testid="stSidebar"]{
        border-right:1px solid #e2e8f0;
    }

    </style>
    """, unsafe_allow_html=True)