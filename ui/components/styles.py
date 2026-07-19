"""
Enterprise Dashboard Styles
"""

from __future__ import annotations

import streamlit as st


def load_styles() -> None:

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL LAYOUT
        ===================================================== */

        .main .block-container {

            max-width: 1450px;

            padding-top: 1.5rem;

            padding-bottom: 3rem;

            padding-left: 2rem;

            padding-right: 2rem;

        }


        /* =====================================================
           HIDE STREAMLIT DEFAULT UI
        ===================================================== */

        #MainMenu {

            visibility: hidden;

        }


        footer {

            visibility: hidden;

        }


        header {

            visibility: hidden;

        }


        /* =====================================================
           HERO SECTION
        ===================================================== */

        .hero {

            background:
                linear-gradient(
                    135deg,
                    #1e3a8a,
                    #2563eb
                );

            border-radius: 22px;

            padding: 32px 38px;

            color: white;

            margin-bottom: 28px;

            box-shadow:
                0 14px 35px
                rgba(30, 58, 138, 0.22);

        }


        .hero h1 {

            margin: 0;

            font-size: 36px;

            font-weight: 750;

            letter-spacing: -0.5px;

        }


        .hero p {

            margin-top: 8px;

            margin-bottom: 0;

            opacity: 0.88;

            font-size: 16px;

        }


        /* =====================================================
           METRIC CARDS
        ===================================================== */

        .metric-card {

            background: #ffffff;

            border: 1px solid #e5e7eb;

            border-radius: 18px;

            padding: 22px;

            min-height: 150px;

            width: 100%;

            max-width: 100%;

            box-sizing: border-box;

            overflow: hidden;

            box-shadow:
                0 6px 18px
                rgba(15, 23, 42, 0.06);

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;

            margin-bottom: 18px;

        }


        .metric-card:hover {

            transform: translateY(-4px);

            box-shadow:
                0 12px 28px
                rgba(15, 23, 42, 0.12);

        }


        .metric-icon {

            font-size: 28px;

            margin-bottom: 12px;

        }


        .metric-title {

            color: #64748b;

            font-size: 14px;

            font-weight: 600;

            letter-spacing: 0.2px;

        }


        .metric-value {

            color: #0f172a;

            font-size: clamp(20px, 2.2vw, 30px);

            font-weight: 750;

            margin-top: 6px;

            line-height: 1.2;

            max-width: 100%;

            overflow-wrap: anywhere;

            word-break: break-word;

        }


        .metric-delta {

            color: #059669;

            font-size: 13px;

            font-weight: 600;

            margin-top: 8px;

        }


        /* =====================================================
           SECTION TITLES
        ===================================================== */

        .section-title {

            color: #0f172a;

            font-size: 24px;

            font-weight: 750;

            margin-top: 28px;

            margin-bottom: 18px;

        }


        /* =====================================================
           PLOTLY CHART CONTAINERS
        ===================================================== */

        [data-testid="stPlotlyChart"] {

            background: #ffffff;

            border: 1px solid #e5e7eb;

            border-radius: 18px;

            padding: 8px;

            box-shadow:
                0 6px 18px
                rgba(15, 23, 42, 0.05);

            margin-bottom: 22px;

        }


        /* =====================================================
           DATA TABLE
        ===================================================== */

        [data-testid="stDataFrame"] {

            border-radius: 16px;

            overflow: hidden;

            border: 1px solid #e5e7eb;

        }


        /* =====================================================
           ALERTS
        ===================================================== */

        [data-testid="stAlert"] {

            border-radius: 14px;

        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        [data-testid="stSidebar"] {

            background:
                linear-gradient(
                    180deg,
                    #0f172a,
                    #1e293b
                );

        }


        /* Sidebar normal text */

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {

            color: #ffffff !important;

        }


        /* =====================================================
           SELECTBOX
        ===================================================== */

        [data-testid="stSelectbox"] {

            margin-bottom: 12px;

        }


        [data-testid="stSelectbox"] label {

            color: #ffffff !important;

        }


        [data-testid="stSelectbox"] [data-baseweb="select"] {

            background-color: #ffffff !important;

            border-radius: 8px;

        }


        /* Selected text */

        [data-testid="stSelectbox"]
        [data-baseweb="select"]
        [data-baseweb="value-container"] {

            color: #0f172a !important;

        }


        [data-testid="stSelectbox"]
        [data-baseweb="select"]
        [data-baseweb="single-value"] {

            color: #0f172a !important;

        }


        [data-testid="stSelectbox"]
        [data-baseweb="select"]
        input {

            color: #0f172a !important;

            -webkit-text-fill-color: #0f172a !important;

        }


        /* Dropdown arrow */

        [data-testid="stSelectbox"]
        [data-baseweb="select"]
        svg {

            fill: #0f172a !important;

            color: #0f172a !important;

        }


        /* Dropdown menu */

        [role="listbox"] {

            background-color: #ffffff !important;

        }


        [role="option"] {

            color: #0f172a !important;

            background-color: #ffffff !important;

        }


        [role="option"]:hover {

            background-color: #f1f5f9 !important;

        }


        /* =====================================================
           RESPONSIVE DESIGN
        ===================================================== */

        @media (max-width: 900px) {

            .main .block-container {

                padding-left: 1rem;

                padding-right: 1rem;

            }


            .hero {

                padding: 24px;

            }


            .hero h1 {

                font-size: 28px;

            }


            .metric-card {

                padding: 18px;

            }


            .metric-value {

                font-size: clamp(18px, 5vw, 25px);

            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )