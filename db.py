
import sqlite3
from typing import Dict, Any

DB_PATH = 'results.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_name TEXT,
        jd_name TEXT,
        score REAL,
        verdict TEXT,
        missing_skills TEXT,
        suggestions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def save_evaluation(resume_name: str, jd_name: str, score: float, verdict: str, missing_skills: str, suggestions: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO evaluations (resume_name, jd_name, score, verdict, missing_skills, suggestions) VALUES (?,?,?,?,?,?)',
                (resume_name, jd_name, score, verdict, missing_skills, suggestions))
    conn.commit()
    conn.close()
