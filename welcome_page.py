import streamlit as st
import base64
import os

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def show():
    image_path = r"C:\Users\ANUGU BHANU REDDY\Desktop\buil.jpg"

    if not os.path.exists(image_path):
        st.error("❌ Image not found at: " + image_path)
        return

    base64_image = get_base64_image(image_path)

    # Inject CSS styles
    st.markdown(f"""
        <style>
            .stApp {{
                background: url("data:image/jpg;base64,{base64_image}") no-repeat center center fixed;
                background-size: cover;
            }}

            .center-button {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1;
            }}

            div.stButton > button {{
                background-color: white;
                color: black;
                font-size: 1.2em;
                padding: 12px 32px;
                border-radius: 30px;
                border: 2px solid gray;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
                transition: all 0.3s ease;
            }}

            div.stButton > button:hover {{
                background-color: #f5f5f5;
                transform: scale(1.05);
                box-shadow: 4px 4px 12px rgba(0,0,0,0.25);
            }}
        </style>
    """, unsafe_allow_html=True)

    # Optional title near top
    # st.markdown('<h1 style="text-align:center; color:black; margin-top: 60px;">🏙️ Welcome to DealMate.AI</h1>', unsafe_allow_html=True)

    # Centered button
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("Next"):
        st.query_params["page"] = "🏠 Home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
