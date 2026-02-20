from groq import Groq
import json
import os
from dotenv import load_dotenv
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_plan(user_profile):

    with open("outputs/analysis.json") as f:
        health = json.load(f)

    prompt = f"""
    You are a certified nutritionist AI.

    Generate a 7-Day personalized diet plan in TEXT TABLE format.

    Health Conditions:
    {health}

    User Preferences:
    {user_profile}

    ABSOLUTE RULES:
    - Output ONLY CSV
    - No sentences
    - No markdown
    - table lines
    - No explanations
    - No extra spaces
    - No blank lines
    - Exactly 5 columns per row

    Header must be EXACTLY:
    Day,Breakfast,Lunch,Snacks,Dinner

    Rows: Sunday to Saturday only.
    Use simple Indian foods.
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    return result
