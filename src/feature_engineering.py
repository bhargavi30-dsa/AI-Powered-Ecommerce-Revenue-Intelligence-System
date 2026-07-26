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
#calculating all at a time
def engineer_all_features(df):
    df=calculate_discount_amount(df)
    df=discount_pct(df)
    df=calculate_value_score(df)
    df=calculate_demand_score(df)
    df=calculate_revenue(df)
    #returns complete featured dataframe
    return df
       
