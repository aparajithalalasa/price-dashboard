import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(layout="wide")
st.title("📊 Dashboard: Product Sales Overview")

# Sidebar - About Me
st.sidebar.header("👩‍💼 About Me")
st.sidebar.markdown("""
**Aparajitha Lalasa Molugu**  
Data Analyst | 5+ Yrs Exp at Amazon  
📍 Hyderabad, India  
📧 [Email](mailto:youremail@example.com)  
🔗 [LinkedIn](https://linkedin.com/in/yourprofile)  
💻 [GitHub](https://github.com/yourusername)
""")

# Download resume from raw GitHub
resume_url = "https://raw.githubusercontent.com/aparajitha-lalasa/price-dashboard/main/Aparajitha_Resume.pdf"
try:
    response = requests.get(resume_url)
    if response.status_code == 200:
        st.sidebar.download_button("📄 Download Resume", response.content, "Aparajitha_Resume.pdf", mime="application/pdf")
except:
    st.sidebar.warning("⚠️ Resume not available.")

# Upload and cache file in session state
uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    st.session_state["df"] = df
    st.success("✅ File uploaded successfully!")
elif "df" in st.session_state:
    df = st.session_state["df"]
else:
    st.info("📁 Please upload a CSV file to begin.")
    st.stop()

st.write("### 🔍 Preview", df.head())

# Required columns
required_cols = {'product_id', 'price', 'units_sold', 'date'}
if not required_cols.issubset(df.columns):
    st.error(f"❌ Missing columns: {required_cols - set(df.columns)}")
    st.stop()

# Filters
col1, col2 = st.columns(2)
if 'category' in df.columns:
    with col1:
        category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['category'].dropna().unique()))
        if category_filter != 'All':
            df = df[df['category'] == category_filter]
with col2:
    product_filter = st.selectbox("Select Product ID", sorted(df['product_id'].dropna().unique()))
    df = df[df['product_id'] == product_filter]

# KPIs
st.markdown("### 📊 Key Metrics")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Units Sold", f"{int(df['units_sold'].sum()):,}")
kpi2.metric("Total Revenue (₹)", f"₹ {(df['price'] * df['units_sold']).sum():,.0f}")
kpi3.metric("Average Price", f"₹ {df['price'].mean():,.0f}")

# Forecast toggle
forecast = st.checkbox("🔮 Enable Sales Forecasting")
forecast_days = st.slider("Days to Forecast", 7, 90, 30) if forecast else 0

# Line chart + forecast
if not df.empty:
    df = df.dropna(subset=['date', 'units_sold'])
    df = df.sort_values('date')
    df['date_ordinal'] = df['date'].map(pd.Timestamp.toordinal)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['date'], y=df['units_sold'], name="Units Sold"))

    if forecast and len(df) > 1:
        from sklearn.linear_model import LinearRegression
        import numpy as np
        X = df[['date_ordinal']]
        y = df['units_sold']
        model = LinearRegression().fit(X, y)
        last_date = df['date'].max()
        future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=forecast_days)
        future_ordinals = future_dates.map(pd.Timestamp.toordinal)
        predictions = model.predict(future_ordinals.to_numpy().reshape(-1, 1))
        fig.add_trace(go.Scatter(x=future_dates, y=predictions, mode='lines+markers',
                                 name='Forecast', line=dict(dash='dot')))

    fig.update_layout(title=f"📈 Sales Trend for Product {product_filter}",
                      xaxis_title="Date", yaxis_title="Units Sold", height=500)
    st.plotly_chart(fig, use_container_width=True)
