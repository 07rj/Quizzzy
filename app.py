import streamlit as st

st.set_page_config(page_title="Quizzy", layout="wide")

st.title("🎯 Quizzzy")
st.subheader("Select Your Level")

#  INIT FIRST
if "page" not in st.session_state:
    st.session_state.page = None


# LEVEL BUTTONS
if st.button("Foundation"):
    st.session_state.page = "foundation"

if st.button("Diploma in Programming"):
    st.session_state.page = "Diploma in Programming"

if st.button("Diploma in Data Science"):
    st.session_state.page = "Diploma in Data Science"

if st.button("BSc Level"):
    st.session_state.page = "BSc"

if st.button("BS Level"):
    st.session_state.page = "Bs"


# SHOW PAGES
if st.session_state.page == "foundation":
    import pages.foundation

elif st.session_state.page == "Diploma in Programming":
    import pages.diploma_in_programming

elif st.session_state.page == "Diploma in Data Science":
    import pages.diploma_in_data_science

elif st.session_state.page == "BSc":
    import pages.bsc

elif st.session_state.page == "Bs":
    import pages.bs  



  
   
