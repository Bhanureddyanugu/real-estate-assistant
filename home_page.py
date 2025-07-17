import streamlit as st

def show():
    st.set_page_config(page_title="DealMate.AI | Real Estate Assistant", layout="wide", page_icon="🏠")

    st.markdown("""
    <style>
    html, body, .main {
        background-color: #F5F9FF;
        font-family: 'Segoe UI', sans-serif;
        color: #2F3E4D;
    }
    .home-title {
        text-align: center;
        font-size: 2.8rem;
        color: #003B73;
        font-weight: bold;
        margin-top: 1.5rem;
    }
    .home-subtitle {
        text-align: center;
        font-size: 18px;
        color: #4B5563;
        margin-bottom: 40px;
    }
    .card {
        background-color: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 3px 14px rgba(0, 0, 0, 0.07);
        height: 100%;
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card img {
        width: 80px;
        height: 80px;
        object-fit: contain;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: #003B73;
        margin-bottom: 12px;
    }
    .footer {
        margin-top: 4rem;
        padding: 2rem 1rem;
        text-align: center;
        background-color: #232F3E;
        color: #ffffff;
        font-size: 13px;
        border-top: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='home-title'>🏠 Welcome to DealMate.AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='home-subtitle'>Revolutionizing Real Estate with AI-powered Modules</div>", unsafe_allow_html=True)

    modules = [
        {"name": "Top Leads", "img": "https://cdn-icons-png.flaticon.com/512/547/547420.png"},
        {"name": "SmartPitch Generator", "img": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"},
        {"name": "Visit Scheduler", "img": "https://cdn-icons-png.flaticon.com/512/2838/2838912.png"},
        {"name": "TalkToCRM", "img": "https://cdn-icons-png.flaticon.com/512/1250/1250620.png"},
        {"name": "Closed Deals", "img": "https://cdn-icons-png.flaticon.com/512/942/942748.png"},
        {"name": "Client Feedback", "img": "https://cdn-icons-png.flaticon.com/512/3063/3063822.png"},
        {"name": "Contract Generator", "img": "https://cdn-icons-png.flaticon.com/512/1250/1250615.png"},
        {"name": "Chat Bot", "img": "https://cdn-icons-png.flaticon.com/512/4712/4712037.png"},
    ]

    for i in range(0, len(modules), 3):
        cols = st.columns(3, gap="large")
        for j in range(3):
            if i + j < len(modules):
                module = modules[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="card">
                            <img src="{module['img']}" alt="{module['name']} Icon">
                            <div class="card-title">{module['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)

                    if st.button("Open", key=module['name'], help=f"Go to {module['name']}", use_container_width=True):
                        st.query_params.update({"page": module['name']})
                        st.rerun()

    # Amazon-style footer
    st.markdown("""
    <div class='footer'>
        © 2025 DealMate.AI · Built with ❤️ by Anugu Bhanu Reddy · All rights reserved.<br>
        Inspired by Amazon’s commitment to usability and trust.
    </div>
    """, unsafe_allow_html=True)
