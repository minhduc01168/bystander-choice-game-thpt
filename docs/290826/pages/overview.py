import streamlit as st
import pandas as pd
import plotly.express as px


from ultis.data_loader import load_players
from ultis.style import apply_style

apply_style()

df = load_players()

st.title("📊 Tổng quan")


# =========================
# KPI
# =========================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Người chơi", len(df))

c2.metric("Điểm trung bình", f"{df.score.mean():.1f}")

c3.metric("Thấu cảm", f"{df.empathy.mean():.2f}")

c4.metric("Can thiệp", f"{df.intervention.mean():.2f}")


# =========================
# SCORE DISTRIBUTION
# =========================

fig = px.histogram(df, x="score", nbins=15, title="Phân bố điểm người chơi")

st.plotly_chart(fig, use_container_width=True)


# =========================
# PSYCHOLOGY
# =========================

psychology = pd.DataFrame(
    {
        "Chỉ số": ["Thấu cảm", "Tự tin ứng phó", "Ý định can thiệp"],
        "Điểm": [df.empathy.mean(), df.confidence.mean(), df.intervention.mean()],
    }
)


fig = px.bar(
    psychology, x="Chỉ số", y="Điểm", range_y=[0, 5], title="Điểm tâm lý trung bình"
)

st.plotly_chart(fig, use_container_width=True)
