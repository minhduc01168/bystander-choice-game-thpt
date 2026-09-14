"""
sample_data_generator.py
-----------------------------------------------------------------------
Generates a synthetic dataset of ~N simulated players (default 100) so
the Streamlit dashboard can be tested and demoed without having to play
the Ren'Py game N times.

Simulates a full playthrough for each player by randomly walking through
the same decision tree defined in game/scenarios.rpy (mirrored here as
plain data), applying the same score deltas and classification rules
used by the real game (game/scoring.rpy), and writing rows into the
same two CSV files the game itself writes to:

    game/data/choice_data.csv
    game/data/player_summary.csv

Usage:
    cd dashboard
    python sample_data_generator.py            # 100 players (default)
    python sample_data_generator.py --n 250    # custom player count
    python sample_data_generator.py --reset    # overwrite existing files
-----------------------------------------------------------------------
"""

import argparse
import csv
import datetime
import os
import random

DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DASHBOARD_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "game", "data")
CHOICE_CSV = os.path.join(DATA_DIR, "choice_data.csv")
SUMMARY_CSV = os.path.join(DATA_DIR, "player_summary.csv")

CHOICE_FIELDNAMES = [
    "player_id", "timestamp", "scenario", "question_id", "branch",
    "choice", "choice_text",
    "empathy_change", "courage_change",
    "responsibility_change", "intervention_change",
]

SUMMARY_FIELDNAMES = [
    "player_id", "timestamp",
    "total_empathy", "total_courage",
    "total_responsibility", "total_intervention",
    "bystander_type",
    "scenario_1_score", "scenario_2_score", "total_score",
]

# Mirrors the decision tree + score deltas defined in game/scenarios.rpy.
# Structure: scenario -> first-choice code -> {
#   text, deltas, second_decisions: [ (code, text, deltas), ... ]
# }
DECISION_TREE = {
    "scenario_1": {
        "A": {
            "text": "Di toi va yeu cau nhom hoc sinh dung lai.",
            "deltas": (1, 4, 3, 4),
            "branch": "A",
            "second": [
                ("A1", "Binh tinh giai thich hanh dong nay khong dung.", (0, 3, 2, 2)),
                ("A2", "Goi them mot nguoi ban toi ho tro.", (0, 0, 2, 2)),
                ("A3", "Tim giao vien va bao su viec.", (0, 0, 3, 3)),
                ("A4", "So hai va rut lui.", (0, -2, 0, -1)),
            ],
        },
        "B": {
            "text": "Di tim giao vien hoac nhan vien nha truong.",
            "deltas": (1, 2, 3, 3),
            "branch": "B",
            "second": [
                ("B1", "Khang dinh minh truc tiep chung kien.", (0, 2, 3, 2)),
                ("B2", "De nghi giao vien di kiem tra.", (0, 0, 2, 3)),
                ("B3", "Noi rang co the chi la dua.", (0, 0, -1, -1)),
                ("B4", "Noi rang Minh nen tu giai quyet.", (0, 0, -2, -2)),
            ],
        },
        "C": {
            "text": "Dung lai quan sat nhung chua lam gi.",
            "deltas": (1, 0, 0, 0),
            "branch": "C",
            "second": [
                ("C1", "Tien toi ho tro Minh.", (3, 0, 0, 2)),
                ("C2", "Nhan tin hoi Minh co on khong.", (3, 0, 0, 1)),
                ("C3", "Cho nhom hoc sinh roi di roi ho tro Minh.", (2, 0, 1, 1)),
                ("C4", "Tiep tuc dung ngoai.", (0, 0, 0, 0)),
            ],
        },
        "D": {
            "text": "Bo di vi nghi do khong phai chuyen cua minh.",
            "deltas": (0, 0, -1, 0),
            "branch": "D",
            "second": [
                ("D1", "Bao giao vien.", (0, 0, 3, 3)),
                ("D2", "Nhan rieng cho Minh.", (3, 0, 0, 2)),
                ("D3", "Khong binh luan nhung tiep tuc theo doi.", (0, 0, 0, 0)),
                ("D4", "Tham gia binh luan che gieu.", (-3, 0, -3, -3)),
            ],
        },
    },
    "scenario_2": {
        "A": {
            "text": "Bao moi nguoi dung lai.",
            "deltas": (1, 4, 4, 3),
            "branch": "A",
            "second": [
                ("A1", "Giai thich vi sao hanh dong nay co the lam Lan ton thuong.", (3, 2, 0, 0)),
                ("A2", "Noi rang se bao giao vien neu tiep tuc.", (0, 3, 3, 2)),
                ("A3", "Thoat group.", (0, 0, -2, -2)),
                ("A4", "Im lang.", (0, -1, 0, 0)),
            ],
        },
        "B": {
            "text": "Nhan rieng cho Lan.",
            "deltas": (4, 1, 2, 2),
            "branch": "B",
            "second": [
                ("B1", "Noi rang ban se o ben va cung tim cach giai quyet.", (4, 0, 0, 3)),
                ("B2", "Khuyen Lan luu bang chung va bao nguoi lon.", (0, 0, 3, 3)),
                ("B3", "Noi Ban dung de y ho.", (1, 0, 0, 0)),
                ("B4", "Khong tra loi.", (-2, 0, -2, 0)),
            ],
        },
        "C": {
            "text": "Bao cao bai dang.",
            "deltas": (0, 0, 3, 3),
            "branch": "C",
            "second": [
                ("C1", "Giu quyet dinh bao cao.", (0, 3, 3, 0)),
                ("C2", "Giai thich ly do bao cao.", (0, 2, 3, 2)),
                ("C3", "Khong tra loi.", (0, 0, 1, 0)),
                ("C4", "Huy bao cao.", (0, 0, -3, -3)),
            ],
        },
        "D": {
            "text": "Khong lam gi.",
            "deltas": (0, 0, 0, 0),
            "branch": "D",
            "second": [
                ("D1", "Noi voi giao vien nhung gi minh biet.", (0, 0, 4, 3)),
                ("D2", "Noi chuyen rieng voi giao vien.", (0, 2, 3, 2)),
                ("D3", "Im lang.", (0, 0, -1, 0)),
                ("D4", "Noi Em khong biet gi ca.", (0, 0, -3, -3)),
            ],
        },
    },
}


def classify_bystander_type(empathy_v, courage_v, responsibility_v, intervention_v):
    """Identical rules to game/scoring.rpy's classify_bystander_type()."""
    if intervention_v >= 10 and courage_v >= 7 and responsibility_v >= 7:
        return "ACTIVE BYSTANDER"
    if empathy_v >= 8 and intervention_v >= 6 and courage_v < 7:
        return "SUPPORTIVE BYSTANDER"
    if intervention_v < 6 and responsibility_v < 6:
        return "PASSIVE BYSTANDER"
    if empathy_v < 4 and responsibility_v < 4 and intervention_v < 4:
        return "AVOIDANT BYSTANDER"
    if intervention_v >= responsibility_v and intervention_v >= empathy_v:
        return "SUPPORTIVE BYSTANDER"
    return "PASSIVE BYSTANDER"


def simulate_player(player_id, choice_rows, rng):
    empathy = courage = responsibility = intervention = 0
    scenario_scores = {}

    for scenario in ("scenario_1", "scenario_2"):
        first_code = rng.choice(list(DECISION_TREE[scenario].keys()))
        node = DECISION_TREE[scenario][first_code]

        e, c, r, i = node["deltas"]
        empathy += e; courage += c; responsibility += r; intervention += i
        choice_rows.append(_make_choice_row(
            player_id, scenario, "Q1", "-", first_code, node["text"], e, c, r, i
        ))

        second_code, second_text, (e2, c2, r2, i2) = rng.choice(node["second"])
        empathy += e2; courage += c2; responsibility += r2; intervention += i2
        choice_rows.append(_make_choice_row(
            player_id, scenario, "Q2", node["branch"], second_code, second_text, e2, c2, r2, i2
        ))

        scenario_scores[scenario] = empathy + courage + responsibility + intervention

    scenario_1_score = scenario_scores["scenario_1"]
    scenario_2_score = scenario_scores["scenario_2"] - scenario_scores["scenario_1"]
    total_score = scenario_scores["scenario_2"]

    bystander_type = classify_bystander_type(empathy, courage, responsibility, intervention)

    return {
        "player_id": player_id,
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "total_empathy": empathy,
        "total_courage": courage,
        "total_responsibility": responsibility,
        "total_intervention": intervention,
        "bystander_type": bystander_type,
        "scenario_1_score": scenario_1_score,
        "scenario_2_score": scenario_2_score,
        "total_score": total_score,
    }


def _make_choice_row(player_id, scenario, question_id, branch, choice, choice_text, e, c, r, i):
    return {
        "player_id": player_id,
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "scenario": scenario,
        "question_id": question_id,
        "branch": branch,
        "choice": choice,
        "choice_text": choice_text,
        "empathy_change": e,
        "courage_change": c,
        "responsibility_change": r,
        "intervention_change": i,
    }


def write_csv(path, fieldnames, rows, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_header = mode == "w" or not os.path.isfile(path) or os.path.getsize(path) == 0
    with open(path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate sample Bystander Choice data.")
    parser.add_argument("--n", type=int, default=100, help="Number of simulated players (default: 100)")
    parser.add_argument("--reset", action="store_true", help="Overwrite existing CSV files instead of appending")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    choice_rows = []
    summary_rows = []
    for idx in range(1, args.n + 1):
        player_id = "P{:05d}".format(idx)
        summary_rows.append(simulate_player(player_id, choice_rows, rng))

    mode = "w" if args.reset else "a"
    write_csv(CHOICE_CSV, CHOICE_FIELDNAMES, choice_rows, mode=mode)
    write_csv(SUMMARY_CSV, SUMMARY_FIELDNAMES, summary_rows, mode=mode)

    print("Generated {} simulated players.".format(args.n))
    print("Wrote: {}".format(CHOICE_CSV))
    print("Wrote: {}".format(SUMMARY_CSV))


if __name__ == "__main__":
    main()
