from openai import OpenAI
import streamlit as st
from gtts import gTTS
import tempfile

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def speech_to_text(audio_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

def text_to_speech(text):
    tts = gTTS(text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name
