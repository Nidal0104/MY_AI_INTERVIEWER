import bcrypt
from database import get_connection
from datetime import datetime

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def register_user(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (
            first_name, last_name, email, password_hash,
            phone, age, address, degree, certifications, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["first_name"],
            data["last_name"],
            data["email"],
            hash_password(data["password"]),
            data["phone"],
            data["age"],
            data["address"],
            data["degree"],
            data["certifications"],
            datetime.now().isoformat()
        ))

        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user["password_hash"]):
        return user
    return None
