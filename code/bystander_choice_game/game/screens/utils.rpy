# ======================================================================
# A. THEME PALETTE
# ======================================================================

define theme_bg          = "#12141c"   # near-black navy, main menu / frame backdrop
define theme_panel       = "#1c2130cc" # translucent panel behind menus/dialogue
define theme_panel_solid = "#1c2130"
define theme_accent      = "#d8b46a"   # warm gold -- title, selected state
define theme_accent_dim  = "#9c8352"
define theme_text        = "#eef1f5"   # primary text
define theme_text_muted  = "#9aa4b5"   # secondary / idle menu text
define theme_line        = "#39415a"   # hairline dividers / borders


# ======================================================================
# B. TRANSITIONS
# ======================================================================

define t_scene   = Dissolve(0.7)             # background / location changes
define t_quick   = Dissolve(0.35)            # small UI swaps
define t_menu    = Dissolve(0.5)             # entering/leaving the main menu
define t_result  = Fade(0.4, 0.0, 0.6)       # fade-to-black into the result screen

# Smooth fade-in for character sprites entering a scene. Combine with a
transform char_enter:
    alpha 0.0
    ease 0.4 alpha 1.0

# Gentle upward drift + fade, used for the dialogue window and for menu
# panels appearing, so nothing simply "pops" onto the screen.
transform panel_enter:
    alpha 0.0
    yoffset 12
    ease 0.35 alpha 1.0 yoffset 0

# Whole-game defaults: fade between interactions instead of Ren'Py's
# default instant cut, and a soft fade when the dialogue box appears.
define config.enter_transition = t_quick
define config.exit_transition = t_quick
define config.window_show_transition = Dissolve(0.25)
define config.window_hide_transition = Dissolve(0.25)


# ======================================================================
# C. MAIN MENU
# ======================================================================

image main_menu_bg = (
    "images/main_menu_bg.png" if renpy.loadable("images/main_menu_bg.png")
    else theme_bg
)

screen main_menu():

    tag menu

    add "main_menu_bg"

    # Soft dark gradient-like vignette using two stacked translucent
    # panels, so menu text stays readable over any background image.
    add Solid("#00000066")

    frame:
        style "mm_panel"
        align (0.5, 0.5)
        xsize 760
        ysize 560
        at panel_enter

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 6

            text "BYSTANDER CHOICE" style "mm_title" xalign 0.5
            text "Người chứng kiến trong bạo lực học đường" style "mm_subtitle" xalign 0.5

            null height 30

            vbox:
                xalign 0.5
                spacing 4
                style_prefix "mm_button"

                textbutton _("Bắt đầu") action Start()
                textbutton _("Tiếp tục") action ShowMenu("load")
                textbutton _("Tuỳ chỉnh") action ShowMenu("preferences")
                textbutton _("Giới thiệu") action ShowMenu("about")
                textbutton _("Trợ giúp") action Help()
                textbutton _("Thoát") action Quit(confirm=not main_menu)

            null height 20
            text "Research prototype -- không dùng để chẩn đoán tâm lý." style "mm_disclaimer" xalign 0.5

    text "v1.0" style "mm_version"


style mm_panel:
    background theme_panel
    padding (50, 40)

style mm_title:
    font "DejaVuSans.ttf"
    size 52
    color theme_accent
    bold True
    kerning 1

style mm_subtitle:
    size 18
    color theme_text_muted

style mm_disclaimer:
    size 13
    italic True
    color theme_text_muted

style mm_version:
    size 14
    color theme_text_muted
    xalign 1.0
    yalign 1.0
    xoffset -20
    yoffset -16

style mm_button_button:
    background None
    hover_background Solid("#ffffff10")
    padding (18, 10)
    xsize 320
    xalign 0.5

style mm_button_button_text:
    size 24
    color theme_text_muted
    hover_color theme_accent
    selected_color theme_accent
    idle_color theme_text_muted
    outlines []
    text_align 0.5
    layout "subtitle"


# ======================================================================
# D. CHOICE SCREEN (in-game menu:// choices)
# ======================================================================
# Replaces Ren'Py's default stacked plain buttons with vertically
# centered "cards": a thin left accent bar, generous padding, and a
# hover state that brightens the whole card rather than just the text.
# This is the screen used for every `menu:` block in scenarios.rpy.

screen choice(items):

    style_prefix "bc_choice"

    modal True

    add Solid("#00000090")  # dim the scene behind the choices

    vbox:
        align (0.5, 0.55)
        spacing 14
        at panel_enter

        for i in items:
            if i.action:
                button:
                    action i.action
                    style "bc_choice_button"

                    hbox:
                        spacing 14
                        frame:
                            style "bc_choice_bar"
                        text i.caption style "bc_choice_text"
            else:
                text i.caption style "bc_choice_disabled"


style bc_choice_button:
    background theme_panel
    hover_background "#2a3348d9"
    padding (22, 16)
    xsize 920
    xmaximum 920

style bc_choice_bar:
    background theme_text_muted
    xsize 4
    ysize 26
    # brighten the accent bar only on the hovered button
    hover_background theme_accent

style bc_choice_text:
    size 22
    color theme_text
    hover_color theme_accent
    selected_color theme_accent
    text_align 0.0
    xsize 830

style bc_choice_disabled:
    size 20
    color theme_text_muted
    italic True


# ======================================================================
# E. DIALOGUE / SAY SCREEN
# ======================================================================
# A slim floating card near the bottom of the screen instead of a
# full-width opaque bar: rounded-feeling via padding, a colored name
# tab that overlaps the top edge, and the same panel_enter fade-up
# used elsewhere so each line settles in gently instead of popping in.

screen say(who, what):

    style_prefix "bc_say"

    window:
        id "window"
        style "bc_say_window"
        at panel_enter

        if who is not None:
            frame:
                style "bc_say_namebox"
                xalign 0.2
                yoffset -20

                text who style "bc_say_name"

        text what id "what" style "bc_say_dialogue"


style bc_say_window:
    # background theme_panel
    xalign 0.5
    xsize 1500
    xmaximum 1500
    yalign 1.0
    yoffset -40
    padding (36, 26)

style bc_say_namebox:
    # background theme_accent
    padding (18, 6)
    xpos 0


style bc_say_name:
    size 20
    bold True
    color "#141414"
    xalign 0.5
    yalign 0.5

style bc_say_dialogue:
    size 24
    color theme_text
    line_spacing 4
    kerning 0.2


screen scenarios_title(title):

    frame:
        xalign 0.5
        yalign 0.5

        xsize 700
        ysize 120

        background "#12141c"

        text title:
            xalign 0.5
            yalign 0.5
            color "#d8b46a"
            size 40