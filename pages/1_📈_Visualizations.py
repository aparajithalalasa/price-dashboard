import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Visual Insights")

uploaded_file = st.file_uploader("Upload your CSV again", type="csv", key="viz")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    if {'date', 'units_sold', 'price', 'brand'}.issubset(df.columns):

        df["revenue"] = df["price"] * df["units_sold"]

        st.subheader("🕒 Revenue Over Time")
        rev_time = df.groupby("date")["revenue"].sum().reset_index()
        fig1 = px.line(rev_time, x="date", y="revenue", title="Revenue Trend")
        st.plotly_chart(fig1, use_container_width=True)

        if 'category' in df.columns:
            st.subheader("🏷️ Revenue by Category")
            fig2 = px.bar(df.groupby("category")["revenue"].sum().reset_index(),
                          x="category", y="revenue", title="Category Revenue")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🏢 Units Sold by Brand")
        fig3 = px.pie(df.groupby("brand")["units_sold"].sum().reset_index(),
                      names="brand", values="units_sold", title="Units Sold (Brand)")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Missing columns for visualization.")
else:
    st.info("Please upload a CSV file.")
