from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
from pdf2image import convert_from_bytes
import io
import base64

# Configure GenerativeAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini responses
def get_gemini_responses(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to setup PDF input
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Streamlit App
st.set_page_config(page_title="StealthAI", layout="wide")

# Header
st.title("Stealth AI: The Content Summarizer & Anti-AI Detection System")
st.markdown("---")

# Sidebar
st.sidebar.title("Options")
input_text = st.sidebar.text_area("Domain:", key="input")
uploaded_file = st.sidebar.file_uploader("Upload your document (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.write("PDF Uploaded Successfully")
else:
    st.sidebar.write("Upload a PDF to get started.")

# Main content area
st.subheader("Select an action:")
col1, col2, col3 = st.columns(3)

# Card 1: Summarize Content
input_prompt1 = """
    You are an experienced AI agent and your task is to review the provided content based on the provided Domain and input and summarise it. The summarised content size should not be more than 30 percent of the original content. 
    You can use professional English and can also improvise the content quality while summarising. It is totally up to you.
"""

input_prompt2 = """
    You are a skilled Plagirism Detection System scanner with a deep understanding of plagirism. Based on the content, give me the percentage of plagirism of the content detected. 
"""

input_prompt3 = """
    You are an experienced AI agent. Your role is to scrutinize the provided content and completely eliminate plagirism and AI Detection and provide a content which looks professional and should stick to the original context.
"""

with col1:
    st.markdown("<h4 style='text-align: center;'>Summarize Content</h4>", unsafe_allow_html=True)
    if st.button("Summarise my content"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_responses(input_text, pdf_content, input_prompt1)
            st.write("### Content Summary:")
            st.write(response)
        else:
            st.warning("Please upload a PDF file")

# Card 2: Plagiarism Percentage
with col2:
    st.markdown("<h4 style='text-align: center;'>Plagiarism Detection</h4>", unsafe_allow_html=True)
    if st.button("Check Plagiarism Percentage"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_responses(input_text, pdf_content, input_prompt2)
            st.write("### Plagiarism Percentage:")
            st.write(response)
        else:
            st.warning("Please upload a PDF file")

# Card 3: Anti-AI Detection
with col3:
    st.markdown("<h4 style='text-align: center;'>Make it Stealthy?</h4>", unsafe_allow_html=True)
    if st.button("Apply Anti-AI Detection"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_responses(input_text, pdf_content, input_prompt3)
            st.write("### Undetectable Content🤫:")
            st.write(response)
        else:
            st.warning("Please upload a PDF file")

# Footer
st.markdown("---")
st.write("© 2024 StealthAI. All rights reserved.")





        
    