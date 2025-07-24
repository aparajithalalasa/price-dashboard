import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Visual Insights")

if "df" not in st.session_state:
    st.warning("Please upload a CSV file in the Dashboard page first.")
    st.stop()

df = st.session_state["df"]

if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

required_cols = {'date', 'units_sold', 'price', 'brand'}
if not required_cols.issubset(df.columns):
    st.warning("Missing required columns for visualization.")
    st.stop()

df["revenue"] = df["price"] * df["units_sold"]

# Revenue over time
st.subheader("🕒 Revenue Over Time")
rev_time = df.groupby("date")["revenue"].sum().reset_index()
fig1 = px.line(rev_time, x="date", y="revenue", title="Revenue Trend")
st.plotly_chart(fig1, use_container_width=True)

# Revenue by category
if 'category' in df.columns:
    st.subheader("🏷️ Revenue by Category")
    cat_rev = df.groupby("category")["revenue"].sum().reset_index()
    fig2 = px.bar(cat_rev, x="category", y="revenue", title="Category Revenue")
    st.plotly_chart(fig2, use_container_width=True)

# Units sold by brand
st.subheader("🏢 Units Sold by Brand")
brand_units = df.groupby("brand")["units_sold"].sum().reset_index()
fig3 = px.pie(brand_units, names="brand", values="units_sold", title="Units Sold (Brand)")
st.plotly_chart(fig3, use_container_width=True)
