# DEFINE IMAGE LINKS

image background_senc01 = "assets/images/scenarios01.png"
image background_senc02 = "assets/images/scenarios02.png"

image background_sc01_branchA = "assets/images/sc1/c_a.png"
image background_sc01_branchB = "assets/images/sc1/c_b.png"
image background_sc01_branchC = "assets/images/sc1/c_c.png"
image background_sc01_branchD = "assets/images/sc1/c_d.png"

image background_sc02_branchA = "assets/images/sc2/c_a.jpeg"
image background_sc02_branchB = "assets/images/sc2/c_b.jpeg"
image background_sc02_branchC = "assets/images/sc2/c_c.jpeg"
image background_sc02_branchD = "assets/images/sc2/c_d.jpeg"

# ============================= SCENARIO 1 ===============================

label scenario_1:

    show screen scenarios_title("{b}TÌNH HUỐNG 1{/b}") 
    pause 1.5
    hide screen scenarios_title

    $ current_scenario = "scenario_1"

    scene background_senc01 with t_scene

    narrator "Sau giờ học, bạn đi ngang qua hành lang trên đường về nhà."

    narrator "Bạn nhìn thấy Minh — một học sinh khá ít nói — đang bị một nhóm học sinh chặn lại."
    narrator "Một học sinh giật lấy cặp sách của Minh."
    narrator "Một học sinh khác giơ điện thoại lên, quay video."

    minh "Trả cặp cho mình đi..."

    narrator "Bạn đứng đó, chứng kiến toàn bộ sự việc."

    label scenario_1_q1:
        $ current_branch = ""
        menu:
            "Bạn sẽ làm gì?"

            "Đi tới và yêu cầu nhóm học sinh dừng lại.":
                $ apply_score(empathy_d=1, courage_d=4, responsibility_d=3, intervention_d=4)
                $ record_choice(player_id, "scenario_1", "Q1", "-", "A",
                    "Di toi va yeu cau nhom hoc sinh dung lai.", 1, 4, 3, 4)
                jump scenario_1_branch_a

            "Đi tìm giáo viên hoặc nhân viên nhà trường.":
                $ apply_score(empathy_d=1, courage_d=2, responsibility_d=3, intervention_d=3)
                $ record_choice(player_id, "scenario_1", "Q1", "-", "B",
                    "Di tim giao vien hoac nhan vien nha truong.", 1, 2, 3, 3)
                jump scenario_1_branch_b

            "Đứng lại quan sát nhưng chưa làm gì.":
                $ apply_score(empathy_d=1, courage_d=0, responsibility_d=0, intervention_d=0)
                $ record_choice(player_id, "scenario_1", "Q1", "-", "C",
                    "Dung lai quan sat nhung chua lam gi.", 1, 0, 0, 0)
                jump scenario_1_branch_c

            "Bỏ đi vì nghĩ đó không phải chuyện của mình.":
                $ apply_score(empathy_d=0, courage_d=0, responsibility_d=-1, intervention_d=0)
                $ record_choice(player_id, "scenario_1", "Q1", "-", "D",
                    "Bo di vi nghi do khong phai chuyen cua minh.", 0, 0, -1, 0)
                jump scenario_1_branch_d


## --- Branch A: Direct Intervention --------------------------------------
label scenario_1_branch_a:
    scene background_sc01_branchA with t_scene

    $ current_branch = "A"
    you "Thôi đi. Trả cặp cho Minh."
    bully1 "Liên quan gì đến mày?"

    menu:
        "Bạn phản ứng thế nào?"

        "Bình tĩnh giải thích rằng hành động này không đúng.":
            $ apply_score(courage_d=3, responsibility_d=2, intervention_d=2)
            $ record_choice(player_id, "scenario_1", "Q2", "A", "A1",
                "Binh tinh giai thich hanh dong nay khong dung.", 0, 3, 2, 2)

        "Gọi thêm một người bạn tới hỗ trợ.":
            $ apply_score(responsibility_d=2, intervention_d=2)
            $ record_choice(player_id, "scenario_1", "Q2", "A", "A2",
                "Goi them mot nguoi ban toi ho tro.", 0, 0, 2, 2)

        "Tìm giáo viên và báo sự việc.":
            $ apply_score(responsibility_d=3, intervention_d=3)
            $ record_choice(player_id, "scenario_1", "Q2", "A", "A3",
                "Tim giao vien va bao su viec.", 0, 0, 3, 3)

        "Sợ hãi và rút lui.":
            $ apply_score(courage_d=-2, intervention_d=-1)
            $ record_choice(player_id, "scenario_1", "Q2", "A", "A4",
                "So hai va rut lui.", 0, -2, 0, -1)

    jump scenario_1_end


## --- Branch B: Find Teacher ----------------------------------------------
label scenario_1_branch_b:
    scene background_sc01_branchB with t_scene


    $ current_branch = "B"

    teacher "Em có chắc đó là bắt nạt không?"

    menu:
        "Bạn trả lời thế nào?"

        "Khẳng định mình trực tiếp chứng kiến.":
            $ apply_score(responsibility_d=3, courage_d=2, intervention_d=2)
            $ record_choice(player_id, "scenario_1", "Q2", "B", "B1",
                "Khang dinh minh truc tiep chung kien.", 0, 2, 3, 2)

        "Đề nghị giáo viên đi kiểm tra.":
            $ apply_score(responsibility_d=2, intervention_d=3)
            $ record_choice(player_id, "scenario_1", "Q2", "B", "B2",
                "De nghi giao vien di kiem tra.", 0, 0, 2, 3)

        "Nói rằng có thể chỉ là đùa.":
            $ apply_score(responsibility_d=-1, intervention_d=-1)
            $ record_choice(player_id, "scenario_1", "Q2", "B", "B3",
                "Noi rang co the chi la dua.", 0, 0, -1, -1)

        "Nói rằng Minh nên tự giải quyết.":
            $ apply_score(responsibility_d=-2, intervention_d=-2)
            $ record_choice(player_id, "scenario_1", "Q2", "B", "B4",
                "Noi rang Minh nen tu giai quyet.", 0, 0, -2, -2)

    jump scenario_1_end


## --- Branch C: Observe ----------------------------------------------------
label scenario_1_branch_c:
    scene background_sc01_branchC with t_scene


    $ current_branch = "C"

    narrator "Minh nhìn về phía bạn."

    menu:
        "Bạn làm gì tiếp theo?"

        "Tiến tới hỗ trợ Minh.":
            $ apply_score(empathy_d=3, intervention_d=2)
            $ record_choice(player_id, "scenario_1", "Q2", "C", "C1",
                "Tien toi ho tro Minh.", 3, 0, 0, 2)

        "Nhắn tin hỏi Minh có ổn không.":
            $ apply_score(empathy_d=3, intervention_d=1)
            $ record_choice(player_id, "scenario_1", "Q2", "C", "C2",
                "Nhan tin hoi Minh co on khong.", 3, 0, 0, 1)

        "Chờ nhóm học sinh rời đi rồi hỗ trợ Minh.":
            $ apply_score(empathy_d=2, responsibility_d=1, intervention_d=1)
            $ record_choice(player_id, "scenario_1", "Q2", "C", "C3",
                "Cho nhom hoc sinh roi di roi ho tro Minh.", 2, 0, 1, 1)

        "Tiếp tục đứng ngoài.":
            $ apply_score(intervention_d=0)
            $ record_choice(player_id, "scenario_1", "Q2", "C", "C4",
                "Tiep tuc dung ngoai.", 0, 0, 0, 0)

    jump scenario_1_end


## --- Branch D: Leave --------------------------------------------------
label scenario_1_branch_d:
    scene background_sc01_branchD with t_scene

    $ current_branch = "D"

    narrator "Bạn bỏ đi. Sau đó, một đoạn video về vụ bắt nạt xuất hiện trong group chat của lớp."

    menu:
        "Bạn phản ứng thế nào?"

        "Báo giáo viên.":
            $ apply_score(responsibility_d=3, intervention_d=3)
            $ record_choice(player_id, "scenario_1", "Q2", "D", "D1",
                "Bao giao vien.", 0, 0, 3, 3)

        "Nhắn riêng cho Minh.":
            $ apply_score(empathy_d=3, intervention_d=2)
            $ record_choice(player_id, "scenario_1", "Q2", "D", "D2",
                "Nhan rieng cho Minh.", 3, 0, 0, 2)

        "Không bình luận nhưng tiếp tục theo dõi.":
            $ apply_score(intervention_d=0)
            $ record_choice(player_id, "scenario_1", "Q2", "D", "D3",
                "Khong binh luan nhung tiep tuc theo doi.", 0, 0, 0, 0)

        "Tham gia bình luận chế giễu.":
            $ apply_score(empathy_d=-3, responsibility_d=-3, intervention_d=-3)
            $ record_choice(player_id, "scenario_1", "Q2", "D", "D4",
                "Tham gia binh luan che gieu.", -3, 0, -3, -3)

    jump scenario_1_end


label scenario_1_end:
    $ snapshot_scenario_score("scenario_1")

    narrator "Một ngày ở trường đã kết thúc."

    scene black with t_scene


    show screen scenarios_title("{b}KẾT THÚC TÌNH HUỐNG 1{/b}") 
    pause 1.5
    hide screen scenarios_title
    
    scene black with t_scene

    jump scenario_2


# ============================= SCENARIO 2 ===============================

label scenario_2:
    
    show screen scenarios_title("{b}TÌNH HUỐNG 2{/b}") 
    pause 1.5
    hide screen scenarios_title

    $ current_scenario = "scenario_2"

    scene background_senc02 with t_scene

    narrator "Tối hôm đó, trong group chat của lớp, một học sinh đăng một tấm ảnh của Lan."
    narrator "Tấm ảnh đã bị chỉnh sửa nhằm chế giễu Lan."

    classmate "Hahaha 🤣🤣🤣"
    classmate "Đăng tiếp đi."
    classmate "Lan mà biết chắc khóc."

    narrator "Lan đang online nhưng không nói gì."
    narrator "Bạn nhìn thấy toàn bộ cuộc trò chuyện."

    label scenario_2_q1:
        $ current_branch = ""
        menu:
            "Bạn sẽ làm gì?"

            "Bảo mọi người dừng lại.":
                $ apply_score(empathy_d=1, courage_d=4, responsibility_d=4, intervention_d=3)
                $ record_choice(player_id, "scenario_2", "Q1", "-", "A",
                    "Bao moi nguoi dung lai.", 1, 4, 4, 3)
                jump scenario_2_branch_a

            "Nhắn riêng cho Lan.":
                $ apply_score(empathy_d=4, courage_d=1, responsibility_d=2, intervention_d=2)
                $ record_choice(player_id, "scenario_2", "Q1", "-", "B",
                    "Nhan rieng cho Lan.", 4, 1, 2, 2)
                jump scenario_2_branch_b

            "Báo cáo bài đăng.":
                $ apply_score(responsibility_d=3, intervention_d=3)
                $ record_choice(player_id, "scenario_2", "Q1", "-", "C",
                    "Bao cao bai dang.", 0, 0, 3, 3)
                jump scenario_2_branch_c

            "Không làm gì.":
                $ apply_score(intervention_d=0)
                $ record_choice(player_id, "scenario_2", "Q1", "-", "D",
                    "Khong lam gi.", 0, 0, 0, 0)
                jump scenario_2_branch_d


## --- Branch A -------------------------------------------------------------
label scenario_2_branch_a:

    scene background_sc02_branchA with t_scene

    $ current_branch = "A"
    classmate "Làm gì căng vậy? Đùa thôi mà."

    menu:
        "Bạn trả lời thế nào?"

        "Giải thích vì sao hành động này có thể làm Lan tổn thương.":
            $ apply_score(empathy_d=3, courage_d=2)
            $ record_choice(player_id, "scenario_2", "Q2", "A", "A1",
                "Giai thich vi sao hanh dong nay co the lam Lan ton thuong.", 3, 2, 0, 0)

        "Nói rằng sẽ báo giáo viên nếu tiếp tục.":
            $ apply_score(courage_d=3, responsibility_d=3, intervention_d=2)
            $ record_choice(player_id, "scenario_2", "Q2", "A", "A2",
                "Noi rang se bao giao vien neu tiep tuc.", 0, 3, 3, 2)

        "Thoát group.":
            $ apply_score(responsibility_d=-2, intervention_d=-2)
            $ record_choice(player_id, "scenario_2", "Q2", "A", "A3",
                "Thoat group.", 0, 0, -2, -2)

        "Im lặng.":
            $ apply_score(courage_d=-1)
            $ record_choice(player_id, "scenario_2", "Q2", "A", "A4",
                "Im lang.", 0, -1, 0, 0)

    jump scenario_2_end


## --- Branch B -------------------------------------------------------------
label scenario_2_branch_b:
    scene background_sc02_branchB with t_scene

    $ current_branch = "B"
    lan "Mình không biết phải làm gì nữa..."

    menu:
        "Bạn nhắn lại gì?"

        "Nói rằng bạn sẽ ở bên và cùng tìm cách giải quyết.":
            $ apply_score(empathy_d=4, intervention_d=3)
            $ record_choice(player_id, "scenario_2", "Q2", "B", "B1",
                "Noi rang ban se o ben va cung tim cach giai quyet.", 4, 0, 0, 3)

        "Khuyên Lan lưu bằng chứng và báo người lớn.":
            $ apply_score(responsibility_d=3, intervention_d=3)
            $ record_choice(player_id, "scenario_2", "Q2", "B", "B2",
                "Khuyen Lan luu bang chung va bao nguoi lon.", 0, 0, 3, 3)

        "Nói \"Bạn đừng để ý họ.\"":
            $ apply_score(empathy_d=1)
            $ record_choice(player_id, "scenario_2", "Q2", "B", "B3",
                "Noi Ban dung de y ho.", 1, 0, 0, 0)

        "Không trả lời.":
            $ apply_score(empathy_d=-2, responsibility_d=-2)
            $ record_choice(player_id, "scenario_2", "Q2", "B", "B4",
                "Khong tra loi.", -2, 0, -2, 0)

    jump scenario_2_end


## --- Branch C -------------------------------------------------------------
label scenario_2_branch_c:
    scene background_sc02_branchC with t_scene

    $ current_branch = "C"
    classmate "Ai report vậy?"

    menu:
        "Bạn phản hồi thế nào?"

        "Giữ quyết định báo cáo.":
            $ apply_score(courage_d=3, responsibility_d=3)
            $ record_choice(player_id, "scenario_2", "Q2", "C", "C1",
                "Giu quyet dinh bao cao.", 0, 3, 3, 0)

        "Giải thích lý do báo cáo.":
            $ apply_score(courage_d=2, responsibility_d=3, intervention_d=2)
            $ record_choice(player_id, "scenario_2", "Q2", "C", "C2",
                "Giai thich ly do bao cao.", 0, 2, 3, 2)

        "Không trả lời.":
            $ apply_score(responsibility_d=1)
            $ record_choice(player_id, "scenario_2", "Q2", "C", "C3",
                "Khong tra loi.", 0, 0, 1, 0)

        "Hủy báo cáo.":
            $ apply_score(responsibility_d=-3, intervention_d=-3)
            $ record_choice(player_id, "scenario_2", "Q2", "C", "C4",
                "Huy bao cao.", 0, 0, -3, -3)

    jump scenario_2_end


## --- Branch D -------------------------------------------------------------
label scenario_2_branch_d:
    scene background_sc02_branchD with t_scene

    $ current_branch = "D"
    scene bg classroom with t_scene
    narrator "Ngày hôm sau, Lan nghỉ học."
    teacher "Có ai biết chuyện gì xảy ra với Lan không?"

    menu:
        "Bạn trả lời thế nào?"

        "Nói với giáo viên những gì mình biết.":
            $ apply_score(responsibility_d=4, intervention_d=3)
            $ record_choice(player_id, "scenario_2", "Q2", "D", "D1",
                "Noi voi giao vien nhung gi minh biet.", 0, 0, 4, 3)

        "Nói chuyện riêng với giáo viên.":
            $ apply_score(responsibility_d=3, courage_d=2, intervention_d=2)
            $ record_choice(player_id, "scenario_2", "Q2", "D", "D2",
                "Noi chuyen rieng voi giao vien.", 0, 2, 3, 2)

        "Im lặng.":
            $ apply_score(responsibility_d=-1)
            $ record_choice(player_id, "scenario_2", "Q2", "D", "D3",
                "Im lang.", 0, 0, -1, 0)

        "Nói \"Em không biết gì cả.\"":
            $ apply_score(responsibility_d=-3, intervention_d=-3)
            $ record_choice(player_id, "scenario_2", "Q2", "D", "D4",
                "Noi Em khong biet gi ca.", 0, 0, -3, -3)

    jump scenario_2_end


label scenario_2_end:
    $ snapshot_scenario_score("scenario_2")
    scene black with t_scene

    show screen scenarios_title("{b}KẾT THÚC TÌNH HUỐNG 2{/b}") 
    pause 1.5
    hide screen scenarios_title
    
    scene black with t_scene

    jump show_ending
