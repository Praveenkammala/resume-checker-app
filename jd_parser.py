"""jd_parser.py
Simple JD parsing to extract must-have and good-to-have skills using heuristics.
This version is more robust, handling common list formats and keywords.
"""
import re

def extract_skills_from_jd(jd_text: str) -> dict:
    # Use a set for faster lookups
    tech_skills = {
        'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'sql', 'nosql', 'go',
        'ruby', 'php', 'swift', 'kotlin', 'scala', 'rust', 'html', 'css', 'react',
        'angular', 'vue', 'nodejs', 'express', 'flask', 'django', 'spring', 'aws',
        'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins',
        'ci/cd', 'git', 'github', 'gitlab', 'svn', 'linux', 'unix', 'windows server',
        'microservices', 'rest api', 'graphql', 'mongodb', 'postgresql', 'mysql',
        'oracle', 'redis', 'spark', 'hadoop', 'kafka', 'airflow', 'scikit-learn',
        'tensorflow', 'pytorch', 'nlp', 'machine learning', 'data science', 'pandas',
        'numpy', 'matplotlib', 'seaborn', 'agile', 'scrum', 'jira', 'confluence'
    }

    # Normalize text for easier parsing
    jd_text_lower = jd_text.lower().replace('\r', '\n')
    
    must_have_skills = []
    good_to_have_skills = []
    
    # 1. Look for explicit sections with keywords
    must_have_section_keywords = ['must have', 'required skills', 'qualifications', 'requirements', 'core skills']
    good_to_have_section_keywords = ['good to have', 'nice to have', 'preferred skills', 'bonus points']
    
    jd_sections = re.split(r'(\n\s*(?:' + '|'.join(must_have_section_keywords + good_to_have_section_keywords) + r')\s*[:\n])', jd_text_lower, flags=re.IGNORECASE)
    
    current_section = None
    for part in jd_sections:
        part_clean = part.strip()
        if not part_clean:
            continue
        
        if any(keyword in part_clean for keyword in must_have_section_keywords):
            current_section = 'must'
            continue
        elif any(keyword in part_clean for keyword in good_to_have_section_keywords):
            current_section = 'good'
            continue
        
        # Split the section into lines and extract skills
        for line in part.split('\n'):
            line_clean = line.strip().lower()
            if line_clean.startswith(('•', '*', '-')): # Handle bullet points
                line_clean = line_clean[1:].strip()
                
            # Find a match from our predefined list
            found_skills = [skill for skill in tech_skills if re.search(r'\b' + re.escape(skill) + r'\b', line_clean)]
            
            if current_section == 'must':
                must_have_skills.extend(found_skills)
            elif current_section == 'good':
                good_to_have_skills.extend(found_skills)
                
    # 2. Fallback: If sections are not found, search the entire text
    if not must_have_skills and not good_to_have_skills:
        for skill in tech_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', jd_text_lower):
                must_have_skills.append(skill) # Treat all found skills as must-haves if no sections are defined

    return {
        'must_have': sorted(list(set(must_have_skills))),
        'good_to_have': sorted(list(set(good_to_have_skills)))
    }