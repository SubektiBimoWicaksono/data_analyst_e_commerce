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
st.write("Welcome to the E-Commerce Public Data Analysis Dashboard. Explore insights and trends from the provided dataset.")

daily_orders_df = create_daily_orders_df(main_df)

# Display the daily orders DataFrame in Streamlit
st.title("Daily Orders Delivered")
st.write(daily_orders_df)

st.subheader("Daily Orders Trend")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_orders_df['order_approved_at'], daily_orders_df['order_count'], marker='o', color='skyblue')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Orders')
ax.set_title('Daily Orders Trend')
ax.grid(True)
st.pyplot(fig)

main_df['shipping_month'] = main_df['shipping_limit_date'].dt.month
month_counts = main_df['shipping_month'].value_counts().sort_index()
month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
               7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
month_counts.index = month_counts.index.map(month_names)

# Create Streamlit app
st.title('Transactional Activity by Month')

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(month_counts.index, month_counts.values, color='salmon')  # Ubah warna menjadi 'salmon'
plt.title('Transactional Activity by Month')
plt.xlabel('Month')
plt.ylabel('Number of Transactions')
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)
st.title('Top 10 Best-selling Products')
st.write('This visualization shows the top 10 best-selling products.')

# Calculate top 10 best-selling products
top_products = main_df['product_category_name'].value_counts().head(20)

# Create bar plot using Seaborn
plt.figure(figsize=(12, 8))
sns.barplot(x=top_products.values, y=top_products.index, palette='magma')  # Ubah palet warna menjadi 'magma'
plt.title('Top 10 Best-selling Products')
plt.xlabel('Number of Sales')
plt.ylabel('Product Category')
st.pyplot(plt)

st.title('Customer Spending Over Time')
st.write('This visualization shows the trend of customer spending over time.')

# Create line plot using Seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(x='shipping_month', y='payment_value', data=main_df, color='skyblue')  # Ubah warna menjadi 'skyblue'
plt.title('Customer Spending Over Time')
plt.xlabel('Month')
plt.ylabel('Total Payment Value')

# Brazil Mapping
st.pyplot(plt)
st.title("Brazil Geolocation Map")
st.write("Showing geolocation data on the map of Brazil.")

plot_brazil_map(geolocation)

# Distribution of Review Scores
st.title("Distribution of Review Scores")
st.write("This chart shows the distribution of review scores.")
plt.figure(figsize=(8, 6))
sns.histplot(main_df['review_score'], bins=5, kde=True, color='lightgreen')  # Ubah warna menjadi 'lightgreen'
plt.title('Distribution of Review Scores')
plt.xlabel('Review Score')
plt.ylabel('Count')
st.pyplot()


# Customer Satisfaction Over Time
st.title("Customer Satisfaction Over Time")
st.write("This chart shows the trend of customer satisfaction over time.")

plt.figure(figsize=(10, 6))
sns.lineplot(x='shipping_month', y='review_score', data=main_df, color='gold')  # Ubah warna menjadi 'gold'
plt.title('Customer Satisfaction Over Time')
plt.xlabel('Month')
plt.ylabel('Review Score')
plt.ylim(0, 5)  
plt.grid(True) 

st.pyplot()