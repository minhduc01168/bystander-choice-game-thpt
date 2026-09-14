## variables.rpy
## -----------------------------------------------------------------------
## Central definition of all persistent / session game state.
## Keeping every `default` declaration in one place makes it easy to see
## the full state surface of the game and avoids duplicate declarations
## scattered across other .rpy files.
## -----------------------------------------------------------------------

# --- Psychological score variables (reset every new game) ---------------
default empathy = 0
default courage = 0
default responsibility = 0
default intervention = 0

# --- Per-scenario subtotal snapshots (captured right after each ending) --
default scenario_1_score = 0
default scenario_2_score = 0
default total_score = 0

# --- Bystander classification result -------------------------------------
default bystander_type = ""

# --- Identity / session bookkeeping (NOT real personal data) -------------
default player_id = ""
default session_choice_log = []   # list of dicts, flushed to CSV at checkpoints
default current_scenario = ""
default current_branch = ""

# --- Persistent counter used only to generate sequential anonymous IDs ---
default persistent.player_sequence = 0

init -1 python:
    # Root of the game's writable data folder. Ren'Py resolves relative
    # paths from the game directory, so this always points at
    # <project>/game/data regardless of platform (Windows/Mac/Linux).
    import os
    DATA_DIR = os.path.join(config.gamedir, "data")
    CHOICE_DATA_CSV = os.path.join(DATA_DIR, "choice_data.csv")
    PLAYER_SUMMARY_CSV = os.path.join(DATA_DIR, "player_summary.csv")
    # Legacy / combined log kept for backward compatibility with section 12
    # of the spec (player_results.csv), mirrors choice_data.csv rows.
    PLAYER_RESULTS_CSV = os.path.join(DATA_DIR, "player_results.csv")
