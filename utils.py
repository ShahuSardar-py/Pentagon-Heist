import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
st.set_page_config(page_title="hello")




response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents="Explain how AI works"
)
st.write(response)