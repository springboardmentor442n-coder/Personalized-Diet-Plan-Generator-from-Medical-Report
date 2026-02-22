import os
from groq import Groq
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_entities_with_llm(raw_text):
    prompt = f"""
    Act as a medical data extractor. Extract all test results from the text.
    Return ONLY a JSON object: {{"Test Name": {{"value": numeric_value, "unit": "unit"}}}}
    
    Text:
    {raw_text[:7000]}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

def build_llm_prompt(diet_data, diet_type):

    return f"""
    Expert Nutritionist: Generate a 7-day {diet_type} plan.
    Patient: BMI {diet_data.get('BMI')}, Conditions: {diet_data.get('Detected Conditions')}.
    Results: {diet_data.get('Extracted Medical Values')}
    
    FORMAT:
    Day 1:
    Breakfast: ...
    Lunch: ...
    Snacks: ...
    Dinner: ...
    Note: [Justified Explanation]
    """


def call_groq_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful nutrition assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=1500,
    )
    return response.choices[0].message.content.strip()
