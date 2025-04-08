import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai
import requests

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def validate_topic(curriculum, grade, subject, topic):
    prompt = f"""
    As an expert curriculum validator for {grade} {subject} ({curriculum}), 
    evaluate this topic: '{topic}'
    
    Return ONLY one word:
    - "valid" - if perfectly matches subject and grade level
    - "irrelevant" - if doesn't match subject but is grade-appropriate
    - "harmful" - if inappropriate for grade
    
    Consider:
    1. Subject matter alignment
    2. Cognitive level for {grade}
    3. {curriculum} standards
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip().lower()

def suggest_topics(curriculum, grade, subject):
    prompt = f"""
    Suggest 3-5 perfect topics for:
    - Curriculum: {curriculum}
    - Grade: {grade}
    - Subject: {subject}
    
    Each must:
    - Be core curriculum items
    - Have clear learning objectives
    - Be engaging for {grade}
    
    Return as a bullet list:
    - Topic 1
    - Topic 2
    - Topic 3
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return [line[2:] for line in response.text.split("\n") if line.startswith("- ")]

def generate_lesson_objectives(curriculum, grade, subject, topic):
    prompt = f"""
    Create 3-4 concise learning objectives for:
    - Topic: {topic}
    - Subject: {subject}
    - Grade: {grade}
    - Curriculum: {curriculum}
    
    Each objective should:
    - Be one short sentence
    - Use simple language
    - Be measurable
    
    Format as plain text with one objective per line
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def generate_subtopics(curriculum, grade, subject, topic, objectives=""):
    prompt = f"""
    Create 3-4 comprehensive subtopics for:
    - Main Topic: {topic}
    - Subject: {subject}
    - Grade: {grade}
    - Curriculum: {curriculum}
    
    Using these objectives: {objectives} try to generate the subtopics
    
    For each subtopic provide:
    1. Title (4-5 word phrase)
    2. Content (4-5 detailed sentences)
    3. Key concepts (2-3 items)
    4. Real-world examples (1-2)
    5. Common misconceptions (1-2)
    
    Return as JSON with this exact structure:
    {{
        "subtopics": [
            {{
                "title": "Subtopic title",
                "content": "Detailed explanation...",
                "key_concepts": ["concept1", "concept2"],
                "examples": ["example1", "example2"],
                "misconceptions": ["misconception1", "misconception2"]
            }}
        ]
    }}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    try:
        json_str = re.search(r'\{.*\}', response.text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception as e:
        return {"error": f"Failed to generate: {str(e)}"}

def fetch_unsplash_image(query, subject, grade, subtopic_index, attempt=0):
    """Fetch a unique educational image from Unsplash for each subtopic"""
    try:
        # Create unique search queries for variety
        search_terms = [
            f"{query} {subject} education {grade}",
            f"{query} learning {grade}",
            f"{subject} {query} classroom",
            f"educational {query} diagram",
            f"{query} teaching aid"
        ]
        
        search_query = search_terms[subtopic_index % len(search_terms)]
        
        # Make request to Unsplash API
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": search_query,
            "per_page": 30,
            "orientation": "landscape",
            "client_id": os.getenv("UNSPLASH_ACCESS_KEY")
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data['results']:
            # Select different image based on subtopic index and attempt
            selection_index = (subtopic_index + attempt) % min(20, len(data['results']))
            return {
                "url": data['results'][selection_index]['urls']['regular'],
                "credit": data['results'][selection_index]['user']['name'],
                "profile": data['results'][selection_index]['user']['links']['html']
            }
        return None
        
    except Exception as e:
        print(f"Error fetching image from Unsplash: {str(e)}")
        return None

def generate_quiz_questions(curriculum, grade, subject, topic, lesson_content):
    """Generate different types of quiz questions based on lesson content"""
    prompt = f"""
    Create a comprehensive quiz for this lesson:
    - Topic: {topic}
    - Subject: {subject}
    - Grade: {grade}
    - Curriculum: {curriculum}
    
    Lesson Content:
    {lesson_content}
    
    Generate 3-4 questions for each type:
    1. Multiple Choice (mcq)
    2. Fill in the Blank (fillblank)
    3. Descriptive (descriptive) (questions and answer should be short)
    
    For Multiple Choice:
    - Provide 4 options
    - Mark the correct answer
    - Add explanation
    
    For Fill in the Blank:
    - Use _____ for blanks
    - Provide the answer
    - Add explanation
    
    For Descriptive:
    - Ask open-ended questions
    - Provide model answer
    - List key points
    
    Return as JSON with this exact structure:
    {{
        "mcq": [
            {{
                "question": "Question text",
                "options": ["A", "B", "C", "D"],
                "answer": "Correct option",
                "explanation": "Explanation text"
            }}
        ],
        "fillblank": [
            {{
                "question": "Question with _____ blank",
                "answer": "Correct fill",
                "explanation": "Explanation text"
            }}
        ],
        "descriptive": [
            {{
                "question": "Open-ended question",
                "answer": "Model answer",
                "key_points": ["Key point 1", "Key point 2"]
            }}
        ]
    }}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    try:
        json_str = re.search(r'\{.*\}', response.text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        return {
            "mcq": [],
            "fillblank": [],
            "descriptive": []
        }
def generate_lesson_summary(curriculum, grade, subject, topic, subtopics):
    """Generate a comprehensive summary of all subtopics"""
    prompt = f"""
    Create a concise yet comprehensive summary of this entire lesson:
    - Curriculum: {curriculum}
    - Grade: {grade}
    - Subject: {subject}
    - Topic: {topic}
    
    The lesson contains these subtopics:
    {json.dumps(subtopics, indent=2)}
    
    Your summary should make:
    1. Begin with an engaging 1-sentence overview
    2. Highlight 2-3 key takeaways
    3. Connect concepts between subtopics
    4. End with a thought-provoking question
    5. Use simple language appropriate for {grade}
    6. Summary should be super short
    
    Format as markdown with bold headings for each section
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text