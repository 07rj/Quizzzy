import streamlit as st
import time
import importlib
from structure import LEVELS
from engine.mock_engine import run_exam

st.title("🎓 BS Level")

# ---------------- SUBJECT CONFIG ----------------
subjects_map = LEVELS["bs"]["subjects"]
subjects = list(subjects_map.keys())

# ---------------- SAFE SESSION INIT ----------------
defaults = {
    "subject": None,
    "mock": None,
    "active_exam": None,
    "answers": {},
    "submitted": False,
    "current_question": 0,
    "start_time": None
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)


# ---------------- RESET FUNCTION ----------------
def reset():
    st.session_state.mock = None
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.current_question = 0
    st.session_state.start_time = None


# ---------------- SUBJECT SELECTION ----------------
if st.session_state.subject is None:

    st.subheader("Select Subject")

    for subject in subjects:

        if st.button(subjects_map[subject], key=f"sub_{subject}"):

            reset()
            st.session_state.subject = subject
            st.rerun()


# ---------------- MOCK SELECTION ----------------
if st.session_state.subject and st.session_state.mock is None:

    if st.button("⬅ Back"):
        st.session_state.subject = None
        reset()
        st.rerun()

    st.subheader(subjects_map[st.session_state.subject])

    for i in range(1, 100):

        mock = f"mock_{i}"
        module_path = f"questions.bs.{st.session_state.subject}.{mock}"

        try:
            importlib.import_module(module_path)

            if st.button(mock, key=f"mock_{mock}"):
                st.session_state.mock = mock
                st.rerun()

        except ModuleNotFoundError:
            break
        except Exception:
            continue


# ---------------- LOAD QUESTIONS ----------------
def load(subject, mock):
    module = importlib.import_module(
        f"questions.bs.{subject}.{mock}"
    )
    return getattr(module, "questions", [])


# ---------------- EXAM ----------------
if st.session_state.subject and st.session_state.mock:

    # ❌ REMOVED AUTO RESET BUG (was breaking app)

    questions = load(st.session_state.subject, st.session_state.mock)

    if not questions:
        st.error("No questions found")
        st.stop()

    run_exam(
        questions,
        f"{subjects_map[st.session_state.subject]} - {st.session_state.mock}",
        duration=1800
    )