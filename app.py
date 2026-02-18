import streamlit as st
from database import create_tables
from auth import register_user, login_user

create_tables()

st.set_page_config(page_title="AI Voice Interview Simulator", layout="wide")

# Country → Top Cities
COUNTRIES_CITIES = {
    "Pakistan": ["Karachi","Lahore","Islamabad","Rawalpindi","Faisalabad","Multan","Peshawar","Quetta","Sialkot","Gujranwala","Bahawalpur","Hyderabad","Sukkur","Abbottabad","Mardan"],
    "India": ["Mumbai","Delhi","Bangalore","Hyderabad","Ahmedabad","Chennai","Kolkata","Pune","Jaipur","Lucknow","Kanpur","Nagpur","Indore","Thane","Bhopal"],
    "Saudi Arabia": ["Riyadh","Jeddah","Mecca","Medina","Dammam","Khobar","Tabuk","Abha","Hail","Jazan","Al Kharj","Al Qatif","Taif","Najran","Yanbu"],
    "England": ["London","Manchester","Birmingham","Leeds","Glasgow","Sheffield","Liverpool","Bristol","Newcastle","Leicester","Coventry","Nottingham","Hull","Bradford","Cardiff"]
}

# Degrees → Disciplines
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

# ---------------- SESSION INIT ----------------
if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎯 AI Voice Interview Simulator")

# ---------------- AUTH SECTION ----------------
if not st.session_state.user:
    option = st.sidebar.selectbox("Select", ["Login", "Register"])

    # ---------------- REGISTER ----------------
    if option == "Register":
        with st.form("register"):
            st.subheader("Create a new account")

            first_name = st.text_input("First Name *")
            last_name = st.text_input("Last Name *")
            email = st.text_input("Email *")
            password = st.text_input("Password *", type="password")
            phone = st.text_input("Cell Number *")
            age = st.selectbox("Age *", AGES)
            country = st.selectbox("Country *", list(COUNTRIES_CITIES.keys()))
            city = st.selectbox("City *", COUNTRIES_CITIES[country])
            degree = st.selectbox("Last Completed Degree *", list(DEGREES_DISCIPLINES.keys()))
            discipline = st.selectbox("Program / Discipline *", DEGREES_DISCIPLINES[degree])
            certifications = st.text_area("Certifications (if any)")

            submitted = st.form_submit_button("Register")

            mandatory_fields = [
                first_name, last_name, email, password,
                phone, age, country, city, degree, discipline
            ]

            if submitted:
                if "" in map(str, mandatory_fields):
                    st.error("Please fill in all mandatory fields before registering.")
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
                        st.success("Account created successfully! You can now login.")
                    else:
                        st.error("A user with this email already exists.")

    # ---------------- LOGIN ----------------
    if option == "Login":
        st.subheader("Login to your account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email.strip() == "" or password.strip() == "":
                st.error("Please enter both email and password.")
            else:
                user = login_user(email, password)
                if user:
                    st.session_state.user = user
                    st.success("Logged in successfully.")
                    st.rerun()   # ✅ FIXED HERE
                else:
                    st.error("Invalid credentials.")

# ---------------- DASHBOARD ----------------
else:
    st.sidebar.success(f"Welcome {st.session_state.user['first_name']}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    job_role = st.sidebar.selectbox("Select Job Role", JOB_ROLES)

    st.write("You are logged in.")
    st.write(f"Selected job role: {job_role}")
