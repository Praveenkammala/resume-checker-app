import openai
from openai import OpenAI
import json

def build_prompt_for_feedback(jd_text, resume_text):
    prompt_template = """
    You are an AI career consultant. Your task is to provide feedback on how a resume matches a job description.
    
    Here is the Job Description:
    {jd_text}
    
    Here is the Resume:
    {resume_text}
    
    Analyze the resume against the job description and provide structured feedback in a single JSON object.
    
    The JSON object must have the following keys:
    1. "suggestions": A list of up to 3 specific suggestions on how to improve the resume for this job. Each suggestion should be a concise string.
    2. "missing_skills": A list of specific skills mentioned in the job description that are not clearly present in the resume.
    
    Example JSON format:
    {{
      "suggestions": [
        "Suggestion 1",
        "Suggestion 2",
        "Suggestion 3"
      ],
      "missing_skills": [
        "Skill A",
        "Skill B"
      ]
    }}
    """
    return prompt_template.format(jd_text=jd_text, resume_text=resume_text)

def call_openai_for_feedback(prompt):
    client = OpenAI()  # Initializes the client using the OPENAI_API_KEY environment variable
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or another model like "gpt-4" if you have access
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    # Access the content from the new response object structure
    feedback_text = response.choices[0].message.content
    return json.loads(feedback_text)