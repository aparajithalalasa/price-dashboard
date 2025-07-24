import streamlit as st
import requests

st.title("👩‍💼 About Me")

st.markdown("""
**Aparajitha Lalasa Molugu**  
Senior Data Analyst | 5+ Years @ Amazon  
📍 Hyderabad, India
📧 [Email me](mailto:aparajitha.lalasa@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/aparajitha-molugu-22543515a/)  
💻 [GitHub](https://github.com/aparajithalalasa)
""")

resume_url = "https://raw.githubusercontent.com//aparajithalalasa/price-dashboard/main/Aparajitha_Lalasa_Molugu_Updated_Resume.pdf"

try:
    response = requests.get(resume_url)
    if response.status_code == 200:
        st.download_button("📄 Download Resume", response.content, "Aparajitha_Resume.pdf", mime="application/pdf")
except:
    st.warning("Could not load resume.")
