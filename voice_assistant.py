import streamlit as st
import pandas as pd
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
import tempfile

# Load dataset
df = pd.read_csv("top_leads_overall.csv")

def transcribe_audio(file):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    with sr.AudioFile(tmp_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Request to speech recognition service failed."

def generate_response(text):
    text = text.lower()
    if "top" in text and "leads" in text:
        results = df.head(3)
        return "\n".join([f"{row['rooms']} room in {row['city']} for ₹{int(row['price'])}" for _, row in results.iterrows()])
    elif "delhi" in text and "property" in text:
        results = df[df["city"].str.lower() == "delhi"].head(3)
        return "\n".join([f"{row['rooms']} room in Delhi for ₹{int(row['price'])}" for _, row in results.iterrows()])
    elif "hyderabad" in text and "visit" in text:
        return "Visit scheduled for Hyderabad at 5 PM tomorrow."
    else:
        return "Sorry, I couldn't understand. Try asking about top leads or a city."

def text_to_speech(text):
    tts = gTTS(text)
    tts_buffer = BytesIO()
    tts.write_to_fp(tts_buffer)
    tts_buffer.seek(0)
    return tts_buffer

def show():
    st.markdown("## 🎙️ Voice Assistant – Real Estate Queries")
    st.info("Upload a voice message (WAV or MP3), and get intelligent property insights!")

    audio_file = st.file_uploader("📤 Upload your voice file", type=["wav", "mp3"])

    if audio_file:
        st.audio(audio_file)

        with st.spinner("🔍 Processing your voice..."):
            transcript = transcribe_audio(audio_file)
            st.success(f"📝 You said: **{transcript}**")

            reply = generate_response(transcript)
            st.markdown(f"**🤖 Response:** {reply}")

            # Voice response
            audio_bytes = text_to_speech(reply)
            st.audio(audio_bytes, format="audio/mp3")
