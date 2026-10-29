# Resume Interview Prep Bot

An LLM-powered web app that reads your resume and a job description, then generates tailored interview questions and a skill-gap analysis.
## Features

- Upload your resume as a PDF
- Paste any job description
- Get 5 technical questions based on your projects and skills
- Get 3 DSA / CS-fundamentals questions relevant to the role
- Get 2 HR / behavioural questions
- Get your top 3 skill gaps, with what to study

## Tech Stack

- **Python**
- **LangChain** (prompt templates, LCEL chains, PDF loader)
- **Google Gemini API** (LLM)
- **Streamlit** (web UI)
- **PyPDF** (PDF parsing)

## How It Works

1. The uploaded PDF is parsed into text with LangChain's `PyPDFLoader`.
2. The resume text and job description are inserted into a `ChatPromptTemplate`.
3. A LangChain chain (`prompt | model | output parser`) sends the prompt to Gemini.
4. The response is shown in the Streamlit app.

## Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/rishikumarsingh123/interview-prep-bot.git
   cd interview-prep-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a free API key from [Google AI Studio](https://aistudio.google.com/) and set it:
   ```bash
   # Windows (Command Prompt)
   set GOOGLE_API_KEY=your_key_here

   # Linux / macOS
   export GOOGLE_API_KEY=your_key_here
   ```

4. Start the app:
   ```bash
   streamlit run interview_prep_bot.py
   ```

## Deployment

Deployed on Streamlit Community Cloud. To deploy your own copy:

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app from the repo.
3. Under **Advanced settings → Secrets**, add:
   ```
   GOOGLE_API_KEY = "your_key_here"
   ```

## Privacy

Uploaded resumes are read only for the current session and are not stored.

## Future Improvements

- Download the generated questions as a PDF
- Add RAG with FAISS to answer questions from your own notes
- Score your answers to the generated questions

## Author

**Rishi Kumar Singh**
B.Tech Electrical Engineering, NIT Durgapur
[GitHub](https://github.com/rishikumarsingh123)
