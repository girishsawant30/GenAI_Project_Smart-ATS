from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import PyPDF2
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
  model = genai.GenerativeModel("gemini-pro")
  responses = model.generate_content(
    [input, pdf_content[0], prompt],
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32
    }
  )
  return responses.text

def input_pdf_setup(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

    return text


## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("% Match & How Can I Improvise my Skills")

#submit3 = st.button("What are the keywords that are missing")

#submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager with a deep understanding of any one job role from data science, full stack, DevOps, Data Analyst, Big Data Engineering, Web Development, database administrator & your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the Top 5 strengths and weaknesses of the applicant in relation to the specified job requirements in the following format. Be strict with the resume matching and should thoroughly analyze the job description and my resume to give accurate answer only.

 Strenghts :- 

 Weakness :-

 Overall Comments :- (it should be less thatn 300 words)
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from data science, full stack, DevOps, Data Analyst, Big Data Engineering, Web Development , database administrator and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.
Be strict with the resume matching and should thoroughly analyze the job description and my resume to give accurate answer only
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
      response=get_gemini_response(input_prompt2, pdf_content, input_text)
      st.subheader("The Response is")
      st.write(response)
   else:
      st.write("Please upload the resume")
