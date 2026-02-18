import streamlit as st
from database import create_tables
from auth import register_user, login_user
import time

create_tables()

st.set_page_config(page_title="AI Voice Interview Simulator", layout="wide")

# ---------------- DATA ----------------

COUNTRIES_CITIES = {
    "Pakistan": ["Karachi","Lahore","Islamabad","Rawalpindi","Faisalabad","Multan","Peshawar","Quetta","Sialkot","Gujranwala","Bahawalpur","Hyderabad","Sukkur","Abbottabad","Mardan"],
    "India": ["Mumbai","Delhi","Bangalore","Hyderabad","Ahmedabad","Chennai","Kolkata","Pune","Jaipur","Lucknow","Kanpur","Nagpur","Indore","Thane","Bhopal"],
    "Saudi Arabia": ["Riyadh","Jeddah","Mecca","Medina","Dammam","Khobar","Tabuk","Abha","Hail","Jazan","Al Kharj","Al Qatif","Taif","Najran","Yanbu"],
    "England": ["London","Manchester","Birmingham","Leeds","Glasgow","Sheffield","Liverpool","Bristol","Newcastle","Leicester","Coventry","Nottingham","Hull","Bradford","Cardiff"]
}

DEGREES_DISCIPLINES = {
    "Matric": ["Science","Arts","Commerce"],
    "Inter": ["Pre-Medical","Pre-Engineering","Commerce","Arts"],
    "Bachelors": ["Computer Science","Electrical Engineering","Mechanical Engineering","Business Administration","Economics","Physics","Mathematics","Biology","Law","Political Science","Marketing","Finance","Psychology","English","Chemistry"],
    "Masters": ["Computer Science","Electrical Engineering","Business Administration","Economics","Physics","Mathematics","Biology","Law","Political Science","Marketing","Finance","Psychology","English","Chemistry"],
    "MPhil": ["Computer Science","Economics","Physics","Mathematics","Biology","Law","Political Science","Business Administration","Psychology","English","Chemistry"],
    "PhD": ["Computer Science","Economics","Physics","Mathematics","Biology","Law","Political Science","Business Administration","Psychology","English","Chemistry"]
}

AGES = list(range(15, 66))

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
TIME_OPTIONS = [1, 2, 3, 5]  # minutes per question

# ---------------- SESSION INIT ----------------

if "user" not in st.session_state:
    st.session_state.user = None

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

st.title("🎯 AI Voice Interview Simulator")

# ---------------- AUTH ----------------

if not st.session_state.user:

    option = st.sidebar.selectbox("Select", ["Login", "Register"])

    # REGISTER
    if option == "Register":
        with st.form("register"):
            st.subheader("Create a new account")

            first_name = st.text_input("First Name *")
