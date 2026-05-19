import streamlit as st
import time
from engine.mock_engine import run_exam
import importlib

mock = importlib.import_module("questions.foundation.maths_1.mock_1")
questions = mock.questions

st.title("🏅 Foundation")

if "subject" not in st.session_state:
    st.session_state.subject = None

if "page" not in st.session_state:
    st.session_state.page = "home"

subjects = [
    "Maths 1",
    "Maths 2",
    "Statistics 1",
    "Statistics 2",
    "English 1",
    "English 2",
    "Computational Thinking",
    "Programming in Python"
]

#  SESSION STATE :
if "subject" not in st.session_state:
    st.session_state.subject = None

if "active_exam" not in st.session_state:
    st.session_state.active_exam = None

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None


#  SUBJECT BUTTONS :
for subject in subjects:

    if st.button(subject, key=subject):

        # reset only when switching subject
        if st.session_state.get("active_exam") != subject:
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.current_question = 0
            st.session_state.start_time = time.time()

        st.session_state.subject = subject
        st.session_state.active_exam = subject

        st.rerun()   


#  RUN ENGINE :
if st.session_state.get("subject"):

    run_exam(
        questions,
        st.session_state.subject,
        duration=1800
    )