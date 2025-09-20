import streamlit as st
from resume_parser import extract_resume_text
from jd_parser import extract_skills_from_jd
from relevance_score import keyword_hard_score, semantic_similarity_score, combined_score
from ai_feedback import build_prompt_for_feedback, call_openai_for_feedback
from db import init_db, save_evaluation
import os
import json

st.set_page_config(page_title='Resume Relevance Checker', layout='wide')

st.title('Automated Resume Relevance Check System - Demo')

st.sidebar.header('Upload Files')
uploaded_jd = st.sidebar.file_uploader('Upload Job Description (TXT or PDF)', type=['txt', 'pdf'])
uploaded_resume = st.sidebar.file_uploader('Upload Resume (TXT, PDF, DOCX)', type=['txt', 'pdf', 'docx'])

if st.sidebar.button('Run Evaluation'):
    if not uploaded_jd or not uploaded_resume:
        st.sidebar.error('Please upload both JD and Resume files.')
    else:
        # Create a temporary directory to store uploaded files
        temp_dir = 'uploaded_files_temp'
        os.makedirs(temp_dir, exist_ok=True)

        # Define the full paths for the uploaded files
        jd_path = os.path.join(temp_dir, uploaded_jd.name)
        resume_path = os.path.join(temp_dir, uploaded_resume.name)

        # Save the uploaded files to the temporary directory
        try:
            with open(jd_path, 'wb') as f:
                f.write(uploaded_jd.getbuffer())
            with open(resume_path, 'wb') as f:
                f.write(uploaded_resume.getbuffer())
        except Exception as e:
            st.error(f"Failed to save uploaded files: {e}")
            st.stop()

        jd_text = ''
        resume_text = ''

        # simple extraction for txt/jd
        if jd_path.lower().endswith('.txt'):
            with open(jd_path, 'r', encoding='utf-8', errors='ignore') as f:
                jd_text = f.read()
        else:
            # try pdf
            try:
                jd_text = extract_resume_text(jd_path)
            except Exception as e:
                st.error('Unable to extract JD text: ' + str(e))
                jd_text = ''

        try:
            resume_text = extract_resume_text(resume_path)
        except Exception as e:
            st.error('Unable to extract resume text: ' + str(e))

        st.subheader('Parsed JD')
        st.write(jd_text[:1000] + ('...' if len(jd_text) > 1000 else ''))

        st.subheader('Parsed Resume')
        st.write(resume_text[:1000] + ('...' if len(resume_text) > 1000 else ''))

        # extract jd skills
        skills = extract_skills_from_jd(jd_text)
        st.write('**Extracted JD skills**', skills)

        # compute hard score
        hard = keyword_hard_score(skills.get('must_have', []), resume_text)
        st.write('Hard match (must-have) score (0-1):', round(hard, 3))

        # semantic score
        try:
            semantic = semantic_similarity_score(jd_text, resume_text)
            st.write('Semantic similarity (0-1):', round(semantic, 3))
        except Exception as e:
            st.warning('Semantic similarity could not be computed: ' + str(e))
            semantic = 0.0

        combined = combined_score(hard, semantic, hard_weight=0.5, semantic_weight=0.5)
        final_score_0_100 = int(combined * 100)
        st.metric('Relevance Score (0-100)', final_score_0_100)

        verdict = 'Low'
        if final_score_0_100 >= 75:
            verdict = 'High'
        elif final_score_0_100 >= 50:
            verdict = 'Medium'

        st.write('Verdict:', verdict)

        # call LLM for detailed suggestions (optional - requires API keys + openai)
        try:
            prompt = build_prompt_for_feedback(jd_text, resume_text)
            feedback = call_openai_for_feedback(prompt)
            st.subheader('LLM Feedback (structured)')
            st.json(feedback)
            suggestions = feedback.get('suggestions') if isinstance(feedback, dict) else []
            missing = feedback.get('missing_skills') if isinstance(feedback, dict) else []
        except Exception as e:
            st.info('LLM feedback not available: ' + str(e))
            suggestions = []
            missing = []

        # save to sqlite
        try:
            init_db()
            save_evaluation(uploaded_resume.name, uploaded_jd.name, final_score_0_100, verdict, ','.join(missing),
                            json.dumps(suggestions))
            st.success('Evaluation saved to local SQLite DB (results.db).')
        except Exception as e:
            st.warning('Could not save to DB: ' + str(e))

        # Clean up temporary files after use
        try:
            # First, remove the individual files
            os.remove(jd_path)
            os.remove(resume_path)
            # Now, remove the empty directory
            os.rmdir(temp_dir)
        except OSError as e:
            st.warning(f"Error cleaning up temporary files: {e.strerror}")