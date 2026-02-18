from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_question(job_role, user_profile, difficulty):
    prompt = f"""
You are conducting an interview for {job_role}.
Candidate degree: {user_profile['degree']}
Certifications: {user_profile['certifications']}

Ask one {difficulty} level question.
Only return the question text.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content
