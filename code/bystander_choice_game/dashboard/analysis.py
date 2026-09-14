"""
analysis.py
-----------------------------------------------------------------------
Pure analysis helpers used by app.py. Kept separate from app.py so the
Streamlit layout code stays readable and the analysis logic is testable
on its own.

IMPORTANT (spec sections 21-22): every text-generating function here
uses descriptive / exploratory / observational language only. Nothing
in this module frames results as a diagnosis of a psychological
condition -- it only ever describes patterns in the recorded in-game
choices.
-----------------------------------------------------------------------
"""

import pandas as pd

BYSTANDER_TYPES = [
    "ACTIVE BYSTANDER",
    "SUPPORTIVE BYSTANDER",
    "PASSIVE BYSTANDER",
    "AVOIDANT BYSTANDER",
]

TRAIT_COLUMNS = {
    "Empathy": "total_empathy",
    "Courage": "total_courage",
    "Responsibility": "total_responsibility",
    "Intervention": "total_intervention",
}

CATEGORY_STYLE = {
    "Direct Intervention": {"color": "#e0654f", "icon": "⚡", "label_vi": "Can thiệp trực tiếp"},
    "Seek Help": {"color": "#4f8fe0", "icon": "🧑‍🏫", "label_vi": "Tìm kiếm hỗ trợ"},
    "Support Victim": {"color": "#a76fe0", "icon": "🤝", "label_vi": "Hỗ trợ nạn nhân"},
    "Do Nothing": {"color": "#8a8f98", "icon": "…", "label_vi": "Không hành động"},
}

SCENARIO_LABELS = {
    "scenario_1": "Scenario 1 · Bắt nạt trực tiếp",
    "scenario_2": "Scenario 2 · Bắt nạt qua mạng",
}

QUESTION_LABELS = {
    "Q1": "Quyết định đầu tiên",
    "Q2": "Quyết định tiếp theo",
}

TRAIT_ICON = {
    "empathy_change": ("Empathy", "💙"),
    "courage_change": ("Courage", "🦁"),
    "responsibility_change": ("Responsibility", "🧭"),
    "intervention_change": ("Intervention", "🙋"),
}

# ---------------------------------------------------------------------
# Human-readable (accented) Vietnamese caption for every decision point,
# for display purposes only. choice_text in the CSV itself is kept
# ASCII-safe by the game for encoding robustness (spec section 24), so
# this lookup restores the original wording purely for the dashboard UI.
# Falls back to the raw choice_text from the CSV if a key is missing
# (e.g. a scenario added later that hasn't been added here yet).
# ---------------------------------------------------------------------
DISPLAY_TEXT_MAP = {
    ("scenario_1", "Q1", "-", "A"): "Đi tới và yêu cầu nhóm học sinh dừng lại.",
    ("scenario_1", "Q1", "-", "B"): "Đi tìm giáo viên hoặc nhân viên nhà trường.",
    ("scenario_1", "Q1", "-", "C"): "Đứng lại quan sát nhưng chưa làm gì.",
    ("scenario_1", "Q1", "-", "D"): "Bỏ đi vì nghĩ đó không phải chuyện của mình.",
    ("scenario_1", "Q2", "A", "A1"): "Bình tĩnh giải thích rằng hành động này không đúng.",
    ("scenario_1", "Q2", "A", "A2"): "Gọi thêm một người bạn tới hỗ trợ.",
    ("scenario_1", "Q2", "A", "A3"): "Tìm giáo viên và báo sự việc.",
    ("scenario_1", "Q2", "A", "A4"): "Sợ hãi và rút lui.",
    ("scenario_1", "Q2", "B", "B1"): "Khẳng định mình trực tiếp chứng kiến.",
    ("scenario_1", "Q2", "B", "B2"): "Đề nghị giáo viên đi kiểm tra.",
    ("scenario_1", "Q2", "B", "B3"): "Nói rằng có thể chỉ là đùa.",
    ("scenario_1", "Q2", "B", "B4"): "Nói rằng Minh nên tự giải quyết.",
    ("scenario_1", "Q2", "C", "C1"): "Tiến tới hỗ trợ Minh.",
    ("scenario_1", "Q2", "C", "C2"): "Nhắn tin hỏi Minh có ổn không.",
    ("scenario_1", "Q2", "C", "C3"): "Chờ nhóm học sinh rời đi rồi hỗ trợ Minh.",
    ("scenario_1", "Q2", "C", "C4"): "Tiếp tục đứng ngoài.",
    ("scenario_1", "Q2", "D", "D1"): "Báo giáo viên.",
    ("scenario_1", "Q2", "D", "D2"): "Nhắn riêng cho Minh.",
    ("scenario_1", "Q2", "D", "D3"): "Không bình luận nhưng tiếp tục theo dõi.",
    ("scenario_1", "Q2", "D", "D4"): "Tham gia bình luận chế giễu.",
    ("scenario_2", "Q1", "-", "A"): "Bảo mọi người dừng lại.",
    ("scenario_2", "Q1", "-", "B"): "Nhắn riêng cho Lan.",
    ("scenario_2", "Q1", "-", "C"): "Báo cáo bài đăng.",
    ("scenario_2", "Q1", "-", "D"): "Không làm gì.",
    ("scenario_2", "Q2", "A", "A1"): "Giải thích vì sao hành động này có thể làm Lan tổn thương.",
    ("scenario_2", "Q2", "A", "A2"): "Nói rằng sẽ báo giáo viên nếu tiếp tục.",
    ("scenario_2", "Q2", "A", "A3"): "Thoát group.",
    ("scenario_2", "Q2", "A", "A4"): "Im lặng.",
    ("scenario_2", "Q2", "B", "B1"): "Nói rằng bạn sẽ ở bên và cùng tìm cách giải quyết.",
    ("scenario_2", "Q2", "B", "B2"): "Khuyên Lan lưu bằng chứng và báo người lớn.",
    ("scenario_2", "Q2", "B", "B3"): "Nói \"Bạn đừng để ý họ.\"",
    ("scenario_2", "Q2", "B", "B4"): "Không trả lời.",
    ("scenario_2", "Q2", "C", "C1"): "Giữ quyết định báo cáo.",
    ("scenario_2", "Q2", "C", "C2"): "Giải thích lý do báo cáo.",
    ("scenario_2", "Q2", "C", "C3"): "Không trả lời.",
    ("scenario_2", "Q2", "C", "C4"): "Hủy báo cáo.",
    ("scenario_2", "Q2", "D", "D1"): "Nói với giáo viên những gì mình biết.",
    ("scenario_2", "Q2", "D", "D2"): "Nói chuyện riêng với giáo viên.",
    ("scenario_2", "Q2", "D", "D3"): "Im lặng.",
    ("scenario_2", "Q2", "D", "D4"): "Nói \"Em không biết gì cả.\"",
}

# ---------------------------------------------------------------------
# Choice -> broad behavioral category, for Chart 5 (spec section 18).
# Keyed by (scenario, question_id, branch, choice). Built manually from
# the scenario script so every one of the 40 possible decision points
# maps to exactly one of the four categories requested in the spec.
# ---------------------------------------------------------------------
CHOICE_CATEGORY_MAP = {
    # --- Scenario 1, first decision ---
    ("scenario_1", "Q1", "-", "A"): "Direct Intervention",
    ("scenario_1", "Q1", "-", "B"): "Seek Help",
    ("scenario_1", "Q1", "-", "C"): "Do Nothing",
    ("scenario_1", "Q1", "-", "D"): "Do Nothing",
    # --- Scenario 1, branch A ---
    ("scenario_1", "Q2", "A", "A1"): "Direct Intervention",
    ("scenario_1", "Q2", "A", "A2"): "Seek Help",
    ("scenario_1", "Q2", "A", "A3"): "Seek Help",
    ("scenario_1", "Q2", "A", "A4"): "Do Nothing",
    # --- Scenario 1, branch B ---
    ("scenario_1", "Q2", "B", "B1"): "Seek Help",
    ("scenario_1", "Q2", "B", "B2"): "Seek Help",
    ("scenario_1", "Q2", "B", "B3"): "Do Nothing",
    ("scenario_1", "Q2", "B", "B4"): "Do Nothing",
    # --- Scenario 1, branch C ---
    ("scenario_1", "Q2", "C", "C1"): "Support Victim",
    ("scenario_1", "Q2", "C", "C2"): "Support Victim",
    ("scenario_1", "Q2", "C", "C3"): "Support Victim",
    ("scenario_1", "Q2", "C", "C4"): "Do Nothing",
    # --- Scenario 1, branch D ---
    ("scenario_1", "Q2", "D", "D1"): "Seek Help",
    ("scenario_1", "Q2", "D", "D2"): "Support Victim",
    ("scenario_1", "Q2", "D", "D3"): "Do Nothing",
    ("scenario_1", "Q2", "D", "D4"): "Do Nothing",
    # --- Scenario 2, first decision ---
    ("scenario_2", "Q1", "-", "A"): "Direct Intervention",
    ("scenario_2", "Q1", "-", "B"): "Support Victim",
    ("scenario_2", "Q1", "-", "C"): "Seek Help",
    ("scenario_2", "Q1", "-", "D"): "Do Nothing",
    # --- Scenario 2, branch A ---
    ("scenario_2", "Q2", "A", "A1"): "Direct Intervention",
    ("scenario_2", "Q2", "A", "A2"): "Seek Help",
    ("scenario_2", "Q2", "A", "A3"): "Do Nothing",
    ("scenario_2", "Q2", "A", "A4"): "Do Nothing",
    # --- Scenario 2, branch B ---
    ("scenario_2", "Q2", "B", "B1"): "Support Victim",
    ("scenario_2", "Q2", "B", "B2"): "Seek Help",
    ("scenario_2", "Q2", "B", "B3"): "Support Victim",
    ("scenario_2", "Q2", "B", "B4"): "Do Nothing",
    # --- Scenario 2, branch C ---
    ("scenario_2", "Q2", "C", "C1"): "Seek Help",
    ("scenario_2", "Q2", "C", "C2"): "Seek Help",
    ("scenario_2", "Q2", "C", "C3"): "Do Nothing",
    ("scenario_2", "Q2", "C", "C4"): "Do Nothing",
    # --- Scenario 2, branch D ---
    ("scenario_2", "Q2", "D", "D1"): "Seek Help",
    ("scenario_2", "Q2", "D", "D2"): "Seek Help",
    ("scenario_2", "Q2", "D", "D3"): "Do Nothing",
    ("scenario_2", "Q2", "D", "D4"): "Do Nothing",
}


def compute_kpis(summary_df: pd.DataFrame) -> dict:
    """Total players + a count per bystander type, defaulting to 0."""
    kpis = {"total_players": int(len(summary_df))}
    counts = summary_df["bystander_type"].value_counts() if not summary_df.empty else pd.Series(dtype=int)
    for t in BYSTANDER_TYPES:
        kpis[t] = int(counts.get(t, 0))
    return kpis


def bystander_type_distribution(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Rows: bystander_type, count -- for the pie/donut chart."""
    if summary_df.empty:
        return pd.DataFrame(columns=["bystander_type", "count"])
    counts = summary_df["bystander_type"].value_counts().reset_index()
    counts.columns = ["bystander_type", "count"]
    return counts


def average_traits(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Rows: trait, average -- for the bar chart of average trait scores."""
    if summary_df.empty:
        return pd.DataFrame({"trait": list(TRAIT_COLUMNS.keys()), "average": [0] * len(TRAIT_COLUMNS)})
    data = {trait: summary_df[col].mean() for trait, col in TRAIT_COLUMNS.items()}
    return pd.DataFrame({"trait": list(data.keys()), "average": list(data.values())})


def radar_data_by_type(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Rows: bystander_type x trait x value -- long format, ready for px.line_polar."""
    rows = []
    for t in BYSTANDER_TYPES:
        subset = summary_df[summary_df["bystander_type"] == t] if not summary_df.empty else summary_df
        for trait, col in TRAIT_COLUMNS.items():
            value = subset[col].mean() if not subset.empty else 0
            rows.append({"bystander_type": t, "trait": trait, "value": 0 if pd.isna(value) else value})
    return pd.DataFrame(rows)


def scenario_comparison(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Average scenario_1_score vs scenario_2_score."""
    if summary_df.empty:
        return pd.DataFrame({"scenario": ["Scenario 1", "Scenario 2"], "average_score": [0, 0]})
    return pd.DataFrame({
        "scenario": ["Scenario 1", "Scenario 2"],
        "average_score": [
            summary_df["scenario_1_score"].mean(),
            summary_df["scenario_2_score"].mean(),
        ],
    })


def _choice_key(row):
    return (row.get("scenario"), row.get("question_id"), row.get("branch"), row.get("choice"))


def choice_category_distribution(choice_df: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage breakdown of every logged decision into the four broad
    behavioral categories from spec section 18.
    """
    categories = ["Direct Intervention", "Seek Help", "Support Victim", "Do Nothing"]
    if choice_df.empty:
        return pd.DataFrame({"category": categories, "percentage": [0] * 4})

    mapped = choice_df.apply(lambda row: CHOICE_CATEGORY_MAP.get(_choice_key(row), "Do Nothing"), axis=1)
    counts = mapped.value_counts(normalize=True) * 100.0
    return pd.DataFrame({
        "category": categories,
        "percentage": [counts.get(c, 0.0) for c in categories],
    })


def generate_research_insights(summary_df: pd.DataFrame, choice_df: pd.DataFrame) -> list:
    """
    Produce a short list of simple, descriptive / exploratory /
    observational sentences about patterns in the current dataset.
    Never claims a diagnosis or a scientifically validated conclusion
    (spec sections 21-22) -- every sentence is phrased as an observed
    tendency within this simulated dataset only.
    """
    insights = []

    if summary_df.empty:
        return ["Chưa có đủ dữ liệu để tạo nhận xét. Hãy chờ thêm người chơi hoàn thành game."]

    avg_empathy = summary_df["total_empathy"].mean()
    avg_courage = summary_df["total_courage"].mean()
    avg_responsibility = summary_df["total_responsibility"].mean()
    avg_intervention = summary_df["total_intervention"].mean()

    if avg_empathy > avg_courage + 2:
        insights.append(
            "Phần lớn người chơi có xu hướng đồng cảm cao hơn so với mức độ "
            "dũng cảm khi can thiệp trực tiếp, dựa trên dữ liệu mô phỏng hiện tại."
        )

    if avg_responsibility > avg_intervention + 2:
        insights.append(
            "Người chơi có xu hướng cảm nhận trách nhiệm cao hơn mức độ hành "
            "động can thiệp thực tế được ghi nhận trong game."
        )

    type_counts = summary_df["bystander_type"].value_counts(normalize=True) * 100
    if not type_counts.empty:
        top_type = type_counts.idxmax()
        insights.append(
            "Nhóm '{}' chiếm tỷ lệ cao nhất trong tập dữ liệu hiện tại ({:.1f}%).".format(
                top_type, type_counts.max()
            )
        )

    if not choice_df.empty:
        s1 = choice_df[choice_df["scenario"] == "scenario_1"]
        s2 = choice_df[choice_df["scenario"] == "scenario_2"]
        report_choices_s1 = s1[s1["choice_text"].str.contains("báo|report", case=False, na=False)] if not s1.empty else s1
        report_choices_s2 = s2[s2["choice_text"].str.contains("báo|report", case=False, na=False)] if not s2.empty else s2
        rate_s1 = (len(report_choices_s1) / len(s1) * 100) if len(s1) else 0
        rate_s2 = (len(report_choices_s2) / len(s2) * 100) if len(s2) else 0
        if rate_s2 > rate_s1:
            insights.append(
                "Scenario 2 (cyberbullying) có tỷ lệ lựa chọn liên quan đến báo cáo "
                "hành vi bắt nạt cao hơn Scenario 1 trong dữ liệu quan sát được."
            )
        elif rate_s1 > rate_s2:
            insights.append(
                "Scenario 1 (bắt nạt trực tiếp) có tỷ lệ lựa chọn liên quan đến báo cáo "
                "hành vi bắt nạt cao hơn Scenario 2 trong dữ liệu quan sát được."
            )

    if not insights:
        insights.append(
            "Chưa phát hiện xu hướng nổi bật nào trong tập dữ liệu hiện tại; "
            "cần thêm dữ liệu để có góc nhìn khám phá (exploratory) rõ ràng hơn."
        )

    insights.append(
        "Lưu ý: các nhận xét trên chỉ mang tính mô tả, khám phá dựa trên hành vi "
        "lựa chọn trong tình huống mô phỏng, không phải kết luận chẩn đoán tâm lý."
    )

    return insights


def build_player_timeline(choice_df: pd.DataFrame, player_id: str) -> pd.DataFrame:
    """All logged decisions for one player, in chronological order (raw rows)."""
    if choice_df.empty:
        return choice_df
    subset = choice_df[choice_df["player_id"] == player_id].copy()
    if "timestamp" in subset.columns:
        subset = subset.sort_values("timestamp")
    return subset


def build_player_timeline_steps(choice_df: pd.DataFrame, player_id: str, bystander_type: str = None) -> list:
    """
    Turn a player's raw choice_data.csv rows into a list of "playthrough"
    groups, ready for a visual (non-plain-text) timeline in the
    dashboard. Each playthrough is a list of step dicts:

        {
            "scenario_label": "Scenario 1 · Bắt nạt trực tiếp",
            "question_label": "Quyết định đầu tiên",
            "code": "A1",
            "text": "Bình tĩnh giải thích ...",   # accented display text
            "category": "Direct Intervention",
            "color": "#e0654f",
            "icon": "⚡",
            "deltas": [("Courage", "🦁", 3), ("Responsibility", "🧭", 2), ...],  # non-zero only
        }

    Every completed playthrough logs exactly 4 rows (Q1+Q2 for each of
    the 2 scenarios), so rows are chunked into groups of 4 in
    chronological order. This also keeps multiple playthroughs under the
    same player_id (e.g. replayed test/sample data) visually separated
    instead of being shown as one confusing run.
    """
    timeline_df = build_player_timeline(choice_df, player_id)
    if timeline_df.empty:
        return []

    steps = []
    for _, row in timeline_df.iterrows():
        key = _choice_key(row)
        category = CHOICE_CATEGORY_MAP.get(key, "Do Nothing")
        style = CATEGORY_STYLE[category]
        deltas = []
        for col, (trait_name, trait_icon) in TRAIT_ICON.items():
            value = row.get(col, 0)
            if pd.notna(value) and value != 0:
                deltas.append((trait_name, trait_icon, int(value)))

        steps.append({
            "scenario_label": SCENARIO_LABELS.get(row.get("scenario"), row.get("scenario")),
            "question_label": QUESTION_LABELS.get(row.get("question_id"), row.get("question_id")),
            "code": row.get("choice"),
            "text": DISPLAY_TEXT_MAP.get(key, row.get("choice_text")),
            "category": category,
            "category_label": style["label_vi"],
            "color": style["color"],
            "icon": style["icon"],
            "deltas": deltas,
        })

    # Chunk into playthroughs of 4 steps each (Q1+Q2 x 2 scenarios).
    playthroughs = [steps[i:i + 4] for i in range(0, len(steps), 4)]
    return playthroughs
