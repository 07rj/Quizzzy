import streamlit as st
import importlib
from structure import LEVELS
from engine.mock_engine import run_exam

st.set_page_config(page_title="Foundation", layout="wide")
st.title("🏅 Foundation")

# =====================================================
# INIT STATE (SAFE)
# =====================================================
defaults = {
    "subject": None,
    "mock": None,
    "answers": {},
    "submitted": False,
    "current_question": 0,
    "start_time": None,
    "active_exam": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


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
# SAFE LEVEL ACCESS (FIXED)
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
        st.session_state.mock = None
        reset()
        st.rerun()

if st.session_state.subject is None:
    st.stop()

subject = st.session_state.subject


# =====================================================
# SAFE SUBJECT NAME
# =====================================================
subject_name = subjects.get(subject, "Unknown Subject")
st.subheader(f"🧪 Subject: {subject_name}")


# =====================================================
# STEP 2 — MOCK DETECTION (FIXED)
# =====================================================
mocks = []

for i in range(1, 100):
    mock = f"mock_{i}"
    module_path = f"questions.{level}.{subject}.{mock}"

    try:
        importlib.import_module(module_path)
        mocks.append(mock)
    except ModuleNotFoundError:
        break
    except Exception:
        continue


for m in mocks:
    if st.button(m, key=f"mock_{m}"):
        st.session_state.mock = m
        st.rerun()

if st.session_state.mock is None:
    st.stop()

mock = st.session_state.mock


# =====================================================
# FINAL SAFETY CHECK
# =====================================================
if not subject or not mock:
    st.stop()


# =====================================================
# LOAD QUESTIONS (SAFE)
# =====================================================
module_path = f"questions.{level}.{subject}.{mock}"

module = importlib.import_module(module_path)
questions = getattr(module, "questions", [])


if not questions:
    st.error("No questions found")
    st.stop()


# =====================================================
# TITLE
# =====================================================
title = f"Foundation - {subject_name} - {mock}"


# =====================================================
# RUN EXAM
# =====================================================
run_exam(
    questions,
    title,
    duration=1800
)