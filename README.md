# Automated Resume Relevance Check System

This project contains a complete, hackathon-ready **AI-first** system for automatically checking the relevance of a resume against a job description.

### Problem Statement

At Innomatics Research Labs, resume evaluation is a manual, inconsistent, and time-consuming process. This leads to delays in shortlisting candidates and a high workload for the placement team. This system solves this problem by providing a fast, scalable, and consistent way to evaluate resumes, ensuring high-quality shortlists for hiring companies.

### Approach

The system uses a **hybrid approach** to evaluate resumes, combining both hard and soft matching techniques.

* **Hard Matching:** Uses keyword checks (TF-IDF, BM25) to identify specific skills and keywords from both documents.
* **Soft Matching:** Employs a **Large Language Model (LLM)** like Gemini to perform semantic matching and generate embeddings. This allows the system to understand skills and concepts even if the exact keywords are not present.

The final **Relevance Score (0-100)** is a weighted combination of these two approaches. The system also provides a suitability verdict and personalized feedback for improvement.

### Structure

The project is organized into the following key files and folders:

* `app_streamlit.py`: The Streamlit web application demo.
* `resume_parser.py`: Code for extracting text from resume files (PDF/DOCX/TXT).
* `jd_parser.py`: Logic for parsing job descriptions and extracting keywords.
* `relevance_score.py`: The core logic for hard and semantic scoring.
* `ai_feedback.py`: LLM prompt templates and helper functions for generating feedback.
* `vector_store.py`: Helper script for vector store integration (e.g., FAISS/Chroma).
* `chain_orchestration.py`: An example of using LangChain for LLM workflows.
* `db.py`: A simple helper for SQLite database storage.
* `sample_data/`: A folder containing sample resumes and JDs for testing.
* `requirements.txt`: The list of Python libraries required for the project.

### Installation & Usage

To set up and run the application locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Praveenkammala/resume-checker-app.git](https://github.com/Praveenkammala/resume-checker-app.git)
    cd resume-checker-app
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set your API key:**
    The application requires an API key for the LLM. Set your Gemini API key as an environment variable in the same terminal session.
    * On Windows: `set GEMINI_API_KEY="your_api_key_here"`
    * On macOS/Linux: `export GEMINI_API_KEY="your_api_key_here"`
5.  **Run the application:**
    ```bash
    streamlit run app_streamlit.py
    ```
    This will open the application in your web browser, where you can upload resumes and job descriptions for evaluation.

### Live Application

You can view the live application here: [Resume Relevance Checker](https://praveenkammala-resume-checker-app-app-streamlit-lr2jdq.streamlit.app/)
