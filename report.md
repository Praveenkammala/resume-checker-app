# Project Report: Automated Resume Relevance Check System

## Problem Statement
Resume shortlisting is time-consuming and inconsistent. This system automates evaluation against job descriptions, providing a relevance score (0-100), missing skill highlights, fit verdicts and actionable feedback.

## Proposed Solution
Hybrid approach:
- Hard matching of keywords
- Semantic matching using embeddings
- LLM-powered feedback + explanations
- Vector-store (FAISS/Chroma) for scalable semantic search

## Architecture
1. Upload JD & Resumes (PDF/DOCX/TXT)
2. Extract text and normalize sections
3. Extract must-have & good-to-have keywords from JD
4. Compute hard-match score (keyword overlap)
5. Compute semantic similarity (embeddings) and combine via weighted formula
6. Ask an LLM for gap analysis and improvement suggestions
7. Store results in SQLite and show dashboard

## Metrics & Evaluation
- Relevance Score (0-100)
- Classification thresholds: [0-50]=Low, (50-75]=Medium, (75-100]=High
- Evaluate on sample dataset (provided)

## Future Work
- Add OCR for image resumes
- Integrate additional LLM providers and privacy-preserving inference
- Multilingual support