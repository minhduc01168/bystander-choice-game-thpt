# gen player

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

NUMBER_OF_PLAYERS = 200

players = []

for i in range(1, NUMBER_OF_PLAYERS + 1):

    player_id = f"P{i:03d}"

    gender = random.choice(["Nam", "Nữ"])

    age = random.choice([15, 16, 17])

    empathy = np.clip(np.random.normal(3.7, 0.65), 1, 5)

    confidence = np.clip(0.65 * empathy + np.random.normal(1.05, 0.55), 1, 5)

    intervention = np.clip(
        0.58 * empathy + 0.38 * confidence + np.random.normal(0.05, 0.35), 1, 5
    )

    score = np.clip(
        35 + intervention * 9 + empathy * 6 + confidence * 4 + np.random.normal(0, 7),
        0,
        100,
    )

    intervention_count = int(
        np.clip(round(intervention / 5 * 10 + np.random.normal(0, 1.2)), 0, 10)
    )

    passive_count = 10 - intervention_count

    play_time = int(np.clip(np.random.normal(12, 3), 5, 25))

    players.append(
        {
            "player_id": player_id,
            "gender": gender,
            "age": age,
            "empathy": round(empathy, 2),
            "confidence": round(confidence, 2),
            "intervention": round(intervention, 2),
            "score": round(score, 1),
            "total_questions": 10,
            "intervention_count": intervention_count,
            "passive_count": passive_count,
            "play_time_minutes": play_time,
        }
    )


df = pd.DataFrame(players)

df.to_csv("data/player_data.csv", index=False, encoding="utf-8-sig")

print("Đã tạo dữ liệu:", len(df))

import pandas as pd
import numpy as np
import random

scenarios = [
    "Video bắt nạt trong nhóm chat",
    "Chứng kiến bạn bị cô lập",
    "Bạn bè rủ tham gia bắt nạt",
    "Phát hiện bình luận xúc phạm",
    "Bạn bị quay video và chia sẻ",
]

actions = ["Can thiệp trực tiếp", "Báo giáo viên", "Hỗ trợ nạn nhân", "Không làm gì"]

scenario_rows = []

for _, player in df.iterrows():

    for scenario_id, scenario in enumerate(scenarios, 1):

        probability = (player["intervention"] - 1) / 4

        probability = np.clip(probability, 0.15, 0.85)

        # Tình huống 3 khó hơn
        if scenario_id == 3:
            probability -= 0.10

        is_active = random.random() < probability

        if is_active:
            action = random.choice(actions[:3])
        else:
            action = "Không làm gì"

        scenario_rows.append(
            {
                "player_id": player["player_id"],
                "scenario_id": scenario_id,
                "scenario": scenario,
                "action": action,
                "empathy_response": round(
                    np.clip(player["empathy"] + np.random.normal(0, 0.25), 1, 5), 2
                ),
                "confidence_response": round(
                    np.clip(player["confidence"] + np.random.normal(0, 0.25), 1, 5), 2
                ),
            }
        )


scenario_df = pd.DataFrame(scenario_rows)

scenario_df.to_csv("data/scenario_choices.csv", index=False, encoding="utf-8-sig")

print("Đã tạo dữ liệu tình huống:", len(scenario_df))
