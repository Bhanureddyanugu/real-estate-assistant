import streamlit as st
from modules import (
    welcome_page, home_page, top_leads, smartpitch, visit_scheduler,
    talktocrm, deal_logger, feedback, contract, chatbot_app
)

# ✅ App Configuration
st.set_page_config(
    page_title="DealMate.AI | Real Estate Assistant",
    layout="wide",
    page_icon="🏠"
)

# ✅ Ensure query_params exists
if "page" not in st.query_params:
    st.query_params["page"] = "👋 Welcome"

# ✅ Current page from URL or default
page = st.query_params.get("page", "👋 Welcome")

# ✅ All Available Pages
pages = [
    "👋 Welcome",
    "🏠 Home",
    "Top Leads",
    "SmartPitch Generator",
    "Visit Scheduler",
    "TalkToCRM",
    "Closed Deals",
    "Client Feedback",
    "Contract Generator",
    "Chat Bot"
]

# ✅ Sidebar Navigation
selected = st.sidebar.selectbox("🔎 Explore DealMate Modules", pages, index=pages.index(page))

# ✅ Update query param if page changed
if selected != page:
    st.query_params.update({"page": selected})
    st.rerun()

# ✅ Routing to each page
if selected == "👋 Welcome":
    welcome_page.show()
elif selected == "🏠 Home":
    home_page.show()
elif selected == "Top Leads":
    top_leads.show()
elif selected == "SmartPitch Generator":
    smartpitch.show()
elif selected == "Visit Scheduler":
    visit_scheduler.show()
elif selected == "TalkToCRM":
    talktocrm.show()
elif selected == "Closed Deals":
    deal_logger.show()
elif selected == "Client Feedback":
    feedback.show()
elif selected == "Contract Generator":
    contract.show()
elif selected == "Chat Bot":
    chatbot_app.show()
else:
    st.error("❌ Invalid page selected.")
