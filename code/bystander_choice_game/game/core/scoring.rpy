## scoring.rpy
## -----------------------------------------------------------------------
## Pure scoring logic: applying deltas to the four psychological
## variables, snapshotting per-scenario subtotals, and classifying the
## final bystander type. No dialogue text and no CSV writing lives here
## (that belongs to scenarios.rpy / data_manager.rpy respectively).
## -----------------------------------------------------------------------

init -1 python:

    def apply_score(empathy_d=0, courage_d=0, responsibility_d=0, intervention_d=0):
        """
        Apply a single choice's score deltas to the four running totals.
        Centralizing this in one function means every choice in
        scenarios.rpy calls the same code path, avoiding copy-pasted
        `store.empathy += ...` lines and any risk of a typo skipping a
        variable.
        """
        store.empathy += empathy_d
        store.courage += courage_d
        store.responsibility += responsibility_d
        store.intervention += intervention_d

    def snapshot_scenario_score(which):
        """
        Capture a simple combined subtotal for 'scenario_1' or
        'scenario_2', taken as the sum of the four running totals at the
        moment the scenario ends. Used for the CSV summary row and the
        dashboard's "Scenario 1 vs Scenario 2" comparison chart.
        """
        current_sum = store.empathy + store.courage + store.responsibility + store.intervention
        if which == "scenario_1":
            store.scenario_1_score = current_sum
        elif which == "scenario_2":
            # scenario_2_score is the marginal contribution of scenario 2
            # alone (total after both scenarios, minus scenario 1's part).
            store.scenario_2_score = current_sum - store.scenario_1_score
        store.total_score = current_sum

    def classify_bystander_type(empathy_v, courage_v, responsibility_v, intervention_v):
        """
        Classify the player into exactly one of four bystander profiles.
        Conditions are checked in priority order per spec section 10:
        ACTIVE > SUPPORTIVE > PASSIVE > AVOIDANT, with a safe fallback
        for any score combination that does not cleanly match one of the
        four defined rule sets.
        """
        if (intervention_v >= 10 and courage_v >= 7 and responsibility_v >= 7):
            return "ACTIVE BYSTANDER"

        if (empathy_v >= 8 and intervention_v >= 6 and courage_v < 7):
            return "SUPPORTIVE BYSTANDER"

        if (intervention_v < 6 and responsibility_v < 6):
            return "PASSIVE BYSTANDER"

        if (empathy_v < 4 and responsibility_v < 4 and intervention_v < 4):
            return "AVOIDANT BYSTANDER"

        # Fallback: none of the four rule sets matched exactly (this can
        # happen with mixed profiles, e.g. high empathy + high courage but
        # moderate intervention). Default to the closest descriptive
        # category rather than leaving bystander_type empty.
        if intervention_v >= responsibility_v and intervention_v >= empathy_v:
            return "SUPPORTIVE BYSTANDER"
        return "PASSIVE BYSTANDER"

    def get_result_description(bystander_type_v):
        """Descriptive (non-diagnostic) blurb shown on the final result screen."""
        descriptions = {
            "ACTIVE BYSTANDER": (
                "Các lựa chọn của bạn cho thấy xu hướng chủ động can thiệp "
                "và tìm kiếm giải pháp khi chứng kiến bắt nạt."
            ),
            "SUPPORTIVE BYSTANDER": (
                "Các lựa chọn của bạn cho thấy sự đồng cảm cao và xu hướng "
                "hỗ trợ nạn nhân, dù còn do dự khi đối đầu trực tiếp."
            ),
            "PASSIVE BYSTANDER": (
                "Các lựa chọn của bạn cho thấy bạn nhận biết vấn đề nhưng "
                "thường chưa chuyển nhận thức thành hành động cụ thể."
            ),
            "AVOIDANT BYSTANDER": (
                "Các lựa chọn của bạn cho thấy xu hướng tránh tham gia "
                "hoặc giữ khoảng cách với trách nhiệm của người chứng kiến."
            ),
        }
        return descriptions.get(
            bystander_type_v,
            "Kết quả cho thấy xu hướng hành vi của bạn trong các tình huống mô phỏng."
        )
