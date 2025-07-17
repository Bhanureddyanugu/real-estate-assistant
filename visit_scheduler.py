import streamlit as st
import pandas as pd
import os
import uuid
import folium
from streamlit_folium import folium_static
from modules.utils import load_all_apartment_data

VISIT_FILE = "data/visit_schedule.csv"

# Load or create visit schedule
def load_visits():
    if os.path.exists(VISIT_FILE):
        return pd.read_csv(VISIT_FILE)
    else:
        return pd.DataFrame(columns=[
            "visit_id", "client_name", "property_id", "city", "scheduled_date",
            "scheduled_time", "latitude", "longitude", "status"
        ])

def save_visits(df):
    df.to_csv(VISIT_FILE, index=False)

def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=16)
    folium.Marker([lat, lon], tooltip="Visit Location").add_to(m)
    folium_static(m)

def show():
    st.markdown("""
    <h2 style='color: #003B73;'>Visit Scheduler</h2>
    <p style='font-size: 17px; color: #374151;'>Manage and visualize scheduled client visits to property locations.</p>
    <hr style='margin-bottom: 1rem;'>
    """, unsafe_allow_html=True)

    df_props = load_all_apartment_data()
    visits_df = load_visits()

    tab1, tab2 = st.tabs(["Schedule Visit", "View Scheduled Visits"])

    with tab1:
        st.markdown("<h4 style='margin-top:1rem;'>Schedule a New Visit</h4>", unsafe_allow_html=True)
        city = st.selectbox("City", sorted(df_props['city'].dropna().unique()))

        filtered_props = df_props[df_props['city'] == city]
        prop_options = {
            f"{row['id']} | {row['type']} | {row['squareMeters']} sqm": (
                row['id'], row['latitude'], row['longitude']
            )
            for _, row in filtered_props.iterrows()
        }

        if not prop_options:
            st.warning("No properties found for the selected city.")
            return

        selected_property = st.selectbox("Property", list(prop_options.keys()))
        property_id, lat, lon = prop_options[selected_property]

        client_name = st.text_input("Client Name")
        date = st.date_input("Visit Date")
        time = st.time_input("Visit Time")

        if st.button("Schedule Visit"):
            if client_name.strip() == "":
                st.warning("Please enter the client's name.")
            else:
                visit_entry = {
                    "visit_id": str(uuid.uuid4()),
                    "client_name": client_name,
                    "property_id": property_id,
                    "city": city,
                    "scheduled_date": date.strftime("%Y-%m-%d"),
                    "scheduled_time": time.strftime("%H:%M"),
                    "latitude": lat,
                    "longitude": lon,
                    "status": "Scheduled"
                }

                visits_df = pd.concat([visits_df, pd.DataFrame([visit_entry])], ignore_index=True)
                save_visits(visits_df)

                st.success(f"Visit scheduled for {client_name} on {date.strftime('%B %d, %Y')} at {time.strftime('%I:%M %p')}")
                show_map(lat, lon)

    with tab2:
        st.markdown("<h4 style='margin-top:1rem;'>All Scheduled Visits</h4>", unsafe_allow_html=True)

        if visits_df.empty:
            st.info("No visits have been scheduled yet.")
        else:
            visits_df = visits_df.sort_values(by=["scheduled_date", "scheduled_time"])
            st.dataframe(visits_df)
            st.download_button("Download CSV", visits_df.to_csv(index=False), "visit_schedule.csv")
