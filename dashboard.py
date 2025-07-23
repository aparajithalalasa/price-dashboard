import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sample data
data = {
    'date': ['2024-01-01', '2024-01-15', '2024-01-01', '2024-01-15'],
    'product_id': [101, 101, 102, 102],
    'category': ['Mobile', 'Mobile', 'Laptop', 'Laptop'],
    'price': [70000, 65000, 80000, 80000],
    'units_sold': [200, 320, 50, 60]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

st.title("📊 Price vs Sales Dashboard")
st.markdown("Compare how price changes affect product sales.")

# Product selection
product_ids = df['product_id'].unique()
selected_product = st.selectbox("Select a Product ID", product_ids)

# Filter data for the selected product
filtered = df[df['product_id'] == selected_product].sort_values('date')
dates = filtered['date'].dt.strftime('%Y-%m-%d').tolist()

# Create figure
fig = go.Figure()

# Bar: Units sold
fig.add_trace(go.Bar(
    x=dates,
    y=filtered['units_sold'],
    name='Units Sold',
    marker_color='skyblue'
))

# Line: Price
fig.add_trace(go.Scatter(
    x=dates,
    y=filtered['price'],
    name='Price',
    yaxis='y2',
    mode='lines+markers',
    marker=dict(color='orange')
))

# Layout config
fig.update_layout(
    title=f"Product {selected_product} - Price vs Units Sold",
    xaxis_title="Date",
    yaxis=dict(title="Units Sold"),
    yaxis2=dict(
        title="Price",
        overlaying='y',
        side='right',
        showgrid=False
    ),
    height=500,
    legend=dict(x=0.5, y=1.15, orientation="h")
)

# Display chart
st.plotly_chart(fig, use_container_width=True)
