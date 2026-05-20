import streamlit as st
from structure import LEVELS
from loader import get_quiz, load_questions
from engine.quiz_engine import run_exam

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Quizzzy", layout="wide")

# =====================================================
# 🌌 STRONG DENSE TWINKLING STAR BACKGROUND (UPGRADED)
# =====================================================
st.markdown("""
<style>

/* BACKGROUND BASE */
.stApp {
    background: radial-gradient(circle at bottom, #02040f 0%, #000000 100%);
}

/* ⭐ STAR FIELD (DENSE + STRONG) */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 250%;
    height: 250%;
    background-image:
        radial-gradient(2px 2px at 5% 10%, white, transparent),
        radial-gradient(1px 1px at 15% 25%, white, transparent),
        radial-gradient(2px 2px at 25% 40%, white, transparent),
        radial-gradient(1px 1px at 35% 60%, white, transparent),
        radial-gradient(2px 2px at 45% 80%, white, transparent),
        radial-gradient(1px 1px at 55% 20%, white, transparent),
        radial-gradient(2px 2px at 65% 35%, white, transparent),
        radial-gradient(1px 1px at 75% 55%, white, transparent),
        radial-gradient(2px 2px at 85% 75%, white, transparent),
        radial-gradient(1px 1px at 95% 90%, white, transparent);
    animation: moveStars 70s linear infinite;
    opacity: 0.95;
    z-index: -1;
}

/* TWINKLE LAYER (MORE STARS) */
.stApp::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 250%;
    height: 250%;
    background-image:
        radial-gradient(1px 1px at 10% 15%, white, transparent),
        radial-gradient(1px 1px at 30% 35%, white, transparent),
        radial-gradient(1px 1px at 50% 55%, white, transparent),
        radial-gradient(1px 1px at 70% 75%, white, transparent),
        radial-gradient(1px 1px at 90% 95%, white, transparent);
    animation: twinkle 2s infinite alternate;
    opacity: 0.8;
    z-index: -1;
}

/* ANIMATIONS */
@keyframes moveStars {
    from {transform: translateY(0);}
    to {transform: translateY(-2500px);}
}

@keyframes twinkle {
    from {opacity: 0.3;}
    to {opacity: 1;}
}

/* TEXT */
* {
    font-weight: 600;
    color: white;
}

/* BUTTON */
div.stButton > button {
    width: 100%;
    padding: 24px;
    border: 1px solid white !important;
    border-radius: 22px !important;
    background: transparent;
    font-size: 26px;
}

div.stButton > button:hover {
    border: 1px solid #4F8BF9 !important;
    transform: scale(1.02);
    transition: 0.2s;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# INIT STATE
# =====================================================
if "init" not in st.session_state:
    st.session_state.clear()
    st.session_state.init = True

for k in ["level", "subject", "quiz"]:
    st.session_state.setdefault(k, None)

st.title("🎯 Quizzzy")

# =====================================================
# RESET HELPERS
# =====================================================
def reset_subject():
    st.session_state.subject = None
    st.session_state.quiz = None

def reset_quiz():
    st.session_state.quiz = None

# =====================================================
# LEVEL PAGE
# =====================================================
level = st.session_state.get("level")
level_data = LEVELS.get(level) if level else None

if level_data is None:

    st.markdown("## 📚 Select Level")

    # ⭐ WELCOME BACK (FIXED)
    st.markdown("""
    <div style="text-align:center; margin-top:30px; margin-bottom:50px;">
        <h1 style="color:#4F8BF9; font-size:80px;">
            🎯 Welcome to Quizzzy
        </h1>
        <h3 style="color:lightgray;">
            Quizzes for Data Science Students
        </h3>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(LEVELS))

    for i, (lvl, data) in enumerate(LEVELS.items()):
        with cols[i]:
            if st.button(data["name"], key=f"lvl_{lvl}", use_container_width=True):
                st.session_state.level = lvl
                reset_subject()
                st.rerun()

    st.stop()

# =====================================================
# SUBJECT PAGE
# =====================================================
subjects = level_data["subjects"]
subject = st.session_state.get("subject")

if subject not in subjects:

    st.subheader(f" {level_data['name']}")

    for code, name in subjects.items():
        if st.button(name, key=f"sub_{code}", use_container_width=True):
            st.session_state.subject = code
            reset_quiz()
            st.rerun()

    if st.button("⬅ Back to Levels"):
        st.session_state.level = None
        reset_subject()
        st.rerun()

    st.stop()

# =====================================================
# QUIZ PAGE (UNCHANGED LOGIC)
# =====================================================
subject_name = subjects[subject]
st.subheader(f"🧪 {subject_name}")

quizzes = get_quiz(level, subject)

if not quizzes:
    st.warning("No quizzes available")
    st.stop()

quiz = st.session_state.get("quiz")

if not quiz:

    if st.button("⬅ Back to Courses"):
        st.session_state.subject = None
        st.session_state.quiz = None
        st.rerun()

    st.markdown("##  Select Quiz")

    for q in quizzes:

        base = q.split(".")[0]
        part = q.split(".")[1] if "." in q else ""

        quiz_num = base.split("_")[1]
        label = f"Quiz {quiz_num}"
        if part:
            label += f" (Part {part.upper()})"

        if st.button(f"{subject_name} → {label}", key=f"quiz_{q}", use_container_width=True):
            st.session_state.quiz = q
            st.rerun()

    st.stop()

# =====================================================
# EXAM PAGE
# =====================================================
questions = load_questions(level, subject, quiz)

base = quiz.split(".")[0]
part = quiz.split(".")[1] if "." in quiz else ""

title = f"{level_data['name']} - {subject_name} - Quiz {base.split('_')[1]}"
if part:
    title += f" (Part {part.upper()})"

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("⬅ Back to Quiz List"):
        st.session_state.quiz = None
        st.rerun()

with col2:
    st.markdown(f"### 🎯 {title}")

run_exam(questions, title, duration=1800)




# git status
# git add .git commit -m "Fix quiz system: support quiz_1.a format without merging quizzes"
# git push origin main
