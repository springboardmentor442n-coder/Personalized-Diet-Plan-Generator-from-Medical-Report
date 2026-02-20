from pypdf import PdfReader
from groq import Groq
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_medical_data(pdf_path):

    # -------- READ PDF TEXT --------
    reader = PdfReader(pdf_path)
    full_text = ""

    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # -------- AI EXTRACTION --------
    prompt = f"""
Extract medical health values and return ONLY JSON.

Fields:
- hba1c
- fasting_glucose
- total_cholesterol
- hdl
- ldl
- triglycerides
- vitamin_d
- hemoglobin
- tsh

Medical Report:
{full_text}
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    # -------- CLEAN JSON --------
    match = re.search(r'\{.*\}', result, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        return {}
