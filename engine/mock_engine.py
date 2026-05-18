import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh


def run_exam(questions, subject_name="Exam", duration=1800):

    # ---------------- INIT ----------------
    st.title(f"📝 {subject_name}")

    # Reset when new subject opens
    if "active_subject" not in st.session_state:
        st.session_state.active_subject = subject_name

    if st.session_state.active_subject != subject_name:
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.start_time = time.time()
        st.session_state.current_question = 0
        st.session_state.active_subject = subject_name

    # ---------------- SESSION STATE ----------------
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    # ---------------- TIMER ----------------
    st_autorefresh(interval=1000, key="timer_refresh")

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(duration - elapsed, 0)

    minutes = remaining // 30
    seconds = remaining % 30
    st.markdown("## ⏱ TIMER")
    st.markdown(f"### 🟢 {minutes:02d}:{seconds:02d}")

    # ---------------- LAYOUT ----------------
    left, right = st.columns([3.5, 1.5])

    # =========================================================
    # LEFT SIDE
    # =========================================================
    with left:

        for index, q in enumerate(questions):

            st.markdown("---")

            # Highlight current question
            if index == st.session_state.current_question:
                st.markdown(f"### 👉 Question {index + 1}")
            else:
                st.markdown(f"### Question {index + 1}")

            st.write(q["question"])

            key = f"{subject_name}_{index}"

            # ---------------- MCQ ----------------
            if q["type"] == "mcq":

                options = q["options"]

                selected = st.radio(
                    "Select option:",
                    list(options.keys()),
                    format_func=lambda x: f"{x}. {options[x]}",
                    key=key,
                    disabled=st.session_state.submitted
                )

                st.session_state.answers[index] = selected

            # ---------------- MSQ ----------------  
            elif q["type"] == "msq":

                options = q["options"]
                selected = []
    
                st.write("Select all correct options:")
                
                for opt_key, opt_val in options.items():
                     if st.checkbox(f"{opt_key}. {opt_val}", key=f"{key}_{opt_key}"):
                         selected.append(opt_key)
    
                st.session_state.answers[index] = selected

            # ---------------- NUMERICAL ----------------
            else:

                ans = st.text_input(
                    "Answer:",
                    key=key,
                    disabled=st.session_state.submitted
                )
                st.session_state.answers[index] = ans

            # ---------------- RESULT ----------------
            if st.session_state.submitted:

                user_ans = st.session_state.answers.get(index, "")
                correct_ans = q["answer"]

                st.markdown("#### Result:")

                if q["type"] == "msq":
                    if set(user_ans) == set(correct_ans):
                        st.success(f"✔ Correct: {correct_ans}")
                    else:
                        st.error(f"✖ Your Answer: {user_ans}")
                        st.success(f"✔ Correct: {correct_ans}")

                else:
                    if str(user_ans) == str(correct_ans):
                        st.success(f"✔ Correct: {correct_ans}")
                    else:
                        st.error(f"✖ Your Answer: {user_ans}")
                        st.success(f"✔ Correct: {correct_ans}")

    # =========================================================
    # RIGHT SIDE (PANEL)
    # =========================================================
    with right:

        st.markdown("## ⏱ TIMER")
        st.markdown(f"### {minutes:02d}:{seconds:02d}")

        st.markdown("---")
        st.markdown("## 📍Question:")

        cols = st.columns(5)

        for i in range(len(questions)):

            col = cols[i % 5]

            status = st.session_state.answers.get(i, None)

            # button color logic
            if i == st.session_state.current_question:
                style = "primary"
            elif status:
                style = "secondary"
            else:
                style = "secondary"

            if col.button(f"{i+1}", key=f"nav_{i}", type=style):

                st.session_state.current_question = i
                st.rerun()

        st.markdown("---")

        # ---------------- SUBMIT ----------------
        if st.button("🚀 SUBMIT TEST", use_container_width=True):

            st.session_state.submitted = True
            score = 0

            for i, q in enumerate(questions):

                user_ans = st.session_state.answers.get(i, "")

                if q["type"] == "msq":
                    if set(user_ans) == set(q["answer"]):
                        score += 1
                else:
                    if str(user_ans) == str(q["answer"]):
                        score += 1

            st.success(f"🎯 SCORE: {score}/{len(questions)}")