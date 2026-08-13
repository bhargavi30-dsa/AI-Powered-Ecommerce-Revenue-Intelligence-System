import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import sys
sys.path.append(r'D:\E-Commerce_dynamic_system\src')
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
    df = pd.read_csv(r'D:\E-Commerce_dynamic_system\data\processed\cleaned_products.csv',
                     index_col=0)
    df = engineer_all_features(df)
    return df

@st.cache_resource
def load_model():
    model = joblib.load(r'D:\E-Commerce_dynamic_system\outputs\models\rf_model.pkl')
    scaler = joblib.load(r'D:\E-Commerce_dynamic_system\outputs\models\scaler.pkl')
    return model, scaler

df = load_data()
model, scaler = load_model()

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