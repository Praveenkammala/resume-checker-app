# Automated Resume Relevance Check System - Hackathon MVP

This project contains a complete hackathon-ready **AI-first** Resume Relevance Check System:
- Resume & JD parsing
- Hybrid scoring: hard (keyword) + semantic (embeddings)
- Vector store (FAISS/Chroma) integration for scale
- LangChain orchestration example for LLM-driven feedback
- Streamlit demo UI (MVP)
- SQLite storage for results
- Sample dataset (text resumes & job descriptions)

## Structure
- `app_streamlit.py` - Streamlit demo application
- `resume_parser.py` - Resume text extraction (PDF/DOCX/TXT)
- `jd_parser.py` - Job description parsing & keyword extraction
- `relevance_score.py` - Hard + semantic scoring logic (embeddings)
- `ai_feedback.py` - LLM prompt templates and helper for feedback
- `vector_store.py` - Vector store helper (FAISS/Chroma)
- `chain_orchestration.py` - LangChain orchestration example (optional)
- `db.py` - Simple SQLite storage helper
- `sample_data/` - Sample resumes and JDs (TXT)
- `report.md` - Project report (editable)
- `README.md`, `requirements.txt`

## How to run (recommended)
1. Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set any API keys (if using OpenAI):
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
3. Run the Streamlit demo:
   ```bash
   streamlit run app_streamlit.py
   ```

## Notes
- The code is a **complete template**. For offline semantic similarity, `sentence-transformers` is used.
- For large scale production, use Chroma or FAISS (helpers included).
- LangChain integration is optional for the hackathon MVP; it's provided as an example orchestration script.