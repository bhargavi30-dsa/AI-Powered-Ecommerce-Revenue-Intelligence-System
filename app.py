import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import sys
import os

# Dynamic path — works from anywhere! any computer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))

from feature_engineering import engineer_all_features
#page configuration
st.set_page_config("E-commerce Revenue Intelligence",page_icon="🛒",layout='wide')

# Title
st.title("🛒 E-Commerce Revenue Intelligence System")
st.markdown("**AI-Powered Dynamic Pricing Analysis for Amazon Electronics**")
st.divider()
# Load data and model
@st.cache_data
def load_data():
    df = pd.read_csv(
        os.path.join(BASE_DIR, 'data', 'processed', 'cleaned_products.csv'),
        index_col=0)
    df = engineer_all_features(df)
    return df

# @st.cache_resource
def load_model():
    model = joblib.load(
        os.path.join(BASE_DIR, 'outputs', 'models', 'rf_model.pkl'))
    scaler = joblib.load(
        os.path.join(BASE_DIR, 'outputs', 'models', 'scaler.pkl'))
    return model, scaler

df = load_data()
model, scaler = load_model()

st.write("MODEL FILE:", os.path.join(BASE_DIR, 'outputs', 'models', 'rf_model.pkl'))
st.write("SCALER FILE:", os.path.join(BASE_DIR, 'outputs', 'models', 'scaler.pkl'))

st.write("SCALER FEATURES:")
st.write(scaler.feature_names_in_.tolist())

st.write("Model expects:")
st.write(model.n_features_in_)
# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.selectbox("Choose Page:", [
    "📊 Dashboard",
    "💰 Price Predictor",
    "🤖 AI Insights"
])

st.sidebar.divider()
st.sidebar.metric("Total Products", f"{len(df):,}")
st.sidebar.metric("Avg Price", f"${df['current/discounted_price'].mean():.2f}")
st.sidebar.metric("Avg Rating", f"{df['rating'].mean():.2f}")

#Page 1 (Dashboard)
if page == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total Products", f"{len(df):,}")
    with col2:
        st.metric("💰 Average Price", 
                  f"${df['current/discounted_price'].mean():.2f}")
    with col3:
        st.metric("⭐ Average Rating", 
                  f"{df['rating'].mean():.2f}")
    with col4:
        st.metric("📉 Avg Revenue Leakage", 
                  f"{df['revenue_leakage_pct'].mean():.1f}%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏷️ Price Category Distribution")
        fig, ax = plt.subplots(figsize=(6,6))
        explode = (0.05, 0, 0)
        colors = ['#2196F3', '#FF9800', '#4CAF50']
        df['price_category'].value_counts().plot(
            kind='pie', 
            autopct='%1.1f%%',
            colors=colors,
            ax=ax,
            explode=explode,
            startangle=90)
        ax.set_ylabel('')
        st.pyplot(fig)
    
    with col2:
        st.subheader("💵 Price Distribution")
        fig, ax = plt.subplots(figsize=(6,6))
        ax.hist(df['current/discounted_price'].clip(upper=500), 
                bins=50, 
                color='#2196F3',
                edgecolor='white',
                alpha=0.8)
        ax.set_xlabel('Price ($)')
        ax.set_ylabel('Number of Products')
        ax.axvline(df['current/discounted_price'].median(),
                   color='red', linestyle='--',
                   label=f"Median: ${df['current/discounted_price'].median():.0f}")
        ax.legend()
        st.pyplot(fig)
    
    st.divider()
    
    # Revenue leakage summary
    st.subheader("💸 Revenue Leakage Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        zero_leakage = (df['revenue_leakage_pct']==0).sum()
        st.metric("Zero Leakage Products", f"{zero_leakage:,}")
    with col2:
        high_leakage = (df['revenue_leakage_pct']>50).sum()
        st.metric("High Leakage (>50%)", f"{high_leakage:,}", 
                  delta="Needs attention!", delta_color="inverse")
    with col3:
        avg_leakage = df['revenue_leakage_pct'].mean()
        st.metric("Average Leakage", f"{avg_leakage:.1f}%")

elif page == "💰 Price Predictor":
    st.header("💰 Price Predictor")
    st.write("Enter product details to get optimal price recommendation!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rating = st.slider("⭐ Product Rating", 
                           1.0, 5.0, 4.0, 0.1)
        reviews = st.number_input("📝 Number of Reviews", 
                                   0, 100000, 1000)
        bought = st.number_input("🛒 Bought Last Month", 
                                  0, 100000, 500)
    
    with col2:
        listed_price = st.number_input("💵 Listed Price ($)", 
                                        0.0, 5000.0, 100.0)
        is_sponsored = st.selectbox("📢 Sponsored?", [0, 1])
        demand_score = bought / 100000
        review_cred = rating * np.log(reviews + 1)
    
    if st.button("🔮 Predict Optimal Price"):
        features = pd.DataFrame({
    'rating': [rating],
    'number_of_reviews': [reviews],
    'bought_in_last_month': [bought],
    'listed_price': [listed_price],
    'is_best_seller': [0],        # ← always 0, doesn't matter!
    'is_sponsored': [is_sponsored],
    'is_couponed': [0],           # ← always 0, doesn't matter!
    'sustainability_badges': [0], # ← always 0, doesn't matter!
    'demand_score': [demand_score],
    'review_credibility': [review_cred]
})
        
        features_scaled = scaler.transform(features)
        predicted_price = model.predict(features_scaled)[0]
        
        st.success(f"💰 Recommended Price: ${predicted_price:.2f}")        