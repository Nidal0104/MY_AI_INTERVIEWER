import streamlit as st
from database import create_tables
from auth import register_user, login_user

create_tables()

st.set_page_config(page_title="AI Voice Interview Simulator", layout="wide")

# ------------------ CONSTANT DATA ------------------

JOB_ROLES = [
    "Teacher",
    "Lawyer",
    "Corporate Software Engineer",
    "Database Engineer",
    "Civil Servant",
    "Data Scientist",
    "AI Engineer",
    "Business Analyst",
    "Digital Marketer"
]

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
TIME_OPTIONS = [1, 2, 3, 5]

# ------------------ SESSION INIT ------------------

if "user" not in st.session_state:
    st.session_state.user = None

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

# ------------------ TITLE ------------------

st.title("🎯 AI Voice Interview Simulator")

# =====================================================
# ================= AUTH SECTION ======================
# =====================================================

if st.session_state.user is None:

    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.success("Logged in successfully.")
            st.rerun()
        else:
            st.error("Invalid credentials.")

# =====================================================
# ================= DASHBOARD =========================
# =====================================================

else:

    st.success(f"Welcome {st.session_state.user['first_name']}")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.interview_started = False
        st.rerun()

    st.divider()

    st.subheader("Interview Settings")

    job_role = st.selectbox("Select Job Role", JOB_ROLES)
    difficulty = st.selectbox("Select Difficulty Level", DIFFICULTY_LEVELS)
    time_per_question = st.selectbox("Time per Question (minutes)", TIME_OPTIONS)

    st.divider()

    if not st.session_state.interview_started:
        if st.button("Start Interview"):
            st.session_state.interview_started = True
            st.rerun()

    if st.session_state.interview_started:
        st.success("Interview Started!")

        st.write(f"Role: {job_role}")
        st.write(f"Difficulty: {difficulty}")
        st.write(f"Time per question: {time_per_question} minute(s)")

        answer = st.text_area("Your Answer", height=150)

        if st.button("Submit Answer"):
            st.info("Answer submitted. (Evaluation will be connected here)")

        if st.button("End Interview"):
            st.session_state.interview_started = False
            st.rerun()
