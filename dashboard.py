import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Product Sales Dashboard with Filters")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert 'date' column to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    st.success("✅ File uploaded!")
    st.write("### 🔍 Preview", df.head())

    required_cols = {'product_id', 'price', 'units_sold', 'date'}
    if required_cols.issubset(df.columns):

        # Optional filters (only shown if column exists)
        col1, col2 = st.columns(2)

        with col1:
            if 'category' in df.columns:
                category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['category'].dropna().unique().tolist()))
                if category_filter != 'All':
                    df = df[df['category'] == category_filter]

        with col2:
            product_filter = st.selectbox("Select Product ID", sorted(df['product_id'].dropna().unique().tolist()))
            df = df[df['product_id'] == product_filter]

        # Plot
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
        st.error(f"Missing columns: {required_cols - set(df.columns)}")

else:
    st.info("📁 Please upload a CSV file to begin.")
