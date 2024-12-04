from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model =genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(inpout,image,promt):
    response=model.generate_content([input,image[0],promt])
    return response.text
st.set_page_config(page_title="Gemini Multi-lang invoice extractor")
st.header("Gemini Application")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_part=[
            {
                "mime_type" :uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_part

input=st.text_input("input prompt:",key="input")
upload_file = st.file_uploader("choose an image of the invoice:",type=['jpg','png','jpeg'])

image=""
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image,caption="uploaded Image",use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expoert in understanind invoices. We will upload an image as invoice and you will first check it that it is invoice or not and after checking you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data=input_image_setup(upload_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is :")
    st.write(response)

