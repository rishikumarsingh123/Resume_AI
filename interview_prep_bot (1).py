"""
Resume Interview Prep Bot  (LangChain + Gemini + Streamlit)

Upload your resume PDF + paste a job description.
The app generates tailored interview questions and tips.

Setup:
    pip install langchain langchain-community langchain-google-genai pypdf streamlit
    set GOOGLE_API_KEY=your_key      (Windows)   |   export GOOGLE_API_KEY=your_key  (Linux/Mac)
    streamlit run interview_prep_bot.py
"""

import tempfile

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Change to whichever Gemini model is current in Google AI Studio
MODEL_NAME = "gemini-2.5-flash"

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strict but helpful technical interviewer for SDE roles. "
     "Use ONLY the resume and job description provided."),
    ("human",
     "RESUME:\n{resume}\n\nJOB DESCRIPTION:\n{jd}\n\n"
     "Generate:\n"
     "1. 5 technical questions based on projects/skills in the resume\n"
     "2. 3 DSA/CS-fundamentals questions relevant to the job description\n"
     "3. 2 HR/behavioural questions\n"
     "4. Top 3 skill gaps between resume and job description, with what to study\n"),
])

# LCEL chain: prompt -> model -> plain text
chain = prompt | ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.4) | StrOutputParser()


def load_pdf_text(uploaded_file) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name
    pages = PyPDFLoader(path).load()
    return "\n".join(p.page_content for p in pages)


st.title("Resume Interview Prep Bot")
pdf = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd = st.text_area("Paste the job description", height=200)

if st.button("Generate questions") and pdf and jd.strip():
    with st.spinner("Thinking..."):
        resume_text = load_pdf_text(pdf)
        st.markdown(chain.invoke({"resume": resume_text, "jd": jd}))
