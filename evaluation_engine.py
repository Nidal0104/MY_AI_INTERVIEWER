from openai import OpenAI
import streamlit as st
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def evaluate_answer(question, answer, job_role):
    prompt = f"""
You are an expert interviewer for {job_role} role.

Evaluate the candidate answer strictly in JSON format:

{{
"score": float (0-10),
"confidence_score": float (0-10),
"grammar_score": float (0-10),
"technical_score": float (0-10),
"communication_score": float (0-10),
"strengths": "...",
"weaknesses": "...",
"improved_answer": "...",
"overall_feedback": "...",
"hire_recommendation": "pass/fail"
}}

Question: {question}
Answer: {answer}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)
