import streamlit as st
from structure import LEVELS
from loader import get_quiz, load_questions
from engine.quiz_engine import run_exam

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Quizzzy", layout="wide")
st.title("🎯 Quizzzy ")


# =====================================================
# INIT SESSION SAFE
# =====================================================
if "init" not in st.session_state:
    st.session_state.clear()
    st.session_state.init = True

defaults = {
    "level": None,
    "subject": None,
    "quiz": None
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)


# =====================================================
# RESET HELPERS
# =====================================================
def reset_subject():
    st.session_state.subject = None
    st.session_state.quiz = None


def reset_quiz():
    st.session_state.quiz = None


# =====================================================
# LEVEL SELECTION
# =====================================================
level = st.session_state.get("level")
level_data = LEVELS.get(level) if level else None

if level_data is None:

    st.subheader("📚 Select Level")

    for lvl, data in LEVELS.items():

        if st.button(data["name"], key=f"lvl_{lvl}"):

            st.session_state.level = lvl
            reset_subject()
            st.rerun()

    st.stop()


# =====================================================
# SUBJECT SELECTION
# =====================================================
subjects = level_data["subjects"]
subject = st.session_state.get("subject")

if subject not in subjects:

    st.subheader(f"📘 {level_data['name']}")

    for code, name in subjects.items():

        if st.button(name, key=f"sub_{code}"):

            st.session_state.subject = code
            reset_quiz()
            st.rerun()

    st.markdown("---")

    if st.button("⬅ Back to Levels"):

        st.session_state.level = None
        reset_subject()
        st.rerun()

    st.stop()


# =====================================================
# QUIZ SELECTION (NO SPLITTING LOGIC)
# =====================================================
subject_name = subjects[subject]
st.subheader(f"🧪 Subject: {subject_name}")

quiz = st.session_state.get("quiz")

available_quizzes = get_quiz(level, subject)

if quiz not in available_quizzes:

    if not available_quizzes:
        st.warning("You have to wait a little bit for this specific quiz")

    for q in available_quizzes:

        # display format
        parts = q.split(".")
        base = parts[0]           # quiz_1
        part = parts[1] if len(parts) > 1 else None

        display = f"Quiz {base.split('_')[1]}"
        if part:
            display += f" (Part {part.upper()})"

        if st.button(display, key=f"quiz_{q}"):

            st.session_state.quiz = q
            st.rerun()

    st.markdown("---")

    if st.button("⬅ Back to Cources"):

        st.session_state.subject = None
        reset_quiz()
        st.rerun()

    st.stop()


# =====================================================
# 🔥 FIX: USE FULL QUIZ NAME DIRECTLY
# =====================================================
questions = load_questions(level, subject, quiz)

if not questions:
    st.error("❌ No questions found")
    st.stop()


# =====================================================
# HEADER
# =====================================================
col1, col2 = st.columns([1, 4])

with col1:

    if st.button("⬅ Quiz List"):

        st.session_state.quiz = None
        st.rerun()

with col2:

    parts = quiz.split(".")
    base = parts[0]
    part = parts[1] if len(parts) > 1 else ""

    title = f"{level_data['name']} → {subject_name} → Quiz {base.split('_')[1]}"
    if part:
        title += f" (Part {part.upper()})"

    st.markdown(f"### 🎯 {title}")


# =====================================================
# RUN EXAM
# =====================================================
run_exam(
    questions,
    title,
    duration=1800
)