import streamlit as st
from database import create_tables
from auth import register_user, login_user

create_tables()

st.set_page_config(page_title="AI Voice Interview Simulator", layout="wide")

# Constants
JOB_ROLES = [
    "Teacher", "Lawyer", "Corporate Software Engineer", "Database Engineer", "Civil Servant", "Data Scientist", "AI Engineer", "Business Analyst", "Digital Marketer"
]

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
TIME_OPTIONS = [1, 2, 3, 5]

# Session State Init
if "user" not in st.session_state:
    st.session_state.user = None

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = None

st.title("🎯 AI Voice Interview Simulator")

# Authentication Section
if st.session_state.user is None:
    st.subheader("Login / Register")
    
    page = st.radio("Select Option", ["Login", "Register"])
    
    if page == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    
    if page == "Register":
        st.subheader("Register")
        
        first_name = st.text_input("First Name *")
        last_name = st.text_input("Last Name *")
        email = st.text_input("Email *")
        password = st.text_input("Password *", type="password")
        phone = st.text_input("Cell Number *")
        age = st.selectbox("Age *", list(range(15, 66)))
        country = st.selectbox("Country *", ["Pakistan", "India", "Saudi Arabia", "England"])
        city = st.selectbox("City *", [])  # City will be updated dynamically
        degree = st.selectbox("Last Completed Degree *", ["Matric", "Inter", "Bachelors", "Masters", "MPhil", "PhD"])
        discipline = st.selectbox("Program / Discipline *", [])  # Discipline will update based on degree
        certifications = st.text_area("Certifications (if any)")
        
        # Dynamic City and Discipline Logic
        country_cities = {
            "Pakistan": ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Sialkot", "Gujranwala", "Bahawalpur", "Hyderabad", "Sukkur", "Abbottabad", "Mardan"],
            "India": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal"],
            "Saudi Arabia": ["Riyadh", "Jeddah", "Mecca", "Medina", "Dammam", "Khobar", "Tabuk", "Abha", "Hail", "Jazan", "Al Kharj", "Al Qatif", "Taif", "Najran", "Yanbu"],
            "England": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Sheffield", "Liverpool", "Bristol", "Newcastle", "Leicester", "Coventry", "Nottingham", "Hull", "Bradford", "Cardiff"]
        }
        
        # Update city options based on selected country
        city = st.selectbox("City *", country_cities.get(country, []))
        
        # Update discipline options based on degree
        degree_disciplines = {
            "Matric": ["Science", "Arts", "Commerce"],
            "Inter": ["Pre-Medical", "Pre-Engineering", "Commerce", "Arts"],
            "Bachelors": ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Business Administration", "Economics", "Physics", "Mathematics", "Biology", "Law", "Political Science", "Marketing", "Finance", "Psychology", "English", "Chemistry"],
            "Masters": ["Computer Science", "Electrical Engineering", "Business Administration", "Economics", "Physics", "Mathematics", "Biology", "Law", "Political Science", "Marketing", "Finance", "Psychology", "English", "Chemistry"],
            "MPhil": ["Computer Science", "Economics", "Physics", "Mathematics", "Biology", "Law", "Political Science", "Business Administration", "Psychology", "English", "Chemistry"],
            "PhD": ["Computer Science", "Economics", "Physics", "Mathematics", "Biology", "Law", "Political Science", "Business Administration", "Psychology", "English", "Chemistry"]
        }
        discipline = st.selectbox("Program / Discipline *", degree_disciplines.get(degree, []))
        
        if st.button("Register"):
            if not first_name or not last_name or not email or not password or not phone or not age or not country or not city or not degree or not discipline:
                st.error("Please fill in all mandatory fields.")
            else:
                success = register_user({
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                    "phone": phone,
                    "age": age,
                    "country": country,
                    "city": city,
                    "degree": degree,
                    "discipline": discipline,
                    "certifications": certifications
                })
                if success:
                    st.success("Account created! Please log in.")
                else:
                    st.error("A user with this email already exists.")

# Dashboard Section
else:
    st.success(f"Welcome, {st.session_state.user['first_name']}")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.interview_started = False
        st.session_state.current_question = None
        st.rerun()

    st.subheader("Interview Settings")

    job_role = st.selectbox("Select Job Role", JOB_ROLES)
    difficulty = st.selectbox("Select Difficulty Level", DIFFICULTY_LEVELS)
    time_per_question = st.selectbox("Time per Question (minutes)", TIME_OPTIONS)

    if not st.session_state.interview_started:
        if st.button("Start Interview"):
            st.session_state.interview_started = True
            st.session_state.current_question = f"Sample question for {job_role}"  # Replace with dynamic logic later
            st.rerun()

    if st.session_state.interview_started:
        st.subheader("Interview Question")
        st.write(st.session_state.current_question)

        answer = st.text_area("Your Answer", height=150)

        if st.button("Submit Answer"):
            st.success("Answer submitted! (Next question logic will be added)")

        if st.button("End Interview"):
            st.session_state.interview_started = False
            st.session_state.current_question = None
            st.rerun()

