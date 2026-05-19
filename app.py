import streamlit as st
from structure import LEVELS
from loader import get_mocks, load_questions
from engine.mock_engine import run_exam

# =====================================================
# PAGE
# =====================================================
st.set_page_config(page_title="Quizzzy", layout="wide")
st.title("🎯 Quizzzy Exam System")

# =====================================================
# CLEAR OLD BROKEN SESSION ON FIRST RUN
# =====================================================
if "app_initialized" not in st.session_state:
    st.session_state.clear()
    st.session_state.app_initialized = True

# =====================================================
# SAFE SESSION STATE
# =====================================================
defaults = {
    "level": None,
    "subject": None,
    "mock": None
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# =====================================================
# RESET HELPERS
# =====================================================
def reset_subject():
    st.session_state.subject = None
    st.session_state.mock = None


def reset_mock():
    st.session_state.mock = None


# =====================================================
# SAFE LEVEL
# =====================================================
level = st.session_state.get("level")
level_data = LEVELS.get(level) if level else None

# =====================================================
# LEVEL PAGE
# =====================================================
if level_data is None:

    st.subheader("📚 Select Level")

    for level_key, data in LEVELS.items():

        if st.button(data["name"], key=f"lvl_{level_key}"):

            st.session_state.level = level_key
            reset_subject()
            st.rerun()

    st.stop()

# =====================================================
# SUBJECT PAGE
# =====================================================
subjects = level_data.get("subjects", {})

subject = st.session_state.get("subject")

if subject not in subjects:

    st.subheader(f"📘 {level_data['name']}")

    for subject_code, subject_name in subjects.items():

        if st.button(subject_name, key=f"sub_{subject_code}"):

            st.session_state.subject = subject_code
            reset_mock()
            st.rerun()

    # BACK TO LEVELS
    st.markdown("---")

    if st.button("⬅ Back to Levels"):

        st.session_state.level = None
        reset_subject()
        st.rerun()

    st.stop()

# =====================================================
# MOCK PAGE
# =====================================================
subject_name = subjects[subject]

st.subheader(f"🧪 Subject: {subject_name}")

mock = st.session_state.get("mock")

available_mocks = get_mocks(level, subject)

if mock not in available_mocks:

    if not available_mocks:
        st.warning("No mocks found")

    for m in available_mocks:

        if st.button(m, key=f"mock_{m}"):

            st.session_state.mock = m
            st.rerun()

    # BACK TO SUBJECTS
    st.markdown("---")

    if st.button("⬅ Back to Subjects"):

        st.session_state.subject = None
        reset_mock()
        st.rerun()

    st.stop()

# =====================================================
# EXAM PAGE
# =====================================================
questions = load_questions(level, subject, mock)

if not questions:

    st.error("❌ No questions found")
    st.stop()

# =====================================================
# EXAM TOP BAR
# =====================================================
col1, col2, col3 = st.columns([1, 4, 1])

with col1:

    # BACK TO MOCKS
    if st.button("⬅ Mocks"):

        st.session_state.mock = None
        st.rerun()

with col2:

    st.markdown(
        f"### 🎯 {level_data['name']} → {subject_name} → {mock}"
    )

# =====================================================
# RUN EXAM
# =====================================================
title = f"{level_data['name']} - {subject_name} - {mock}"

run_exam(
    questions,
    title,
    duration=1800
)







  
   
