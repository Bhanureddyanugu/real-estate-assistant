import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

FEEDBACK_FILE = "data/client_feedback.csv"
REQUIRED_DOCS = ["aadhaar", "pan", "income", "photo"]

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        return pd.read_csv(FEEDBACK_FILE)
    else:
        return pd.DataFrame(columns=[
            "client_id", "client_name", "property_id", "feedback", "rating",
            "documents_uploaded", "missing_docs", "upload_time"
        ])

def save_feedback(df):
    df.to_csv(FEEDBACK_FILE, index=False)

def process_uploaded_files(uploaded_files):
    uploaded_types = []
    saved_names = []

    for file in uploaded_files:
        filename = file.name
        saved_path = os.path.join("data", "docs", filename)
        os.makedirs(os.path.dirname(saved_path), exist_ok=True)
        with open(saved_path, "wb") as f:
            f.write(file.read())
        saved_names.append(filename)
        for doc in REQUIRED_DOCS:
            if doc.lower() in filename.lower():
                uploaded_types.append(doc.lower())

    missing = list(set(REQUIRED_DOCS) - set(uploaded_types))
    return saved_names, missing

def show():
    st.markdown("""
    <h2 style='color: #003B73;'>Client Feedback</h2>
    <p style='font-size: 17px; color: #374151;'>Collect valuable client insights and ensure all documentation is submitted accurately.</p>
    <hr style='margin-bottom: 1rem;'>
    """, unsafe_allow_html=True)

    with st.form("feedback_form"):
        st.markdown("<h4 style='margin-top:1rem;'>Submit Feedback</h4>", unsafe_allow_html=True)
        client_name = st.text_input("Client Name")
        property_id = st.text_input("Property ID")
        feedback = st.text_area("Feedback")
        rating = st.slider("Rating (1-5)", min_value=1, max_value=5, value=3)

        uploaded_files = st.file_uploader("Upload Documents (Aadhaar, PAN, etc.)", accept_multiple_files=True)

        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if not client_name or not property_id:
                st.warning("Please fill in all required fields.")
                return

            docs_uploaded, missing_docs = process_uploaded_files(uploaded_files)

            new_entry = {
                "client_id": str(uuid.uuid4()),
                "client_name": client_name,
                "property_id": property_id,
                "feedback": feedback,
                "rating": rating,
                "documents_uploaded": ", ".join(docs_uploaded),
                "missing_docs": ", ".join(missing_docs),
                "upload_time": datetime.now()
            }

            df = load_feedback()
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            save_feedback(df)
            st.success("Feedback submitted and saved.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #1E3A8A;'>Recent Feedback</h4>", unsafe_allow_html=True)

    df = load_feedback()
    if df.empty:
        st.info("No feedback yet.")
    else:
        st.dataframe(df.sort_values(by="upload_time", ascending=False).head(5))
        st.download_button("Download Feedback", df.to_csv(index=False), "client_feedback.csv")
