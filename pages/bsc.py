import streamlit as st
import time
from engine.mock_engine import run_exam

st.title(" 📜 BSc Leve")

subjects = [ "Intro To Big Data",
            "Large Language Module",
            "Programming in C"
   
]

# ---------------- SESSION STATE ----------------
if "subject" not in st.session_state:
    st.session_state.subject = None

if "active_exam" not in st.session_state:
    st.session_state.active_exam = None

#  SUBJECT BUTTONS :
for subject in subjects:

    if st.button(subject, key = subject):

        st.session_state.subject = subject

        # RESET ENGINE STATE FOR NEW SUBJECT
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.current_question = 0
        st.session_state.start_time = time.time()

        # SAVE ACTIVE SUBJECT
        st.session_state.active_exam = subject

#  QUESTIONS :
questions = [
    {
    "type": "mcq",
    "question": "What is 2 + 2?",
    "options": {
        "A":  "1",
        "B":  "2",
        "C":  "3",
        "D":  "4"
    },
    "answer": "D"
},

    {
        "type": "numerical",
        "question": "What is 10 / 2?",
        "answer": "5"
},

    {
    "type": "msq",
    "question": "Select even numbers",
    "options": {
        "A":  "1",
        "B":  "2",
        "C":  "4",
        "D":  "5"
    },
    "answer": ["B", "C"]
}

]

# OPEN ENGINE :
if st.session_state.subject:
    run_exam(
        questions,
        st.session_state.subject,
        duration=1800
    )