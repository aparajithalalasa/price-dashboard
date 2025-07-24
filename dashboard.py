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
uploaded_file = st.file_
