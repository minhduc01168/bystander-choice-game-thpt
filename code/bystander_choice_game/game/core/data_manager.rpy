## data_manager.rpy
## -----------------------------------------------------------------------
## All data persistence logic lives here (per spec section 14).
## No game/dialogue logic should be written in this file, and no data
## logic should live directly in script.rpy.
##
## Responsibilities:
##   - generate_player_id()   -> unique anonymous ID, e.g. "P00001"
##   - record_choice(...)     -> append one row to choice_data.csv
##   - save_player_result(...)-> append one row to player_summary.csv
##   - export_data(...)       -> convenience helper to flush in-memory log
##
## Privacy note (spec section 23): only an anonymous player_id is ever
## written to disk. No real names, emails, phone numbers, addresses or
## social media handles are collected or stored anywhere in this module.
## -----------------------------------------------------------------------

init -1 python:
    import csv
    import os
    import datetime

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

    def _ensure_data_dir():
        """Make sure game/data exists before any CSV write is attempted."""
        try:
            if not os.path.isdir(DATA_DIR):
                os.makedirs(DATA_DIR)
        except OSError as e:
            # Non-fatal: we still try the write, which will raise its own
            # error if the directory truly cannot be created.
            renpy.log("data_manager: could not create data dir: %s" % e)

    def _write_row(csv_path, fieldnames, row):
        """
        Append a single row to csv_path, creating the file (with a header)
        the first time it is written. Uses newline='' + utf-8 so the file
        never gets corrupted by extra blank lines on Windows and Vietnamese
        text is preserved correctly.
        """
        _ensure_data_dir()
        file_exists = os.path.isfile(csv_path)
        try:
            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists or os.path.getsize(csv_path) == 0:
                    writer.writeheader()
                writer.writerow(row)
            return True
        except (IOError, OSError) as e:
            renpy.log("data_manager: failed to write to %s -> %s" % (csv_path, e))
            # Surface a non-blocking notification in-game rather than
            # crashing the whole session on a data-write failure.
            try:
                renpy.notify("Không thể lưu dữ liệu (xem log).")
            except Exception:
                pass
            return False

    def generate_player_id():
        """
        Generate a unique, sequential, anonymous player id such as
        'P00001'. The counter is stored in Ren'Py persistent data so it
        keeps incrementing across play sessions on the same machine and
        never collides with a previous player's id.
        """
        persistent.player_sequence = (persistent.player_sequence or 0) + 1
        return "P{:05d}".format(persistent.player_sequence)

    def record_choice(player_id, scenario, question_id, branch,
                    choice, choice_text,
                    empathy_change=0, courage_change=0,
                    responsibility_change=0, intervention_change=0):
        """
        Record exactly one player decision. Called immediately after every
        single choice menu resolves (first decision AND second decision),
        so every branch/question the player passes through produces one
        CSV row, per spec section 12.
        """
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        row = {
            "player_id": player_id,
            "timestamp": timestamp,
            "scenario": scenario,
            "question_id": question_id,
            "branch": branch,
            "choice": choice,
            "choice_text": choice_text,
            "empathy_change": empathy_change,
            "courage_change": courage_change,
            "responsibility_change": responsibility_change,
            "intervention_change": intervention_change,
        }

        # Keep an in-memory copy too, useful for the in-game timeline /
        # debugging, and so export_data() can re-flush if needed.
        session_choice_log.append(row)

        ok1 = _write_row(CHOICE_DATA_CSV, CHOICE_FIELDNAMES, row)
        # Mirror into the legacy combined file described in section 12.
        ok2 = _write_row(PLAYER_RESULTS_CSV, CHOICE_FIELDNAMES, row)
        return ok1 and ok2

    def save_player_result(player_id, total_empathy, total_courage,
                            total_responsibility, total_intervention,
                            bystander_type, scenario_1_score,
                            scenario_2_score, total_score):
        """
        Record the final summary row for a completed playthrough, per
        spec section 11 / 12. Called once, at the end of the game.
        """
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        row = {
            "player_id": player_id,
            "timestamp": timestamp,
            "total_empathy": total_empathy,
            "total_courage": total_courage,
            "total_responsibility": total_responsibility,
            "total_intervention": total_intervention,
            "bystander_type": bystander_type,
            "scenario_1_score": scenario_1_score,
            "scenario_2_score": scenario_2_score,
            "total_score": total_score,
        }
        return _write_row(PLAYER_SUMMARY_CSV, SUMMARY_FIELDNAMES, row)

    def export_data():
        """
        Convenience helper: re-flushes the full in-memory session log to
        choice_data.csv. Not required for normal play (record_choice
        already writes incrementally) but useful for debugging, testing,
        or forcing a re-sync if a write ever failed mid-session.
        """
        ok = True
        for row in session_choice_log:
            ok = _write_row(CHOICE_DATA_CSV, CHOICE_FIELDNAMES, row) and ok
        return ok


