import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Supply Chain Analytics Dashboard", layout="wide")

# Title
st.title("📦 Supply Chain Analytics Dashboard")

# Load dataset
df = pd.read_csv("supplychain_cleaned.csv")

# -------------------------
# Feature Engineering
# -------------------------

df["Profit_Margin"] = df["Order Profit Per Order"] / df["Sales"]

df["Discount_Percentage"] = (df["Order Item Discount"] / df["Sales"]) * 100

df["Delivery_Delay"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    df["Order Region"].unique(),
    default=df["Order Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    df["Category Name"].unique(),
    default=df["Category Name"].unique()
)

shipping_filter = st.sidebar.multiselect(
    "Select Shipping Mode",
    df["Shipping Mode"].unique(),
    default=df["Shipping Mode"].unique()
)

filtered_df = df[
    (df["Order Region"].isin(region_filter)) &
    (df["Category Name"].isin(category_filter)) &
    (df["Shipping Mode"].isin(shipping_filter))
]

# -------------------------
# KPI Section
# -------------------------

total_revenue = filtered_df["Sales"].sum()
total_profit = filtered_df["Order Profit Per Order"].sum()
total_orders = filtered_df.shape[0]
loss_orders = filtered_df[filtered_df["Order Profit Per Order"] < 0].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", total_orders)
col4.metric("Loss Orders", loss_orders)

st.divider()

# -------------------------
# Category Revenue Analysis
# -------------------------

st.subheader("📊 Revenue by Category")

category_sales = (
    filtered_df.groupby("Category Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_sales)

# -------------------------
# Regional Revenue Analysis
# -------------------------

st.subheader("🌍 Revenue by Region")

region_sales = (
    filtered_df.groupby("Order Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(region_sales)

# -------------------------
# Discount Impact
# -------------------------

st.subheader("💸 Discount Impact on Profit")

discount_profit = filtered_df.groupby(
    pd.cut(filtered_df["Discount_Percentage"], bins=5)
)["Order Profit Per Order"].mean()

st.bar_chart(discount_profit)

# -------------------------
# Shipping Delay Analysis
# -------------------------

st.subheader("🚚 Average Delivery Delay by Shipping Mode")

delay = filtered_df.groupby("Shipping Mode")["Delivery_Delay"].mean()

st.bar_chart(delay)

# -------------------------
# Top Customers
# -------------------------

st.subheader("👥 Top Customers by Revenue")

top_customers = (
    filtered_df.groupby("Customer Id")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_customers)

# -------------------------
# Dataset Preview
# -------------------------

st.subheader("🔎 Dataset Preview")

st.dataframe(filtered_df.head())