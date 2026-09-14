import streamlit as st
import plotly.express as px


from ultis.data_loader import load_players
from ultis.style import apply_style

apply_style()

df = load_players()

st.title("🧠 Phân tích tâm lý")


col1, col2 = st.columns(2)


with col1:

    fig = px.scatter(
        df,
        x="empathy",
        y="intervention",
        trendline="ols",
        title="Thấu cảm → Ý định can thiệp",
        labels={"empathy": "Thấu cảm", "intervention": "Ý định can thiệp"},
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:

    fig = px.scatter(
        df,
        x="confidence",
        y="intervention",
        trendline="ols",
        title="Tự tin → Ý định can thiệp",
        labels={"confidence": "Tự tin ứng phó", "intervention": "Ý định can thiệp"},
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================
# CORRELATION
# =========================

corr = df[["empathy", "confidence", "intervention", "score"]].corr()


fig = px.imshow(corr, text_auto=True, aspect="auto", title="Ma trận tương quan")

st.plotly_chart(fig, use_container_width=True)
