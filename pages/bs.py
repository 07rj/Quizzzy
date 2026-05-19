import streamlit as st
import importlib
from structure import LEVELS
from engine.quiz_engine import run_exam

# =====================================================
# TITLE
# =====================================================
st.title("🎓 BS Level")

level = "bs"

subjects_map = LEVELS[level]["subjects"]
subjects = list(subjects_map.keys())

# =====================================================
# SAFE SESSION INIT
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
# RESET
# =====================================================
def reset():
    st.session_state.quiz = None
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.current_question = 0
    st.session_state.start_time = None


# =====================================================
# SUBJECT SELECTION
# =====================================================
if st.session_state.subject is None:

    st.subheader("Select Subject")

    for subject in subjects:

        if st.button(subjects_map[subject], key=f"sub_{subject}"):

            reset()
            st.session_state.subject = subject
            st.rerun()


# =====================================================
# QUIZ SELECTION
# =====================================================
if st.session_state.subject and st.session_state.quiz is None:

    subject = st.session_state.subject

    if st.button("⬅ Back"):
        st.session_state.subject = None
        reset()
        st.rerun()

    st.subheader(subjects_map[subject])

    quizzes = []

    for i in range(1, 100):

        quiz = f"quiz_{i}"
        module_path = f"questions.bs.{subject}.{quiz}"

        try:
            importlib.import_module(module_path)
            quizzes.append(quiz)
        except ModuleNotFoundError:
            break
        except Exception:
            continue

    for q in quizzes:

        if st.button(q, key=f"quiz_{q}"):

            st.session_state.quiz = q   # ✅ FIXED (was uiz)
            st.rerun()


# =====================================================
# LOAD QUESTIONS
# =====================================================
def load(subject, quiz):

    module = importlib.import_module(
        f"questions.bs.{subject}.{quiz}"
    )
    return getattr(module, "questions", [])


# =====================================================
# RUN EXAM
# =====================================================
if st.session_state.subject and st.session_state.quiz:

    questions = load(st.session_state.subject, st.session_state.quiz)

    if not questions:
        st.error(f"❌ No questions found for {st.session_state.quiz}")
        st.stop()

    run_exam(
        questions,
        f"{subjects_map[st.session_state.subject]} - {st.session_state.quiz}",
        duration=1800
    )