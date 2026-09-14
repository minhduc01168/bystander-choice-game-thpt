import streamlit as st
import plotly.express as px

from ultis.data_loader import load_scenarios
from ultis.style import apply_style

apply_style()

df = load_scenarios()

st.title("🎯 Phân tích hành vi")


counts = df["action"].value_counts().reset_index()

counts.columns = ["action", "count"]


fig = px.bar(
    counts, x="action", y="count", title="Các lựa chọn của người chơi", text="count"
)

st.plotly_chart(fig, use_container_width=True)


# =========================
# RATE
# =========================

rates = df["action"].value_counts(normalize=True).mul(100).round(1).reset_index()

rates.columns = ["action", "percentage"]


st.subheader("📈 Tỷ lệ lựa chọn")

st.dataframe(rates, use_container_width=True, hide_index=True)
