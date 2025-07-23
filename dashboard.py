import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Product Price vs Sales Dashboard")

# 📁 Upload Section
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Try converting date if possible
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    st.success("✅ File uploaded successfully!")
    st.write("### Preview of Uploaded Data", df.head())

    # Check required columns
    required_cols = {'product_id', 'price', 'units_sold', 'date'}
    if required_cols.issubset(set(df.columns)):

        # Dropdown to select product_id
        selected = st.selectbox("Choose Product ID", df["product_id"].unique())
        filtered = df[df["product_id"] == selected].sort_values("date")

        fig = go.Figure()
        fig.add_trace(go.Bar(x=filtered["date"], y=filtered["units_sold"], name="Units Sold"))
        fig.add_trace(go.Scatter(x=filtered["date"], y=filtered["price"], yaxis="y2", name="Price"))

        fig.update_layout(
            yaxis=dict(title="Units Sold"),
            yaxis2=dict(title="Price", overlaying="y", side="right"),
            title=f"Product {selected} - Sales vs Price"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"❌ Required columns not found: {required_cols - set(df.columns)}")

else:
    st.info("👈 Please upload a CSV file to begin.")
