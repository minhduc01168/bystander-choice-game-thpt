import streamlit as st


def custom_player_timeline_style():
    st.markdown(
        """
    <style>
    .bc-timeline { position: relative; padding-left: 30px; margin: 6px 0 18px 4px; }
    .bc-timeline::before {
        content: ""; position: absolute; left: 9px; top: 4px; bottom: 4px;
        width: 2px; background: rgba(128,128,128,0.35);
    }
    .bc-step { position: relative; margin-bottom: 14px; }
    .bc-dot {
        position: absolute; left: -30px; top: 2px; width: 22px; height: 22px;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 11px; color: #fff; box-shadow: 0 0 0 3px var(--background-color, #fff);
    }
    .bc-card {
        background: var(--secondary-background-color, rgba(128,128,128,0.08));
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 10px; padding: 10px 14px;
    }
    .bc-meta { font-size: 12px; opacity: 0.65; margin-bottom: 3px; }
    .bc-text { font-size: 14.5px; }
    .bc-code {
        display: inline-block; font-weight: 700; font-size: 11px;
        padding: 1px 7px; border-radius: 999px; margin-right: 6px; color: #fff;
    }
    .bc-chip {
        display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 999px;
        margin-right: 6px; margin-top: 7px; background: rgba(128,128,128,0.15);
    }
    .bc-playthrough-title {
        font-weight: 700; margin: 4px 0 10px 0; font-size: 12.5px; opacity: 0.6;
        text-transform: uppercase; letter-spacing: 0.04em;
    }
    .bc-final {
        margin: 6px 0 22px 0; padding: 12px 16px; border-radius: 10px;
        font-weight: 700; text-align: center; background: rgba(128,128,128,0.12);
    }
    .bc-legend-item { display:inline-flex; align-items:center; margin-right:16px; font-size:12.5px; opacity:0.8; }
    .bc-legend-dot { width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:6px; }
    </style>
    """,
        unsafe_allow_html=True,
    )


def custom_tab_style():

    st.markdown(
        """
    <style>
    /* Khoảng cách giữa các tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    /* Tab mặc định */
    .stTabs [data-baseweb="tab"] {
        background-color: #E8F3FF;
        color: #3B6E9E;

        border-radius: 12px;
        padding: 8px 18px;
        

        font-weight: 500;
        border: 1px solid #D4E9FA;

        transition: all 0.2s ease;
    }

    /* Hover */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #D9EDFF;
        color: #2563EB;
        transform: translateY(-1px);
    }

    # /* Tab đang active */
    # .stTabs [aria-selected="true"] {
    #     background-color: #BFE0FF;
    #     color: #1D5FA7;

    #     border: 1px solid #A8D3F5;
    #     box-shadow: 0 2px 6px rgba(37, 99, 235, 0.12);
    #     border-radius: 10px;
    # }

    /* Bỏ thanh xanh mặc định bên dưới */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent;
    }

    /* Bỏ border/divider mặc định */
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def custom_metrics_style():
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
