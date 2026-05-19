import streamlit as st

from engine.mock_engine import run_exam


st.set_page_config(page_title="Quizzzy", layout="wide")

st.title("🎯 Quizzzy")
st.subheader("Select Your Level")

#  INITIAL STATE :
if "page" not in st.session_state:
    st.session_state.page = "home"

if "level" not in st.session_state:
    st.session_state.level = None

if "subject" not in st.session_state:
    st.session_state.subject = None


#  LEVEL PAGE :
if st.session_state.page == "home":

    if st.button("Foundation"):
        st.session_state.level = "foundation"
        st.session_state.page = "subjects"
        st.rerun()

    if st.button("Diploma in Programming"):
        st.session_state.level = "diploma_prog"
        st.session_state.page = "subjects"
        st.rerun()

    if st.button("Diploma in Data Science"):
        st.session_state.level = "diploma_ds"
        st.session_state.page = "subjects"
        st.rerun()

    if st.button("BSc Level"):
        st.session_state.level = "bsc"
        st.session_state.page = "subjects"
        st.rerun()

    if st.button("BS Level"):
        st.session_state.level = "bs"
        st.session_state.page = "subjects"
        st.rerun()


#  SUBJECT COURSE :
elif st.session_state.page == "subjects":

    st.title(f"Level: {st.session_state.level}")

    subjects_map = {
    "foundation": ["Maths 1", "Maths 2", "English 1", "English 2", "Statistics 1", " Statistics 2",
                   "Programming in Python", "Computational Thinking"],

    "diploma_prog": ["PDSA using Python", "Database Management System", "MOdern Application Development 1", 
                     "Modern Application Development 2", "Programming Concepts Using JAVA", 
                     "System commands"],

    "diploma_ds": ["Machine Learning Foundation", "Machine Learning Techniques", "Machine Learning Practice",
                    "Business Data Management", "Tools in Data Science", "Business Data Analytics", 
                    "Introduction to Deep Learning and Generative Ai"],

    "bsc": ["Intro To Big Data", "Large Language Models", " Programming in C"],

    "bs": ["Software Engineering", "Software Testing", "Ai : Search Method", " Deep Learning"]
}

    subjects = subjects_map.get(st.session_state.level, [])

    if st.button("⬅ Back to Levels"):
        st.session_state.page = "home"
        st.session_state.level = None
        st.rerun()

    st.markdown("---")

    for sub in subjects:

        if st.button(sub, key=sub):

            st.session_state.subject = sub
            st.session_state.page = "exam"
            st.rerun()


#  EXAM PAGE :
elif st.session_state.page == "exam":

    st.title(f"Course : {st.session_state.subject}")

    if st.button("⬅ Back to Courses"):
        st.session_state.page = "subjects"
        st.session_state.subject = None
        st.rerun()

    # IMPORT QUESTIONS ONLY HERE (safe)
    from questions.foundation.maths_1.mock_1 import questions

    run_exam(
        questions,
        st.session_state.subject,
        duration=1800
    )



  
   
