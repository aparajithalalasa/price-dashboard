import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Product Sales Dashboard")

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

        # Optional filter: Category
        if 'category' in df.columns:
            with col1:
                category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['category'].dropna().unique()))
                if category_filter != 'All':
                    df = df[df['category'] == category_filter]

        with col2:
            product_filter = st.selectbox("Select Product ID", sorted(df['product_id'].dropna().unique()))
            df = df[df['product_id'] == product_filter]

        # KPIs / Summary cards
        total_units = int(df["units_sold"].sum())
        total_revenue = float((df["price"] * df["units_sold"]).sum())
        avg_price = float(df["price"].mean())

        st.markdown("### 📊 Key Metrics")

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Total Units Sold", value=f"{total_units:,}")
        kpi2.metric(label="Total Revenue (₹)", value=f"₹ {total_revenue:,.0f}")
        kpi3.metric(label="Average Price", value=f"₹ {avg_price:,.0f}")

        # Chart
        df = df.sort_values('date')
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['date'], y=df['units_sold'], name="Units Sold"))
        fig.add_trace(go.Scatter(x=df['date'], y=df['price'], yaxis="y2", name="Price", mode="lines+markers"))

        fig.update_layout(
            title=f"📈 Sales & Price Trends for Product {product_filter}",
            xaxis_title="Date",
            yaxis=dict(title="Units Sold"),
            yaxis2=dict(title="Price", overlaying="y", side="right"),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"❌ Missing columns: {required_cols - set(df.columns)}")

else:
    st.info("📁 Please upload a CSV file to begin.")
