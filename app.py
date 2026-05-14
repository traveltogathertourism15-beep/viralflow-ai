import streamlit as st
import google.generativeai as genai

# Website ki setting
st.set_page_config(page_title="ViralFlow AI", page_icon="🚀")

# Design theek kiya gaya hai
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #ffffff; color: #000000; }
    .stTextInput input { border: 2px solid #007bff !important; }
    h1 { color: #007bff !important; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 ViralFlow AI")
st.write("Kamran Ali ka apna Viral Content Generator")

# API Key aur Settings
api_key = st.text_input("1. Apni Gemini API Key yahan dalein:", type="password")
lang = st.selectbox("2. Zaban select karein:", ["Roman Urdu", "Pure Urdu", "English"])

st.divider()

# Input Topic
topic = st.text_input("3. Video ka topic likhein:", placeholder="maslan: Mobile se paise kaise kamayein")

if st.button("Generate Script"):
    if not api_key:
        st.error("Bhai, pehle API Key dalein!")
    elif not topic:
        st.warning("Pehle koi topic to likhein.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"Write a viral social media script in {lang} about: {topic}. Include a hook and CTA."
            
            with st.spinner('AI likh raha hai...'):
                response = model.generate_content(prompt)
                st.success("Tayar hai!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("ViralFlow AI v2.0 - Powered by Kamran Ali")
