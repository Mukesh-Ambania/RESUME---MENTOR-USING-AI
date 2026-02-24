from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

# Ensure API key exists
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)


def analyze_resume(resume_text):

    prompt = f"""
    You are an expert AI Career Mentor.

    Analyze the following resume carefully and generate a structured report:

    1. Resume Score (out of 100)
    2. Strengths
    3. Weaknesses
    4. Suitable Career Roles
    5. Skill Gap Analysis
    6. 6-Month Learning Roadmap
    7. Resume Improvement Suggestions

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ Updated model
        messages=[
            {"role": "system", "content": "You are a professional career advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1500
    )

    result = response.choices[0].message.content

    # Extract score like "85/100"
    score_match = re.search(r'(\d{1,3})\s*/\s*100', result)
    score = int(score_match.group(1)) if score_match else 75

    return result, score


def chatbot_response(user_message):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ Updated model
        messages=[
            {"role": "system", "content": "You are a friendly AI Career Mentor."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content