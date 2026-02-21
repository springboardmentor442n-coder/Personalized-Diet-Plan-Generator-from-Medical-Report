import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_structured_data(full_text: str) -> dict:
    """
    Takes full raw PDF text and returns structured medical data as dictionary.
    """

    prompt = f"""
You are a medical data extraction system.

From the following lab report text, extract structured data in STRICT JSON format.

Rules:
- Return ONLY valid JSON.
- Do NOT include explanations.
- Do NOT include markdown.
- Do NOT summarize.
- If field not found, use empty string.
- Extract all lab tests listed.

Required JSON schema:

{{
  "patient_information": {{
    "name": "",
    "age": "",
    "gender": "",
    "lab_number": "",
    "collection_datetime": "",
    "report_datetime": ""
  }},
  "tests": [
    {{
      "test_name": "",
      "value": "",
      "units": "",
      "reference_range": ""
    }}
  ]
}}

Lab Report Text:
\"\"\"
{full_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )

    result_json = response.choices[0].message.content

    return json.loads(result_json)
