# DEFINE CHARACTERS
define narrator = Character("Người dẫn truyện", cps=32)
define you = Character("Bạn", color="#8fd3ff", cps=32)
define minh = Character("Minh", color="#ffd27f", cps=32)
define lan = Character("Lan", color="#ffb3d9", cps=32)
define teacher = Character("Giáo viên", color="#b3ffb3", cps=32)
define bully1 = Character("Học sinh A", color="#ff9d9d", cps=32)
define bully2 = Character("Học sinh B", color="#ff9d9d", cps=32)
define classmate = Character("Bạn cùng lớp", color="#d0b3ff", cps=32)

# ============================= START GAME ===============================
label start:

    play music "assets/audio/background_sound.mp3" loop

    $ player_id = generate_player_id()
    $ empathy = 0
    $ courage = 0
    $ responsibility = 0
    $ intervention = 0
    $ scenario_1_score = 0
    $ scenario_2_score = 0
    $ total_score = 0
    $ bystander_type = ""
    $ session_choice_log = []

    scene black with t_scene

    centered "{b}BYSTANDER CHOICE{/b}\n\nMột trò chơi mô phỏng dành cho học sinh THPT\n\nvề vai trò của người chứng kiến trong bắt nạt học đường."
    centered "Đây là một nguyên mẫu nghiên cứu (research prototype).\n\nKết quả không dùng để chẩn đoán tâm lý.\n\nDữ liệu được thu thập ẩn danh, không lưu thông tin cá nhân."

    with t_scene

    jump scenario_1
