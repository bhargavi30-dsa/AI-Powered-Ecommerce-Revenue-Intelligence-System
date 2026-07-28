import pandas as pd
import numpy as np
#It calculates actual discount given,this will help the companies to know the gross margin
def calculate_discount_amount(df):
    df['discounted_amount']=df['listed_price']-df['current/discounted_price']
    return df
#calculates discount % given by the company for each product
def discount_pct(df):
    df['discount_pct']=(df['discounted_amount']/df['listed_price'])*100
    return df
#It calculates customer value for money
def calculate_value_score(df):
    df['value_score']=df['rating']/df['current/discounted_price']
    return df
#normalize demand across all products
def calculate_demand_score(df):
    df['demand_score']=df['bought_in_last_month']/df['bought_in_last_month'].max() 
    return df
def calculate_revenue(df):
    df['estimated_revenue']=df['current/discounted_price']*df['bought_in_last_month']
    return df
#grouping current/discounted_price to categories like budget,mid-range,premium
def create_price_category(df):
    def get_category(price):
        if pd.isna(price):
            return 'Unknown'
        elif price<25:
            return 'Budget'
        elif price<125:
            return 'Mid-range'
        else:
            return 'Premium'
    df['price_category']=df['current/discounted_price'].apply(get_category)
    return df   
#used to know whether the price is mid-range,budget,premium by comparing with all the prices.Simply helpful to know how far the value is from avg
def calculate_market_positioning(df):
    avg_price=df['current/discounted_price'].mean()
    df['price_vs_avg']=df['current/discounted_price']/avg_price
    return df
#calculating revenue leakage
def calculate_revenue_leakage(df):
    potential_revenue=df['listed_price']*df['bought_in_last_month']
    actual_revenue=df['estimated_revenue']
    leakage_revenue=((potential_revenue-actual_revenue)/potential_revenue)*100
    df['revenue_leakage_pct']=leakage_revenue.clip(lower=0)
    df['premium_price_flag']=(leakage_revenue<0).astype(int)
    return df
"""
    High rating with many reviews = very trustworthy!
    High rating with few reviews = less trustworthy!
    Formula: rating × log(number_of_reviews + 1)
    +1 to avoid log(0) error!
"""
def calculate_review_credibility(df):
    df['review_credibility']=df['rating']*np.log(df['number_of_reviews']+1)
    return df
#calculating all at a time
def engineer_all_features(df):
    df=calculate_discount_amount(df)
    df=discount_pct(df)
    df=calculate_value_score(df)
    df=calculate_demand_score(df)
    df=calculate_revenue(df)
    df=create_price_category(df)
    df=calculate_revenue_leakage(df)
    df=calculate_market_positioning(df)
    df=calculate_review_credibility(df)
    #returns complete featured dataframe
    return df


