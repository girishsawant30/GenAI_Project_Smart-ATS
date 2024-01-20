import streamlit as st
from PIL import Image
import pdf2image
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

from dotenv import load_dotenv
load_dotenv()
import os
import base64
import io



import google.generativeai as genai
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
#or genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
  model = genai.GenerativeModel("gemini-pro-vision")
  responses = model.generate_content(
    [input, pdf_content[0], prompt],
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32
    },
  stream=True,
  )
  
  for response in responses:
     print(response.text, end="")

def input_pdf_setup(uploaded_file):
   if uploaded_file is not None:  
   ## Convert the PDF to image
      images=pdf2image.convert_from_bytes(uploaded_file.read())
      first_page=images[0]
   #Convert to Bytes
      img_byte_arr = io.BytesIO()
      first_page.save(img_byte_arr, format='JPEG')
      img_byte_arr = img_byte_arr.getvalue()

      pdf_parts = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
            ]
      return pdf_parts 
   else:
     raise FileNotFoundError("No file uploaded")

#Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description:", key=input)
uploaded_file=st.file_uploader("Upload your Resume(PDF)...", type=['pdf'])

if uploaded_file is not None:
   st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my Skills")

#submit3 = st.button("What are the keywords that are missing")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager with a deep understanding of of any one job role from data science, full stack, DevOps, Data Analyst, Big Data Engineering, Web Development, database administrator & your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from data science, full stack, DevOps, Data Analyst, Big Data Engineering, Web Development , database administrator and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
   if uploaded_file is not None:
      pdf_content=input_pdf_setup(uploaded_file)
      response=get_gemini_response(input_prompt1, pdf_content, input_text)
      st.subheader("The Response is")
      st.write(response)
   else:
      st.write("Please upload the resume")

elif submit2:
   if uploaded_file is not None:
      pdf_content=input_pdf_setup(uploaded_file)
      response=get_gemini_response(input_prompt3, pdf_content, input_text)
      st.subheader("The Response is")
      st.write(response)
   else:
      st.write("Please upload the resume")

elif submit3:
   if uploaded_file is not None:
      pdf_content=input_pdf_setup(uploaded_file)
      response=get_gemini_response(input_prompt1, pdf_content, input_text)
      st.subheader("The Response is")
      st.write(response)
   else:
      st.write("Please upload the resume")