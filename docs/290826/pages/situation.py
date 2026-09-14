import streamlit as st
import plotly.express as px

from ultis.data_loader import load_scenarios
from ultis.style import apply_style

apply_style()

df = load_scenarios()

st.title("📋 Phân tích từng tình huống")


summary = df.groupby(["scenario", "action"]).size().reset_index(name="count")


fig = px.bar(
    summary,
    x="scenario",
    y="count",
    color="action",
    barmode="stack",
    title="Lựa chọn theo tình huống",
)

fig.update_xaxes(tickangle=-20)


st.plotly_chart(fig, use_container_width=True)


# =========================
# TABLE
# =========================

pivot = summary.pivot(index="scenario", columns="action", values="count").fillna(0)


st.subheader("📊 Bảng phân tích")

st.dataframe(pivot, use_container_width=True)
