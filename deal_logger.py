import streamlit as st
import pandas as pd
from datetime import datetime
import os

DEAL_FILE = "data/deal_log.csv"

def load_deals():
    if os.path.exists(DEAL_FILE):
        return pd.read_csv(DEAL_FILE, parse_dates=["deal_date"])
    else:
        return pd.DataFrame(columns=[
            "deal_id", "client_name", "property_id", "city",
            "price", "deal_date", "status"
        ])

def save_deals(df):
    df.to_csv(DEAL_FILE, index=False)

def show():
    st.markdown("""
    <h2 style='color: #003B73;'>Closed Deals</h2>
    <p style='font-size: 17px; color: #374151;'>Record finalized property deals and track performance metrics.</p>
    <hr style='margin-bottom: 1rem;'>
    """, unsafe_allow_html=True)

    df = load_deals()

    with st.form("log_deal_form"):
        st.markdown("<h4 style='margin-top:1rem;'>Log a New Deal</h4>", unsafe_allow_html=True)
        client_name = st.text_input("Client Name")
        property_id = st.text_input("Property ID")
        city = st.text_input("City")
        price = st.number_input("Final Deal Price (PLN)", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Log Deal")

        if submitted:
            if not client_name or not property_id or not city:
                st.warning("Please fill in all required fields.")
            else:
                new_deal = {
                    "deal_id": f"DL-{len(df)+1:04d}",
                    "client_name": client_name,
                    "property_id": property_id,
                    "city": city,
                    "price": price,
                    "deal_date": datetime.now(),
                    "status": "closed"
                }
                df = pd.concat([df, pd.DataFrame([new_deal])], ignore_index=True)
                save_deals(df)
                st.success(f"Deal logged for {client_name} – {price:.0f} PLN")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #1E3A8A;'>Deal Analytics</h4>", unsafe_allow_html=True)

    if df.empty:
        st.info("No deals logged yet.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"{df['price'].sum():,.0f} PLN")
    col2.metric("Deals Closed", len(df))
    col3.metric("Average Deal Value", f"{df['price'].mean():,.0f} PLN")

    st.markdown("<h5 style='margin-top:2rem;'>Deals by City</h5>", unsafe_allow_html=True)
    city_summary = df.groupby("city")["price"].sum().sort_values(ascending=False).reset_index()
    st.dataframe(city_summary.rename(columns={"price": "Total Value (PLN)"}))

    st.markdown("<h5 style='margin-top:2rem;'>Deals Over Time</h5>", unsafe_allow_html=True)
    df['month'] = df['deal_date'].dt.to_period("M").astype(str)
    monthly_summary = df.groupby("month")["deal_id"].count().reset_index(name="Deals")
    st.line_chart(monthly_summary.set_index("month"))

    st.markdown("<h5 style='margin-top:2rem;'>All Logged Deals</h5>", unsafe_allow_html=True)
    st.dataframe(df.sort_values(by="deal_date", ascending=False))
    st.download_button("Download Deal Log", df.to_csv(index=False), "deal_log.csv")
