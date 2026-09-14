"""
app.py
-----------------------------------------------------------------------
Bystander Choice - Psychological Analysis Dashboard (Streamlit).

Reads choice_data.csv and player_summary.csv produced by the Ren'Py
game and renders KPI cards, five charts, filters, a per-player detail
view (with a proper visual timeline instead of a plain text line), and
a plain-language "Research Insights" section.

The dashboard is split into tabs so the viewer can open only the
section they care about instead of scrolling through everything at
once.

Run with:
    cd dashboard
    pip install -r requirements.txt
    streamlit run app.py
-----------------------------------------------------------------------
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data.data_loader import load_choice_data, load_player_summary, data_files_exist
import analysis as analysis

from helpers.custom_style import (
    custom_metrics_style,
    custom_tab_style,
    custom_player_timeline_style,
)

st.set_page_config(
    page_title="Bystander Choice Dashboard",
    page_icon="🧭",
    layout="wide",
)

custom_player_timeline_style()

# ------------------------------------------------------------------ #
# HEADER
# ------------------------------------------------------------------ #
st.title(
    "BYSTANDER CHOICE\n\nMột trò chơi mô phỏng dành cho học sinh THPT về vai trò của người chứng kiến trong bắt nạt học đường.",
    text_alignment="center",
)
st.caption("Psychological Analysis Dashboard")
st.info(
    "Nguyên mẫu nghiên cứu mô tả hành vi lựa chọn trong tình huống bắt nạt học đường mô phỏng. "
    "Kết quả mang tính khám phá (exploratory), không phải công cụ chẩn đoán tâm lý.",
    icon="ℹ️",
)
st.divider()

# ------------------------------------------------------------------ #
# LOAD DATA
# ------------------------------------------------------------------ #
choice_df = load_choice_data()
summary_df = load_player_summary()

if not data_files_exist():
    st.info(
        "Chưa có dữ liệu người chơi nào. Hãy chạy game Ren'Py trước, hoặc tạo dữ liệu mẫu bằng "
        "`python sample_data_generator.py` trong thư mục `dashboard/` để thử dashboard."
    )

# ------------------------------------------------------------------ #
# SIDEBAR FILTERS --> applies to Overview & Charts tabs
# ------------------------------------------------------------------ #
st.sidebar.header("Filter")

type_options = ["All", "Active", "Supportive", "Passive", "Avoidant"]
type_label_to_value = {
    "All": None,
    "Active": "ACTIVE BYSTANDER",
    "Supportive": "SUPPORTIVE BYSTANDER",
    "Passive": "PASSIVE BYSTANDER",
    "Avoidant": "AVOIDANT BYSTANDER",
}
selected_type_label = st.sidebar.selectbox("Bystander Type", type_options, index=0)
selected_type = type_label_to_value[selected_type_label]

scenario_options = ["All", "scenario_1", "scenario_2"]
selected_scenario = st.sidebar.selectbox("Scenario", scenario_options, index=0)

player_options = (
    ["All"] + sorted(summary_df["player_id"].unique().tolist())
    if not summary_df.empty
    else ["All"]
)
selected_player_filter = st.sidebar.selectbox("Player ID", player_options, index=0)

st.sidebar.caption(
    "Bộ lọc này áp dụng cho tab **Tổng quan** và **Biểu đồ**. "
    "Tab **Chi tiết người chơi** có ô chọn player riêng."
)

# Apply filters
filtered_summary = summary_df.copy()
if selected_type is not None and not filtered_summary.empty:
    filtered_summary = filtered_summary[
        filtered_summary["bystander_type"] == selected_type
    ]
if selected_player_filter != "All" and not filtered_summary.empty:
    filtered_summary = filtered_summary[
        filtered_summary["player_id"] == selected_player_filter
    ]

filtered_choices = choice_df.copy()
if selected_scenario != "All" and not filtered_choices.empty:
    filtered_choices = filtered_choices[
        filtered_choices["scenario"] == selected_scenario
    ]
if selected_player_filter != "All" and not filtered_choices.empty:
    filtered_choices = filtered_choices[
        filtered_choices["player_id"] == selected_player_filter
    ]
if selected_type is not None and not filtered_choices.empty and not summary_df.empty:
    matching_ids = summary_df[summary_df["bystander_type"] == selected_type][
        "player_id"
    ]
    filtered_choices = filtered_choices[
        filtered_choices["player_id"].isin(matching_ids)
    ]

# ------------------------------------------------------------------ #
# TABS -- lets the viewer open only the section they want instead of
# scrolling through KPIs + 5 charts + player detail + insights at once.
# ------------------------------------------------------------------ #

custom_tab_style()

tab_overview, tab_charts, tab_player, tab_insights = st.tabs(
    [
        "📌 Tổng quan",
        "📊 Biểu đồ",
        "🧑‍🎓 Chi tiết người chơi",
        "🔍 Nhận định nghiên cứu",
    ]
)

# ==================================================================== #
# TAB 1 -- OVERVIEW (KPI cards)
# ==================================================================== #
with tab_overview:
    kpis = analysis.compute_kpis(filtered_summary)

    kpi_cols = st.columns(5)

    custom_metrics_style()

    kpi_cols[0].metric("Total Players", kpis["total_players"])
    kpi_cols[1].metric("Active Bystanders", kpis["ACTIVE BYSTANDER"])
    kpi_cols[2].metric("Supportive Bystanders", kpis["SUPPORTIVE BYSTANDER"])
    kpi_cols[3].metric("Passive Bystanders", kpis["PASSIVE BYSTANDER"])
    kpi_cols[4].metric("Avoidant Bystanders", kpis["AVOIDANT BYSTANDER"])

    st.caption(
        "Số liệu phản ánh bộ lọc hiện tại ở sidebar (Bystander Type / Player ID)."
    )

    if not filtered_summary.empty:
        st.divider()
        st.markdown("**Tóm tắt nhanh**")
        dist_df = analysis.bystander_type_distribution(filtered_summary)
        st.dataframe(dist_df, hide_index=True, use_container_width=True)

# ==================================================================== #
# TAB 2 -- CHARTS, each chart in its own sub-tab so
# the viewer picks which one to look at instead of seeing all 5 at once.
# ==================================================================== #
with tab_charts:
    chart_tabs = st.tabs(
        [
            "🥯 Phân bố nhóm",
            "📶 Điểm trung bình",
            "🕸️ Radar theo nhóm",
            "⚖️ Scenario 1 vs 2",
            "🎯 Loại hành vi lựa chọn",
        ]
    )

    with chart_tabs[0]:
        st.subheader("Bystander Type Distribution")
        dist_df = analysis.bystander_type_distribution(filtered_summary)
        if dist_df.empty or dist_df["count"].sum() == 0:
            st.caption("Chưa có dữ liệu để hiển thị.")
        else:
            fig = px.pie(dist_df, names="bystander_type", values="count", hole=0.45)
            st.plotly_chart(fig, use_container_width=True)

    with chart_tabs[1]:
        st.subheader("Average Trait Scores")
        avg_df = analysis.average_traits(filtered_summary)
        fig = px.bar(avg_df, x="trait", y="average", color="trait")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with chart_tabs[2]:
        st.subheader("Trait Profile by Bystander Type (Radar)")
        st.caption(
            "Biểu đồ này luôn dùng toàn bộ dữ liệu (không áp dụng bộ lọc) để so sánh công bằng giữa 4 nhóm."
        )
        radar_df = analysis.radar_data_by_type(summary_df)
        if radar_df.empty or radar_df["value"].sum() == 0:
            st.caption("Chưa có dữ liệu để hiển thị.")
        else:
            fig = go.Figure()
            for t in analysis.BYSTANDER_TYPES:
                sub = radar_df[radar_df["bystander_type"] == t]
                fig.add_trace(
                    go.Scatterpolar(
                        r=sub["value"], theta=sub["trait"], fill="toself", name=t
                    )
                )
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)), showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

    with chart_tabs[3]:
        st.subheader("Scenario 1 vs Scenario 2 (Average Score)")
        scen_df = analysis.scenario_comparison(filtered_summary)
        fig = px.bar(scen_df, x="scenario", y="average_score", color="scenario")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with chart_tabs[4]:
        st.subheader("Choice Category Distribution")
        cat_df = analysis.choice_category_distribution(filtered_choices)
        if cat_df["percentage"].sum() == 0:
            st.caption("Chưa có dữ liệu để hiển thị.")
        else:
            fig = px.bar(
                cat_df, x="category", y="percentage", color="category", text_auto=".1f"
            )
            fig.update_layout(showlegend=False, yaxis_title="Percentage (%)")
            st.plotly_chart(fig, use_container_width=True)

# ==================================================================== #
# TAB 3 -- PLAYER DETAIL, with a proper visual
# timeline instead of a single line of plain text.
# ==================================================================== #
with tab_player:
    if summary_df.empty:
        st.caption("Chưa có người chơi nào trong dữ liệu.")
    else:
        detail_player = st.selectbox(
            "Chọn một player để xem chi tiết",
            sorted(summary_df["player_id"].unique().tolist()),
            key="player_detail_select",
        )
        player_row = summary_df[summary_df["player_id"] == detail_player].iloc[-1]

        detail_cols = st.columns([1, 2])
        with detail_cols[0]:
            st.markdown("**Player:** {}".format(detail_player))
            st.markdown("- Empathy: {}".format(int(player_row["total_empathy"])))
            st.markdown("- Courage: {}".format(int(player_row["total_courage"])))
            st.markdown(
                "- Responsibility: {}".format(int(player_row["total_responsibility"]))
            )
            st.markdown(
                "- Intervention: {}".format(int(player_row["total_intervention"]))
            )
            st.markdown("**Type:** {}".format(player_row["bystander_type"]))

        with detail_cols[1]:
            st.markdown("**Timeline**")

            # Legend for the category colors used in the dots/badges below.
            legend_html = "".join(
                '<span class="bc-legend-item"><span class="bc-legend-dot" '
                'style="background:{color}"></span>{label}</span>'.format(
                    color=style["color"], label=style["label_vi"]
                )
                for style in analysis.CATEGORY_STYLE.values()
            )
            st.markdown(legend_html, unsafe_allow_html=True)

            playthroughs = analysis.build_player_timeline_steps(
                choice_df, detail_player
            )

            if not playthroughs:
                st.caption("Không có bản ghi lựa chọn chi tiết cho player này.")
            else:
                for p_idx, steps in enumerate(playthroughs, start=1):
                    html_parts = []
                    if len(playthroughs) > 1:
                        html_parts.append(
                            '<div class="bc-playthrough-title">Lượt chơi {}</div>'.format(
                                p_idx
                            )
                        )
                    html_parts.append('<div class="bc-timeline">')

                    for step in steps:
                        chips = (
                            "".join(
                                '<span class="bc-chip">{icon} {trait} {sign}{val}</span>'.format(
                                    icon=icon,
                                    trait=trait,
                                    sign="+" if val > 0 else "",
                                    val=val,
                                )
                                for trait, icon, val in step["deltas"]
                            )
                            or '<span class="bc-chip">Không thay đổi điểm</span>'
                        )

                        html_parts.append("<div>")

                        html_parts.append(
                            """
                            <div class="bc-step">
                                <div class="bc-dot" style="background:{color}">{icon}</div>
                                <div class="bc-card">
                                    <div class="bc-meta">{scenario_label} · {question_label}</div>
                                    <div class="bc-text">
                                        <span class="bc-code" style="background:{color}">{code}</span>
                                        {text}
                                    </div>
                                    <div>{chips}</div>
                                </div>
                            </div>
                            """.format(
                                color=step["color"],
                                icon=step["icon"],
                                scenario_label=step["scenario_label"],
                                question_label=step["question_label"],
                                code=step["code"],
                                text=step["text"],
                                chips=chips,
                            )
                        )

                    html_parts.append("</div>")

                    if p_idx == len(playthroughs):
                        html_parts.append(
                            '<div class="bc-final">Final Result: {}</div>'.format(
                                player_row["bystander_type"]
                            )
                        )

                    st.markdown("".join(html_parts), unsafe_allow_html=True)

# ==================================================================== #
# TAB 4 -- RESEARCH INSIGHTS
# ==================================================================== #
with tab_insights:
    st.subheader("Research Insights")
    st.caption(
        "Các nhận xét dưới đây chỉ mang tính mô tả / khám phá / quan sát dựa trên dữ liệu hiện có, "
        "không phải kết luận chẩn đoán tâm lý hay bệnh lý."
    )
    for insight in analysis.generate_research_insights(
        filtered_summary, filtered_choices
    ):
        st.markdown("- " + insight)
