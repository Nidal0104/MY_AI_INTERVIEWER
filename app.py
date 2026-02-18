import streamlit as st
from database import create_tables
from auth import register_user, login_user

create_tables()
st.set_page_config(page_title="AI Voice Interview Simulator", layout="wide")

# ---------------- CONSTANTS ----------------

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

# Dummy sample question (temporary until we reconnect engine)
SAMPLE_QUESTIONS = {
    "Teacher": "How would you handle a disruptive student in class?",
    "Lawyer": "How do you prepare for a high-profile court case?",
    "Corporate Software Engineer": "Explain the difference between multithreading and multiprocessing.",
    "Database Engineer": "What is normalization in databases?",
    "Civil Servant": "How would you handle public complaints effectively?",
    "Data Scientist": "Explain bias-variance tradeoff.",
    "AI Engineer": "What is overfitting in machine learning?",
    "Business Analyst": "How do you gather business requirements?",
    "Digital Marketer": "How would you improve conversion rate?"
}

# ---------------- SESSION INIT ----------------

if "user" not in st.session_state:
    st.session_state.user = None

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = None

# ---------------- TITLE ----------------

st.title("🎯 AI Voice Interview Simulator")

# =====================================================
# ================= AUTH SECTION ======================
# =====================================================

if st.session_state.user is None:

    page = st.radio("Select Option", ["Login", "Register"])

    # -------- LOGIN --------
    if page == "Login":
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

    # -------- REGISTER --------
    if page == "Register":
        st.subheader("Register")

        first_name = st.text_input("First Name *")
        last_name = st.text_input("Last Name *")
        email = st.text_input("Email *")
        password = st.text_input("Password *", type="password")

        if st.button("Create Account"):
            if not first_name or not last_name or not email or not password:
                st.error("All fields are required.")
            else:
                success = register_user({
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                    "phone": "N/A",
                    "age": 18,
                    "country": "N/A",
                    "city": "N/A",
                    "degree": "N/A",
                    "discipline": "N/A",
                    "certifications": ""
                })
                if success:
                    st.success("Account created. Please login.")
                else:
                    st.error("Email already exists.")

# =====================================================
# ================= DASHBOARD =========================
# =====================================================

else:

    st.success(f"Welcome {st.session_state.user['first_name']}")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.interview_started = False
        st.session_state.current_question = None
        st.rerun()

    st.divider()

    # Interview Settings
    job_role = st.selectbox("Select Job Role", JOB_ROLES)
    difficulty = st.selectbox("Select Difficulty", DIFFICULTY_LEVELS)
    time_per_question = st.selectbox("Time per Question (minutes)", TIME_OPTIONS)

    st.divider()

    # Start Interview
    if not st.session_state.interview_started:
        if st.button("Start Interview"):
            st.session_state.interview_started = True
            st.session_state.current_question = SAMPLE_QUESTIONS[job_role]
            st.rerun()

    # Interview Screen
    if st.session_state.interview_started:

        st.subheader("Interview Question")
        st.write(st.session_state.current_question)

        answer = st.text_area("Your Answer", height=150)

        if st.button("Submit Answer"):
            st.success("Answer submitted successfully.")

        if st.button("End Interview"):
            st.session_state.interview_started = False
            st.session_state.current_question = None
            st.rerun()
