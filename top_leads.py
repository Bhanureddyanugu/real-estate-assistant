import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from modules.utils import load_all_apartment_data
# modules/top_leads.py

def show():


    st.markdown("""
    <h2 style='color: #003B73;'>Top Leads Overview</h2>
    <p style='font-size: 17px; color: #374151;'>Explore the highest scoring rental leads ranked by quality, location, and amenities.</p>
    <hr style='margin-bottom: 1rem;'>
    """, unsafe_allow_html=True)

    df = load_all_apartment_data()

    # Preprocessing
    bool_cols = ['hasParkingSpace', 'hasBalcony', 'hasElevator', 'hasSecurity', 'hasStorageRoom']
    for col in bool_cols:
        df[col] = df[col].map({'yes': 1, 'no': 0}).fillna(0)

    for col in ['buildYear', 'price', 'floorCount', 'squareMeters', 'floor', 'rooms']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())

    df = df.drop_duplicates(subset=['id'])
    df['condition'] = df['condition'].fillna("standard")

    # Scoring
    def condition_score(c):
        if 'premium' in str(c).lower(): return 1
        elif 'good' in str(c).lower(): return 0.5
        return 0

    df['conditionBonus'] = df['condition'].apply(condition_score)

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    cols = ["squareMeters", "rooms", "floor", "floorCount", "buildYear", "centreDistance",
            "poiCount", "schoolDistance", "clinicDistance", "restaurantDistance",
            "pharmacyDistance", "price"]
    df[cols] = scaler.fit_transform(df[cols])

    def score(row):
        score = 0
        score += (1 - row['centreDistance']) * 2
        score += (1 - row['schoolDistance']) * 1.5
        score += (1 - row['clinicDistance']) * 1.5
        score += (1 - row['restaurantDistance']) * 1
        score += (1 - row['pharmacyDistance']) * 1
        score += row['poiCount'] * 2
        score += (1 - row['price']) * 2
        score += row['squareMeters'] * 1
        score += row['hasParkingSpace'] * 1
        score += row['hasBalcony'] * 0.5
        score += row['hasElevator'] * 0.5
        score += row['hasSecurity'] * 0.5
        score += row['hasStorageRoom'] * 0.5
        score += row['buildYear'] * 1
        score += row['conditionBonus'] * 0.5
        return score

    df['leadScore'] = df.apply(score, axis=1)
    df['leadRank'] = df['leadScore'].rank(ascending=False)

    def urgency(s):
        if s >= 12: return 'High'
        elif s >= 8: return 'Medium'
        else: return 'Low'

    df['urgency'] = df['leadScore'].apply(urgency)
    df.to_csv("data/top_leads_overall.csv", index=False)

    st.markdown("<h4 style='margin-top:2rem; color:#1E3A8A;'>Top 10 Ranked Properties</h4>", unsafe_allow_html=True)
    st.dataframe(df[['id', 'city', 'leadScore', 'urgency', 'price']].sort_values(by="leadScore", ascending=False).head(10))

    st.markdown("<h4 style='margin-top:3rem;'>Urgency Distribution</h4>", unsafe_allow_html=True)
    fig1 = sns.countplot(data=df, x='urgency', order=['High', 'Medium', 'Low'])
    st.pyplot(fig1.figure)
    plt.clf()

    st.markdown("<h4 style='margin-top:3rem;'>Price vs. Size (Lead Score)</h4>", unsafe_allow_html=True)
    bubble_df = df[['squareMeters', 'price', 'leadScore', 'urgency']].dropna()
    bubble_df = bubble_df[bubble_df['leadScore'] > 0]

    if bubble_df.empty:
        st.warning("Not enough valid data to plot bubble chart.")
    else:
        fig2 = px.scatter(
            bubble_df,
            x="squareMeters",
            y="price",
            size="leadScore",
            color="urgency",
            title="Price vs Size (Bubble = Lead Score)",
            template="plotly_white"
        )
        st.plotly_chart(fig2)

    st.markdown("<h4 style='margin-top:3rem;'>Top Cities by Average Lead Score</h4>", unsafe_allow_html=True)
    avg = df.groupby("city")["leadScore"].mean().reset_index().sort_values(by="leadScore", ascending=False)
    fig3 = px.bar(avg.head(10), x="leadScore", y="city", orientation="h", template="plotly_white")
    st.plotly_chart(fig3) 