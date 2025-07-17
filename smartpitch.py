import streamlit as st
import pandas as pd
from modules.utils import load_all_apartment_data

def generate_pitch(row):
    pitch_parts = []

    pitch_parts.append(
        f"{int(row['squareMeters'])} sqft {row['type']} located in {row['city'].capitalize()} with {int(row['rooms'])} rooms."
    )

    if row['floor'] == 0:
        floor_desc = "on the ground floor"
    elif row['floor'] == row['floorCount']:
        floor_desc = "on the top floor"
    else:
        floor_desc = f"on floor {int(row['floor'])} of {int(row['floorCount'])}"

    pitch_parts.append(f"Positioned {floor_desc}. Constructed in {int(row['buildYear'])}.")

    pitch_parts.append(f"Approximate distance from the city centre: {row['centreDistance']} km.")

    amenities = []
    if row['hasParkingSpace']: amenities.append("Parking")
    if row['hasBalcony']: amenities.append("Balcony")
    if row['hasElevator']: amenities.append("Elevator")
    if row['hasSecurity']: amenities.append("Security")
    if row['hasStorageRoom']: amenities.append("Storage Room")

    if amenities:
        pitch_parts.append("Amenities include: " + ", ".join(amenities))

    pitch_parts.append(f"Monthly Rent: ₹{int(row['price'])}")

    return " • ".join(pitch_parts)

def show():
    st.markdown("""
    <h2 style='color: #003B73;'>SmartPitch Generator</h2>
    <p style='font-size: 17px; color: #374151;'>Generate compelling property descriptions based on your selected preferences.</p>
    <hr style='margin-bottom: 1rem;'>
    """, unsafe_allow_html=True)

    df = load_all_apartment_data()

    cities = sorted(df['city'].unique())
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("Select City", cities)
        price_min = st.slider("Minimum Price (INR)", 5000, 90000, 10000)
    with col2:
        price_max = st.slider("Maximum Price (INR)", 5000, 90000, 30000)
        min_rooms = st.slider("Minimum Rooms", 1, 5, 2)

    top_n = st.slider("Number of Listings to Display", 1, 10, 5)

    filtered = df[
        (df['city'] == city) &
        (df['price'] >= price_min) &
        (df['price'] <= price_max) &
        (df['rooms'] >= min_rooms)
    ]

    if filtered.empty:
        st.warning("No properties found matching your criteria.")
        return

    filtered = filtered.sort_values(by='squareMeters', ascending=False).head(top_n)
    st.success(f"Found {len(filtered)} matching properties")

    for i, row in filtered.iterrows():
        with st.container():
            st.markdown(f"""
            <div style='background-color: #ffffff; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
                <h4 style='color:#1E3A8A;'>Property ID: {row['id']}</h4>
                <p style='margin-top: 8px;'>{generate_pitch(row)}</p>
            </div>
            """, unsafe_allow_html=True)
