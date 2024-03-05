import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib



# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("./DataSet_All.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("./logo_e_commerce.png"
                 , width=100)
    with col3:
        st.write(' ')

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

def create_daily_orders_df(main_df):
    daily_orders_df = main_df.resample(rule='D', on='order_approved_at').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    
    return daily_orders_df
 
st.title("E-Commerce Public Data Analysis")
st.write("Welcome to the E-Commerce Public Data Analysis Dashboard.")

daily_orders_df = create_daily_orders_df(main_df)

main_df['shipping_month'] = main_df['shipping_limit_date'].dt.month
month_counts = main_df['shipping_month'].value_counts().sort_index()
month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
               7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
month_counts.index = month_counts.index.map(month_names)

# Create Streamlit app
st.title('Transactional Activity by Month')

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(month_counts.index, month_counts.values, color='skyblue')
plt.title('Transactional Activity by Month')
plt.xlabel('Month')
plt.ylabel('Number of Transactions')
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)
st.title('Top 20 Best-selling Products')
st.write('This visualization shows the top 20 best-selling products.')

# Calculate top 20 best-selling products
top_products = main_df['product_category_name'].value_counts().head(20)

# Create bar plot using Seaborn
plt.figure(figsize=(12, 8))
sns.barplot(x=top_products.values, y=top_products.index, palette='cividis')
plt.title('Top 20 Best-selling Products')
plt.xlabel('Number of Sales')
plt.ylabel('Product Category')
st.pyplot(plt)
