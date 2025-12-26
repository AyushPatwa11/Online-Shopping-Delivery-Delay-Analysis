import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Delivery Delay Analysis", layout="wide")

st.title("📦 Online Shopping Delivery Delay Pattern Analysis")
st.markdown("Analyze delivery delays using Pandas and visual insights.")

# Load data
df = pd.read_csv("delivery_data.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["delivery_date"] = pd.to_datetime(df["delivery_date"])

# Calculate delay
df["delivery_delay_days"] = (df["delivery_date"] - df["order_date"]).dt.days

# Sidebar filters
st.sidebar.header("🔍 Filters")
city = st.sidebar.selectbox("Select City", ["All"] + list(df["city"].unique()))
shipping = st.sidebar.selectbox("Shipping Type", ["All"] + list(df["shipping_type"].unique()))

if city != "All":
    df = df[df["city"] == city]

if shipping != "All":
    df = df[df["shipping_type"] == shipping]

# Display data
st.subheader("📄 Delivery Data")
st.dataframe(df)

# Descriptive statistics
st.subheader("📊 Delay Statistics")
st.write(df["delivery_delay_days"].describe())

# Line plot
st.subheader("📈 Delivery Delay Trend")
fig, ax = plt.subplots()
ax.plot(df["order_date"], df["delivery_delay_days"], marker="o")
ax.set_xlabel("Order Date")
ax.set_ylabel("Delay (Days)")
ax.set_title("Delivery Delay Over Time")
st.pyplot(fig)

# Average delay by city
st.subheader("🏙️ Average Delay by City")
avg_city = df.groupby("city")["delivery_delay_days"].mean()
st.bar_chart(avg_city)

# Download report
st.subheader("⬇️ Download Report")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV Report", csv, "delivery_delay_report.csv", "text/csv")
