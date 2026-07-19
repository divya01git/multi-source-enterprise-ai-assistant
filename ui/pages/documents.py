"""
Enterprise AI Assistant
Documents
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from rag.vector_store import vector_store


# ============================================================
# CONFIG
# ============================================================

UPLOAD_FOLDER = Path(
    "documents/uploaded"
)

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .header{
        background:linear-gradient(90deg,#0F172A,#1E3A8A);
        color:white;
        padding:22px;
        border-radius:18px;
        margin-bottom:25px;
    }

    .card{
        background:white;
        border-radius:16px;
        padding:18px;
        border:1px solid #E5E7EB;
        box-shadow:0 2px 8px rgba(0,0,0,.05);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="header">

    <h2>📄 Document Intelligence</h2>

    <p>
    Upload enterprise documents and automatically index them
    into the AI Knowledge Base.
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# UPLOAD
# ============================================================

st.subheader(
    "Upload PDF"
)


uploaded = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"],
)


if uploaded is not None:

    save_path = UPLOAD_FOLDER / uploaded.name

    with open(
        save_path,
        "wb",
    ) as file:

        file.write(
            uploaded.getbuffer()
        )

    with st.spinner(
        "Indexing document..."
    ):

        try:

            vector_store.build_from_file(
                save_path
            )

            st.success(
                "✅ Document uploaded and indexed successfully!"
            )

        except Exception as error:

            st.error(
                f"Indexing failed:\n\n{error}"
            )


# ============================================================
# EXISTING DOCUMENTS
# ============================================================

st.divider()


st.subheader(
    "Indexed Documents"
)


files = sorted(
    UPLOAD_FOLDER.glob("*")
)


if files:

    documents = pd.DataFrame(
        {
            "Document": [
                file.name
                for file in files
            ],

            "Status": [
                "Indexed"
                for _ in files
            ],
        }
    )

    st.dataframe(
        documents,
        hide_index=True,
        width="stretch",
    )

else:

    st.info(
        "No uploaded documents found."
    )


# ============================================================
# SEARCH PREVIEW
# ============================================================

st.divider()


query = st.text_input(
    "Search Preview"
)


if query:

    try:

        db = vector_store.get()

        docs = db.similarity_search(
            query,
            k=3,
        )

        if docs:

            st.success(
                f"Found {len(docs)} matching chunks"
            )

            for index, doc in enumerate(
                docs,
                1,
            ):

                st.markdown(
                    f"### Result {index}"
                )

                st.write(
                    doc.page_content[:500]
                )

                st.divider()

        else:

            st.warning(
                "No matching content found."
            )

    except Exception as error:

        st.error(
            error
        )