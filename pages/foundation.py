import streamlit as st
from structure import LEVELS
from loader import get_quiz, load_questions
from engine.quiz_engine import run_exam

# =====================================================
# PAGE
# =====================================================
st.set_page_config(page_title="Foundation", layout="wide")
st.title("🏅 Foundation")


# =====================================================
# INIT STATE (SAFE)
# =====================================================
defaults = {
    "subject": None,
    "quiz": None,
    "answers": {},
    "submitted": False,
    "current_question": 0,
    "start_time": None,
    "active_exam": None
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)


# =====================================================
# RESET FUNCTION
# =====================================================
def reset():
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.current_question = 0
    st.session_state.start_time = None
    st.session_state.active_exam = None


# =====================================================
# LEVEL
# =====================================================
level = "foundation"

level_data = LEVELS.get(level)

if not level_data:
    st.error("Invalid level")
    st.stop()

subjects = level_data.get("subjects", {})


# =====================================================
# STEP 1 — SUBJECT SELECTION
# =====================================================
st.subheader("📘 Select Subject")

for code, name in subjects.items():

    if st.button(name, key=f"sub_{code}"):

        st.session_state.subject = code
        st.session_state.quiz = None
        reset()
        st.rerun()

if st.session_state.subject is None:
    st.stop()

subject = st.session_state.subject
subject_name = subjects.get(subject, "Unknown Subject")

st.subheader(f"🧪 Subject: {subject_name}")


# =====================================================
# STEP 2 — QUIZ DETECTION
# =====================================================
quizzes = get_quiz(level, subject)

if not quizzes:
    st.warning("No quizzes found in folder")
    st.stop()


# =====================================================
# STEP 3 — QUIZ SELECTION UI (FIXED CLEAN VERSION)
# =====================================================
for q in quizzes:

    parts = q.split(".")     # quiz_1.a → ['quiz_1', 'a']
    base = parts[0]          # quiz_1
    part = parts[1] if len(parts) > 1 else None

    quiz_number = base.split("_")[1]

    display = f"Quiz {quiz_number}"

    if part:
        display += f" (Part {part.upper()})"

    if st.button(display, key=f"quiz_{q}"):

        st.session_state.quiz = q
        st.rerun()

if st.session_state.quiz is None:
    st.stop()

quiz = st.session_state.quiz


# =====================================================
# FINAL SAFETY CHECK
# =====================================================
if not subject or not quiz:
    st.stop()


# =====================================================
# LOAD QUESTIONS (FIXED LOADER USAGE)
# =====================================================
questions = load_questions(level, subject, quiz)

if not questions:
    st.error(f"❌ No questions found for {quiz}")
    st.stop()


# =====================================================
# TITLE
# =====================================================
title = f"Foundation - {subject_name} - {quiz}"


# =====================================================
# RUN EXAM
# =====================================================
run_exam(
    questions,
    title,
    duration=1800
)