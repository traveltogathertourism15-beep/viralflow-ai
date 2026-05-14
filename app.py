import streamlit as st
import google.generativeai as genai

# Website Appearance
st.set_page_config(page_title="ViralFlow AI Pro", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(to bottom, #ffffff, #e3f2fd); color: #1e1e1e; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; font-weight: bold; height: 3em; }
    .stTextInput>div>div>input { border-radius: 10px; border: 2px solid #007bff !important; }
    .output-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

st.title("⚡ ViralFlow AI Pro")
st.write("---")

# Setup Section
api_key = st.text_input("🔑 Enter Gemini API Key", type="password")
lang = st.selectbox("🌍 Select Language", ["Roman Urdu", "Pure Urdu", "English"])

# Input Section
topic = st.text_input("📝 Video Topic", placeholder="e.g., How to earn money online")

if st.button("Generate Viral Script"):
    if not api_key:
        st.error("Please enter your API Key first!")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            genai.configure(api_key=api_key)
            # Naya Model Name jo 2026 mein stable hai
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            
            prompt = f"Create a viral, high-retention social media video script about '{topic}' in {lang}. Include a hook, body, and CTA."
            
            with st.spinner('AI is generating...'):
                response = model.generate_content(prompt)
                st.success("Success!")
                st.markdown(f'<div class="output-card">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")
st.caption("Developed by Kamran Ali | v3.0")
