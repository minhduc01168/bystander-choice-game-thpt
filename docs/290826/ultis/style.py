import streamlit as st


def apply_style():

    st.markdown(
        """
        <style>

        .main {
            background-color: #f7f8fc;
        }

        .block-container {
            padding-top: 2rem;
        }

        h1 {
            font-weight: 800;
        }

        div[data-testid="stMetric"] {

            background: white;

            border: 1px solid #e5e7eb;

            padding: 18px;

            border-radius: 15px;

            box-shadow:
                0 2px 8px
                rgba(0,0,0,0.05);
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
