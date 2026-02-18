import sqlite3
from database import get_connection
import bcrypt
from datetime import datetime

# -------------------- REGISTER USER --------------------
def register_user(user_data):
    """
    user_data dictionary keys:
    first_name, last_name, email, password, phone,
    age, country, city, degree, discipline, certifications
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (user_data["email"],))
    if cursor.fetchone():
        conn.close()
        return False  # user exists

    # Hash password
    password_bytes = user_data["password"].encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Insert user
    cursor.execute("""
        INSERT INTO users (
            first_name, last_name, email, password_hash, phone,
            age, country, city, degree, discipline, certifications, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_data["first_name"],
        user_data["last_name"],
        user_data["email"],
        hashed,
        user_data["phone"],
        user_data["age"],
        user_data["country"],
        user_data["city"],
        user_data["degree"],
        user_data["discipline"],
        user_data.get("certifications", ""),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
    return True

# -------------------- LOGIN USER --------------------
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_hash = row[4]  # password_hash
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "phone": row[5],
                "age": row[6],
                "country": row[7],
                "city": row[8],
                "degree": row[9],
                "discipline": row[10],
                "certifications": row[11]
            }
    return None
