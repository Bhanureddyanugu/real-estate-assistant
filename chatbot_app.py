import streamlit as st
import pandas as pd
import os
import numpy as np

# ✅ Load and clean dataset
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "../data/top_leads_overall.csv")
    df = pd.read_csv(file_path)

    # Ensure numeric columns and replace 0, NaN, or values < 1 with 1
    for col in ["price", "squareMeters", "leadScore", "leadRank"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].apply(lambda x: round(x, 2) if pd.notna(x) and x >= 1 else 1.0)

    df.dropna(subset=["city"], inplace=True)
    return df

# Load cleaned data
df = load_data()

# ✅ Detect user intent
def process_input(user_input):
    user_input = user_input.lower()
    if any(greet in user_input for greet in ["hi", "hello", "hey", "hii", "greetings"]):
        return "greeting"
    elif "top" in user_input and "lead" in user_input:
        return "top_leads"
    elif "schedule" in user_input and "visit" in user_input:
        return "schedule_visit"
    elif "price" in user_input:
        return "price_query"
    elif "city" in user_input or "in" in user_input:
        return "city_query"
    else:
        return "fallback"

# ✅ Generate response
def respond_to_user(user_input):
    intent = process_input(user_input)

    if intent == "greeting":
        return "👋 Hello! How can I assist you with real estate queries today?"

    elif intent == "top_leads":
        top = df.sort_values(by="leadScore", ascending=False).head(5)
        return "\n\n".join([
            f"🏡 {row['city'].capitalize()} | {row['squareMeters']} sqm | {row['price']} PLN | Rank: {int(row['leadRank'])}"
            for _, row in top.iterrows()
        ])

    elif intent == "schedule_visit":
        return "📅 Please provide the property ID and preferred date to schedule a visit."

    elif intent == "price_query":
        avg_price = df["price"].mean()
        avg_price = round(avg_price, 2) if avg_price >= 1 else 1.0
        return f"💰 The average price across listings is approximately {avg_price} PLN."

    elif intent == "city_query":
        for city in df["city"].unique():
            if city.lower() in user_input:
                city_df = df[df["city"].str.lower() == city.lower()].sort_values(by="leadScore", ascending=False).head(3)
                return "\n".join([
                    f"🏙️ {city.capitalize()} | {row['squareMeters']} sqm | {row['price']} PLN | Lead Score: {row['leadScore']:.2f}"
                    for _, row in city_df.iterrows()
                ])
        return "🤔 Sorry, we couldn't find that city in our current listings."

    else:
        return "❓ I'm not sure how to help with that. Try asking about top leads, prices, or cities."

# ✅ Streamlit Chat UI
def show():
    st.set_page_config("Real Estate Chatbot", layout="centered")
    st.markdown("""
    <h2 style='color: #003B73;'>AI Chat Assistant</h2>
    <p style='font-size: 17px; color: #374151;'>Ask about top leads, prices, scheduling visits, or property info.</p>
    <hr style='margin-bottom: 1rem;'>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask me anything about properties...")

    if user_input:
        st.session_state.chat_history.append({"user": user_input})
        response = respond_to_user(user_input)
        st.session_state.chat_history.append({"bot": response})

    for message in st.session_state.chat_history:
        if "user" in message:
            st.markdown(f"**You:** {message['user']}")
        else:
            st.markdown(f"**Bot:** {message['bot']}")
