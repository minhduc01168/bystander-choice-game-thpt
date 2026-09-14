## endings.rpy
## -----------------------------------------------------------------------
## Runs once both scenarios are complete: classifies the player into a
## bystander_type, persists the final summary row to player_summary.csv,
## and shows the final result screen (spec section 26).
## -----------------------------------------------------------------------

label show_ending:

    $ bystander_type = classify_bystander_type(empathy, courage, responsibility, intervention)

    $ save_player_result(
        player_id,
        empathy, courage, responsibility, intervention,
        bystander_type,
        scenario_1_score, scenario_2_score, total_score,
    )

    $ result_description = get_result_description(bystander_type)

    call screen final_result_screen(
        player_id, bystander_type, result_description,
        empathy, courage, responsibility, intervention,
    )

    if _return == "play_again":
        jump reset_and_restart
    else:
        # "EXIT" returns the player to Ren'Py's built-in main menu rather
        # than relying on an empty call stack (this label is reached via
        # `jump`, not `call`, from script.rpy).
        jump main_menu_screen


label reset_and_restart:
    # Reset in-game state for a brand new playthrough (spec section 15).
    # A fresh player_id is generated and nothing already written to the
    # CSV files for the previous player is touched or overwritten.
    $ empathy = 0
    $ courage = 0
    $ responsibility = 0
    $ intervention = 0
    $ scenario_1_score = 0
    $ scenario_2_score = 0
    $ total_score = 0
    $ bystander_type = ""
    $ session_choice_log = []
    $ player_id = generate_player_id()
    jump scenario_1
