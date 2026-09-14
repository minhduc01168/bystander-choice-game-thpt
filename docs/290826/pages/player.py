import streamlit as st
import plotly.graph_objects as go

from ultis.data_loader import load_players
from ultis.style import apply_style

apply_style()

df = load_players()

st.title("👤 Phân tích từng người chơi")


player_id = st.selectbox("Chọn người chơi", df["player_id"].tolist())


player = df[df["player_id"] == player_id].iloc[0]


# =========================
# KPI
# =========================

c1, c2, c3, c4 = st.columns(4)


c1.metric("⭐ Điểm", f"{player.score:.1f}/100")

c2.metric("🧠 Thấu cảm", f"{player.empathy:.2f}/5")

c3.metric("💪 Tự tin", f"{player.confidence:.2f}/5")

c4.metric("🎯 Can thiệp", f"{player.intervention:.2f}/5")


# =========================
# RADAR
# =========================

fig = go.Figure()


fig.add_trace(
    go.Scatterpolar(
        r=[player.empathy, player.confidence, player.intervention],
        theta=["Thấu cảm", "Tự tin ứng phó", "Ý định can thiệp"],
        fill="toself",
        name=player_id,
    )
)


fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    title=f"Hồ sơ tâm lý - {player_id}",
)


st.plotly_chart(fig, use_container_width=True)


# =========================
# INFORMATION
# =========================

st.markdown("### 👤 Thông tin")

col1, col2, col3 = st.columns(3)

col1.write(f"**Tuổi:** {player.age}")

col2.write(f"**Giới tính:** {player.gender}")

col3.write(f"**Thời gian chơi:** " f"{player.play_time_minutes} phút")


st.markdown("### 🎯 Hành vi")

col1, col2 = st.columns(2)

col1.metric("Số lần can thiệp", player.intervention_count)

col2.metric("Số lần thụ động", player.passive_count)
