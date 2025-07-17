import streamlit as st
import os
import tempfile
import whisper
from pydub import AudioSegment
from datetime import datetime
import pandas as pd
import re

@st.cache_resource
def load_model():
    return whisper.load_model("base")  # You may choose "medium" or "large" if needed

model = load_model()

def transcribe_audio(uploaded_file):
    try:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        audio = AudioSegment.from_file(uploaded_file, format=file_ext)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio.export(tmp.name, format="wav")
            tmp_path = tmp.name

        result = model.transcribe(tmp_path, language="en", task="translate")

        os.remove(tmp_path)
        return result["text"]
    except Exception as e:
        return f"Transcription error: {e}"

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

def contains_time_info(sentence):
    # Regex pattern for time expressions (expand as needed)
    time_patterns = [
        r"\b\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)\b",  # e.g., 5 PM, 10:30 am
        r"\b\d{1,2}\s?(am|pm|AM|PM)\b",           # e.g., 9am
        r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        r"\btoday\b", r"\btomorrow\b", r"\bnext week\b", r"\bthis weekend\b"
    ]
    return any(re.search(p, sentence, re.IGNORECASE) for p in time_patterns)

def summarize_text(text, max_sentences=3):
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    if len(sentences) <= max_sentences:
        return ' '.join(sentences)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)
    scores = np.array(X.sum(axis=1)).ravel()

    # Boost scores for sentences that mention time
    for i, sentence in enumerate(sentences):
        if contains_time_info(sentence):
            scores[i] += 5  # Boost weight for time-related sentences

    top_indices = scores.argsort()[-max_sentences:][::-1]
    top_sentences = [sentences[i] for i in sorted(top_indices)]

    return ' '.join(top_sentences)



def save_transcript(client_name, transcript, summary):
    df_path = "data/client_transcripts.csv"
    os.makedirs("data", exist_ok=True)
    new_row = {
        "client_name": client_name,
        "transcription": transcript,
        "summary": summary,
        "timestamp": datetime.now()
    }
    if os.path.exists(df_path):
        df = pd.read_csv(df_path)
    else:
        df = pd.DataFrame(columns=new_row.keys())
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(df_path, index=False)

def show():
    st.markdown("""
    <h2 style='color: #003B73;'>TalkToCRM</h2>
    <p style='font-size: 17px; color: #374151;'>Upload and transcribe a client's voice message, then get a quick summary to log key insights.</p>
    <hr style='margin-bottom: 1rem;'>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload voice message (.mp3, .m4a, .wav)", type=["mp3", "m4a", "wav"])

    if uploaded_file:
        client_name = st.text_input("Client Name")

        if st.button("Transcribe & Summarize"):
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(uploaded_file)
                summary = summarize_text(transcript)
                save_transcript(client_name or "Unknown", transcript, summary)

            st.success("Transcription completed successfully!")
            st.markdown("<h4 style='color: #1E3A8A;'>Transcript</h4>", unsafe_allow_html=True)
            st.write(transcript)

            st.markdown("<h4 style='color: #1E3A8A;'>Summary</h4>", unsafe_allow_html=True)
            st.write(summary)

    df_path = "data/client_transcripts.csv"
    if os.path.exists(df_path):
        st.markdown("---")
        st.markdown("<h4 style='color:#1E3A8A;'>Recent Transcripts</h4>", unsafe_allow_html=True)
        df = pd.read_csv(df_path)
        st.dataframe(df.tail(5))
