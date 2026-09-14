"""
data_loader.py
-----------------------------------------------------------------------
Loads the two CSV files produced by the Ren'Py game (choice_data.csv and
player_summary.csv) into pandas DataFrames, with defensive handling for:
    - missing files (first run, before anyone has played)
    - empty files (header only, or truly empty)
    - a single player's worth of data
    - wrong / mixed encodings

All functions return a well-formed (possibly empty) DataFrame with the
expected columns, so the rest of the dashboard never has to special-case
"file not found".
-----------------------------------------------------------------------
"""

import os
import pandas as pd

# Resolve paths relative to this file so `streamlit run app.py` works
# regardless of the current working directory the user launches it from.
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(DASHBOARD_DIR))
DATA_DIR = os.path.join(PROJECT_ROOT, "game", "data")


CHOICE_DATA_PATH = os.path.join(DATA_DIR, "choice_data.csv")
PLAYER_SUMMARY_PATH = os.path.join(DATA_DIR, "player_summary.csv")

CHOICE_COLUMNS = [
    "player_id",
    "timestamp",
    "scenario",
    "question_id",
    "branch",
    "choice",
    "choice_text",
    "empathy_change",
    "courage_change",
    "responsibility_change",
    "intervention_change",
]

SUMMARY_COLUMNS = [
    "player_id",
    "timestamp",
    "total_empathy",
    "total_courage",
    "total_responsibility",
    "total_intervention",
    "bystander_type",
    "scenario_1_score",
    "scenario_2_score",
    "total_score",
]

NUMERIC_CHOICE_COLS = [
    "empathy_change",
    "courage_change",
    "responsibility_change",
    "intervention_change",
]

NUMERIC_SUMMARY_COLS = [
    "total_empathy",
    "total_courage",
    "total_responsibility",
    "total_intervention",
    "scenario_1_score",
    "scenario_2_score",
    "total_score",
]


def _safe_read_csv(path, expected_columns):
    """
    Read a CSV file defensively. Returns an empty DataFrame with the
    expected columns if the file is missing, empty, or unparsable, so
    callers never need to check `if df is None`.
    """
    if not os.path.isfile(path):
        return pd.DataFrame(columns=expected_columns)

    try:
        if os.path.getsize(path) == 0:
            return pd.DataFrame(columns=expected_columns)
        df = pd.read_csv(path, encoding="utf-8")
    except (pd.errors.EmptyDataError, UnicodeDecodeError, OSError):
        return pd.DataFrame(columns=expected_columns)

    if df.empty:
        return pd.DataFrame(columns=expected_columns)

    # Guarantee every expected column exists, even if an older CSV
    # version is missing one (forward-compatibility with future scenarios).
    for col in expected_columns:
        if col not in df.columns:
            df[col] = pd.NA

    return df


def load_choice_data():
    """Load choice_data.csv (one row per decision made by every player)."""
    df = _safe_read_csv(CHOICE_DATA_PATH, CHOICE_COLUMNS)
    for col in NUMERIC_CHOICE_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    if "timestamp" in df.columns and not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df


def load_player_summary():
    """Load player_summary.csv (one row per completed playthrough)."""
    df = _safe_read_csv(PLAYER_SUMMARY_PATH, SUMMARY_COLUMNS)
    for col in NUMERIC_SUMMARY_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    if "timestamp" in df.columns and not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "bystander_type" in df.columns:
        df["bystander_type"] = df["bystander_type"].fillna("UNKNOWN")
    return df


def data_files_exist():
    """Whether at least one of the two data files is present and non-empty."""
    choice_ok = (
        os.path.isfile(CHOICE_DATA_PATH) and os.path.getsize(CHOICE_DATA_PATH) > 0
    )
    summary_ok = (
        os.path.isfile(PLAYER_SUMMARY_PATH) and os.path.getsize(PLAYER_SUMMARY_PATH) > 0
    )
    return choice_ok or summary_ok
