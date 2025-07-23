import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 Product Sales Dashboard with Forecasting")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    st.success("✅ File uploaded successfully!")
    st.write("### 🔍 Preview", df.head())

    required_cols = {'product_id', 'price', 'units_sold', 'date'}
    if required_cols.issubset(df.columns):

        col1, col2 = st.columns(2)

        # Optional category filter
        if 'category' in df.columns:
            with col1:
                category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['category'].dropna().unique()))
                if category_filter != 'All':
                    df = df[df['category'] == category_filter]

        with col2:
            product_filter = st.selectbox("Select Product ID", sorted(df['product_id'].dropna().unique()))
            df = df[df['product_id'] == product_filter]

        # KPIs
        total_units = int(df["units_sold"].sum())
        total_revenue = float((df["price"] * df["units_sold"]).sum())
        avg_price = float(df["price"].mean())

        st.markdown("### 📊 Key Metrics")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Total Units Sold", value=f"{total_units:,}")
        kpi2.metric(label="Total Revenue (₹)", value=f"₹ {total_revenue:,.0f}")
        kpi3.metric(label="Average Price", value=f"₹ {avg_price:,.0f}")

        # Forecast toggle
        forecast_days = 0
        forecast = st.checkbox("🔮 Enable Sales Forecasting")
        if forecast:
            forecast_days = st.slider("Select how many future days to predict", 7, 90, 30)

        # Chart
        df = df.dropna(subset=['date', 'units_sold'])
        df = df.sort_values('date')
        df['date_ordinal'] = df['date'].map(pd.Timestamp.toordinal)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['date'], y=df['units_sold'], name="Units Sold"))

        if forecast and len(df) > 1:
            # Prepare model
            X = df[['date_ordinal']]
            y = df['units_sold']
            model = LinearRegression().fit(X, y)

            last_date = df['date'].max()
            future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=forecast_days)
            future_ordinals = future_dates.map(pd.Timestamp.toordinal)
            predictions = model.predict(future_ordinals.to_numpy().reshape(-1, 1))

            # Plot prediction line
            fig.add_trace(go.Scatter(x=future_dates, y=predictions, mode='lines+markers',
                                     name='Predicted Units Sold', line=dict(dash='dot')))

        fig.update_layout(
            title=f"📈 Sales Trend for Product {product_filter}",
            xaxis_title="Date",
            yaxis_title="Units Sold",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"❌ Missing columns: {required_cols - set(df.columns)}")

else:
    st.info("📁 Please upload a CSV file to begin.")
