import streamlit as st

from ultis.data_loader import load_players
from ultis.style import apply_style

st.set_page_config(page_title="Player Analytics", page_icon="🎮", layout="wide")

apply_style()

df = load_players()


# =========================
# SIDEBAR
# =========================

st.sidebar.title("🎮 Player Analytics")

st.sidebar.caption("Phân tích dữ liệu game Visual Novel")

st.sidebar.markdown("---")

st.sidebar.subheader("🔎 Bộ lọc")


ages = st.sidebar.multiselect(
    "Độ tuổi", sorted(df["age"].unique()), default=sorted(df["age"].unique())
)


genders = st.sidebar.multiselect(
    "Giới tính", sorted(df["gender"].unique()), default=sorted(df["gender"].unique())
)


score_range = st.sidebar.slider("Khoảng điểm", 0, 100, (0, 100))


# =========================
# FILTER
# =========================

filtered_df = df[
    df["age"].isin(ages)
    & df["gender"].isin(genders)
    & df["score"].between(score_range[0], score_range[1])
]


# =========================
# HEADER
# =========================

st.title("🎮 Player Analytics Dashboard")

st.caption("Dashboard phân tích dữ liệu người chơi từ Visual Novel")


# =========================
# KPI
# =========================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric("👥 Người chơi", len(filtered_df))


with col2:

    st.metric("⭐ Điểm trung bình", f"{filtered_df['score'].mean():.1f}")


with col3:

    st.metric("🧠 Thấu cảm", f"{filtered_df['empathy'].mean():.2f}/5")


with col4:

    st.metric("🎯 Can thiệp", f"{filtered_df['intervention'].mean():.2f}/5")


st.markdown("---")


st.subheader("📌 Dữ liệu người chơi")

st.dataframe(filtered_df, use_container_width=True, hide_index=True)
