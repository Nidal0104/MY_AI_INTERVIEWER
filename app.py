import streamlit as st
from database import create_tables
from auth import register_user, login_user
from interview_engine import generate_question
from evaluation_engine import evaluate_answer
from analytics import generate_radar_chart
from voice_utils import speech_to_text, text_to_speech
import time

create_tables()

st.set_page_config(page_title="AI Interview Simulator", layout="wide")

JOB_ROLES = [
    "Teacher", "Lawyer", "Corporate Software Engineer",
    "Database Engineer", "Civil Servant",
    "Data Scientist", "AI Engineer",
    "Business Analyst", "Digital Marketer"
]

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎯 AI Voice Interview Simulator")

# AUTH SECTION
if not st.session_state.user:
    option = st.sidebar.selectbox("Select", ["Login", "Register"])

    if option == "Register":
        with st.form("register"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            phone = st.text_input("Phone")
            age = st.number_input("Age")
            address = st.text_input("Address")
            degree = st.text_input("Last Degree")
            certifications = st.text_area("Certifications")

            submitted = st.form_submit_button("Register")

            if submitted:
                success = register_user({
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                    "phone": phone,
                    "age": age,
                    "address": address,
                    "degree": degree,
                    "certifications": certifications
                })
                if success:
                    st.success("Account created. Please login.")
                else:
                    st.error("User already exists.")

    if option == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully.")
                st.rerun()
            else:
                st.error("Invalid credentials")

else:
    st.sidebar.success(f"Welcome {st.session_state.user['first_name']}")
    job_role = st.sidebar.selectbox("Select Job Role", JOB_ROLES)

    if st.button("Start Interview"):
        st.session_state.interview_active = True
        st.session_state.question_count = 0
        st.session_state.total_score = 0

    if st.session_state.get("interview_active"):

        difficulty = "medium"
        question = generate_question(job_role, st.session_state.user, difficulty)

        st.subheader("Interview Question")
        st.write(question)

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):
            evaluation = evaluate_answer(question, answer, job_role)

            st.write("### AI Feedback")
            st.write(evaluation["overall_feedback"])

            st.write("### Improved Answer")
            st.write(evaluation["improved_answer"])

            st.session_state.total_score += evaluation["score"]

            fig = generate_radar_chart(evaluation)
            st.plotly_chart(fig)

            if evaluation["hire_recommendation"] == "pass":
                st.success("🎉 Interview Passed")
            else:
                st.error("❌ Interview Failed")

            st.session_state.interview_active = False
