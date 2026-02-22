import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_llm_extraction(report_text):

    prompt = f"""
You are a medical lab report extraction system.

Extract ALL laboratory test values from the given medical report.

STRICT RULES:
- Extract ONLY values explicitly present in the report.
- DO NOT guess or hallucinate values.
- DO NOT add medical interpretation.
- Return output in VALID JSON format.
- Each test must include:
    - test_name
    - value (number)
    - unit (if available)

Return JSON in this exact structure:

{{
  "Hemoglobin": {{"value": 13.5, "unit": "g/dL"}},
  "Fasting Glucose": {{"value": 110, "unit": "mg/dL"}}
}}

If no lab values are found, return empty JSON {{}}.

Medical Report:
{report_text}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  
            messages=[
                {"role": "system", "content": "You extract structured lab data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0  
        )

        response_text = completion.choices[0].message.content.strip()

        # Convert to dictionary
        extracted_data = json.loads(response_text)

        return extracted_data

    except Exception as e:
        print("LLM extraction failed:", e)
        return {}
