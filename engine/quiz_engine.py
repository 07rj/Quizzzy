import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh


def run_exam(questions, exam_title="Exam", duration=1800):

    if not questions:
        st.warning("No questions available")
        return

    # =====================================================
    # EXAM INIT
    # =====================================================
    exam_key = exam_title

    if st.session_state.get("exam_id") != exam_key:
        st.session_state.exam_id = exam_key
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.current_question = 0
        st.session_state.start_time = time.time()

    st.session_state.setdefault("answers", {})
    st.session_state.setdefault("submitted", False)
    st.session_state.setdefault("current_question", 0)
    st.session_state.setdefault("start_time", time.time())

    # =====================================================
    # TITLE
    # =====================================================
    st.title(f"📝 {exam_title}")

    # =====================================================
    # TIMER
    # =====================================================
    st_autorefresh(interval=1000, key=f"timer_{exam_key}")

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(duration - elapsed, 0)

    st.markdown(f"## ⏱ Time Left: {remaining//30:02d}:{remaining%30:02d}")

    if remaining <= 0 and not st.session_state.submitted:
        st.session_state.submitted = True
        st.error("⏰ Time Over!")

    # =====================================================
    # CURRENT QUESTION
    # =====================================================
    total = len(questions)

    current = min(st.session_state.current_question, total - 1)
    st.session_state.current_question = current

    q = questions[current]

    q_type = q.get("type", "mcq")
    options = q.get("options", {})
    answer = q.get("answer", "")

    left, right = st.columns([3.5, 1.5])

    # =====================================================
    # QUESTION PANEL
    # =====================================================
    with left:

        st.markdown("---")
        st.markdown(f"### Question {current + 1} / {total}")

        st.write(q.get("question", ""))

        key = f"{exam_key}_{current}"

        # =====================================================
        # MCQ
        # =====================================================
        if q_type == "mcq":

            previous = st.session_state.answers.get(current, None)

            default_index = None

            if previous in options.keys():
                default_index = list(options.keys()).index(previous)

            ans = st.radio(
                "Select",
                list(options.keys()),
                format_func=lambda x: f"{x}. {options[x]}",
                key=key,
                index=default_index,
                disabled=st.session_state.submitted
            )

            st.session_state.answers[current] = ans

        # =====================================================
        # MSQ
        # =====================================================
        elif q_type == "msq":

            selected = st.session_state.answers.get(current, [])

            if not isinstance(selected, list):
                selected = []

            new_selected = []

            st.write("Select all correct options:")

            for k, v in options.items():

                checked = st.checkbox(
                    f"{k}. {v}",
                    value=k in selected,
                    key=f"{key}_{k}",
                    disabled=st.session_state.submitted
                )

                if checked:
                    new_selected.append(k)

            st.session_state.answers[current] = new_selected

        # =====================================================
        # NUMERICAL
        # =====================================================
        else:

            ans = st.text_input(
                "Answer",
                value=st.session_state.answers.get(current, ""),
                key=key,
                disabled=st.session_state.submitted
            )

            st.session_state.answers[current] = ans

        # =====================================================
        # SHOW RESULT AFTER SUBMIT
        # =====================================================
        if st.session_state.submitted:

            user = st.session_state.answers.get(current, "")

            if q_type == "msq":

                if set(user) == set(answer):
                    st.success("✔ Correct")
                else:
                    st.error(f"✖ Your Answer: {user}")
                    st.info(f"✔ Correct Answer: {answer}")

            else:

                try:
                    ok = float(user) == float(answer)
                except:
                    ok = str(user).strip() == str(answer).strip()

                if ok:
                    st.success("✔ Correct")
                else:
                    st.error(f"✖ Your Answer: {user}")
                    st.info(f"✔ Correct Answer: {answer}")

    # =====================================================
    # NAVIGATION PANEL
    # =====================================================
    with right:

        st.markdown("""
        <style>

        div.stButton > button {
            border-radius: 10px !important;
            font-weight: bold !important;
            border: 1px solid white !important;
            min-height: 45px !important;
        }

        </style>
        """, unsafe_allow_html=True)

        st.markdown("## 📍 Navigation")

        cols = st.columns(5)

        for i in range(total):

            col = cols[i % 5]

            is_current = (i == current)

            user_answer = st.session_state.answers.get(i, None)

            # =====================================================
            # ANSWER CHECK
            # =====================================================
            answered = False

            if isinstance(user_answer, list):
                answered = len(user_answer) > 0
            else:
                answered = user_answer not in [None, ""]

            # =====================================================
            # COLOR LOGIC
            # =====================================================
            if is_current:
                bg = "#ff2b2b"      # RED
            elif answered:
                bg = "#18a558"      # GREEN
            else:
                bg = "#111111"      # DARK

            # =====================================================
            # UNIQUE CSS FOR BUTTON
            # =====================================================
            st.markdown(f"""
            <style>

            div[data-testid="stButton"] button[kind="secondary"][id*="nav_{exam_key}_{i}"],
            div[data-testid="stButton"] button[kind="primary"][id*="nav_{exam_key}_{i}"] {{

                background: {bg} !important;
                color: white !important;
                border: 1px solid white !important;
                border-radius: 10px !important;
                font-weight: bold !important;
                min-height: 45px !important;
            }}

            </style>
            """, unsafe_allow_html=True)

            if col.button(
                f"{i+1}",
                key=f"nav_{exam_key}_{i}"
            ):
                st.session_state.current_question = i
                st.rerun()

        st.markdown("---")

        # =====================================================
        # PREV / NEXT
        # =====================================================
        c1, c2 = st.columns(2)

        with c1:
            if st.button("⬅ Prev") and current > 0:
                st.session_state.current_question -= 1
                st.rerun()

        with c2:
            if st.button("Next ➡") and current < total - 1:
                st.session_state.current_question += 1
                st.rerun()

        st.markdown("---")

        # =====================================================
        # SUBMIT
        # =====================================================
        if not st.session_state.submitted:

            if st.button("🚀 Submit", use_container_width=True):
                st.session_state.submitted = True
                st.rerun()

        # =====================================================
        # SCORE
        # =====================================================
        def calculate_score():

            score = 0

            for i, q in enumerate(questions):

                user = st.session_state.answers.get(i, "")
                correct = q.get("answer", "")
                q_type = q.get("type", "mcq")

                if q_type == "msq":

                    if set(user) == set(correct):
                        score += 1

                else:

                    try:
                        ok = float(user) == float(correct)
                    except:
                        ok = str(user).strip() == str(correct).strip()

                    if ok:
                        score += 1

            return score

        if st.session_state.submitted:

            st.success(
                f"🎯 Score: {calculate_score()}/{total}"
            )