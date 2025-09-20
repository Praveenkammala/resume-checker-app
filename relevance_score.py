
"""relevance_score.py
Contains functions to compute hard-match and semantic similarity scores.
Semantic embeddings use sentence-transformers (local) or OpenAI embeddings (optional).
"""
from typing import List, Tuple
import numpy as np

def keyword_hard_score(jd_skills: List[str], resume_text: str) -> float:
    # simple overlap: count how many must-have skills appear in resume_text
    resume_lower = resume_text.lower()
    if not jd_skills:
        return 0.0
    found = 0
    for skill in jd_skills:
        if skill.lower() in resume_lower:
            found += 1
    score = found / len(jd_skills)
    return float(score)  # range 0-1

def semantic_similarity_score(jd_text: str, resume_text: str, model=None) -> float:
    # If model is None, try to import sentence-transformers model inside
    if model is None:
        try:
            from sentence_transformers import SentenceTransformer, util
            model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            raise ImportError('Install sentence-transformers to compute embeddings or pass a model object') from e
    # encode
    emb_jd = model.encode(jd_text, convert_to_tensor=True)
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    sim = util.cos_sim(emb_jd, emb_resume).item()
    # clamp and return 0-1
    return max(0.0, min(1.0, float(sim)))

def combined_score(hard: float, semantic: float, hard_weight: float = 0.5, semantic_weight: float = 0.5) -> float:
    s = hard_weight * hard + semantic_weight * semantic
    return float(s)  # 0-1
