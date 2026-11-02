"""
Resume Interview Prep Bot  (LangChain + Gemini + Streamlit)

Upload your resume PDF + paste a job description.
The app generates tailored interview questions and tips.

Python 3.15 notes:
  - Uses only pure-Python code on our side; no temp files, no langchain-community.
  - PDF reading uses pypdf directly (pure Python), which avoids a heavy dependency.

Setup (use a fresh virtual environment):
    python3.15 -m venv .venv
    source .venv/bin/activate            (Windows: .venv\\Scripts\\activate)
    pip install -U pip
    pip install -U langchain-core langchain-google-genai pypdf streamlit
    export GOOGLE_API_KEY=your_key       (Windows: set GOOGLE_API_KEY=your_key)
    streamlit run interview_prep_bot.py
"""

import os
from io import BytesIO

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader

# Change to whichever Gemini model is current in Google AI Studio
MODEL_NAME = "gemini-2.5-flash"

PROMPT = ChatPromptTemplate.from_messages([
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


@st.cache_resource
def get_chain():
    """Build the LCEL chain once: prompt -> model -> plain text."""
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.4)
    return PROMPT | llm | StrOutputParser()


def load_pdf_text(uploaded_file) -> str:
    """Extract text from an uploaded PDF fully in memory."""
    reader = PdfReader(BytesIO(uploaded_file.getvalue()))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()


def main() -> None:
    st.title("Resume Interview Prep Bot")

    if not os.environ.get("GOOGLE_API_KEY"):
        st.error("GOOGLE_API_KEY is not set. Set it and restart the app.")
        st.stop()

    pdf = st.file_uploader("Upload your resume (PDF)", type="pdf")
    jd = st.text_area("Paste the job description", height=200)

    if st.button("Generate questions"):
        if not pdf or not jd.strip():
            st.warning("Please upload a resume PDF and paste a job description.")
            return

        with st.spinner("Thinking..."):
            resume_text = load_pdf_text(pdf)
            if not resume_text:
                st.error(
                    "No text found in this PDF (it may be a scanned image). "
                    "Please upload a text-based PDF."
                )
                return
            try:
                result = get_chain().invoke({"resume": resume_text, "jd": jd})
            except Exception as exc:  # network / quota / bad key
                st.error(f"Generation failed: {exc}")
                return
        st.markdown(result)


if __name__ == "__main__":
    main()
else:
    # Streamlit executes the script as a module, so run the UI directly.
    main()
