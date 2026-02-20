from groq import Groq
import base64
from dotenv import load_dotenv
import os

load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image(path):
    with open(path,"rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")
    
image_base64=encode_image("data/page_6.png")

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": """
Extract the following medical values from this report and return ONLY valid JSON.

Fields:
- hba1c
- fasting_glucose
- total_cholesterol
- hdl
- ldl
- triglycerides
- vitamin_d
- tsh

If a value is missing, write null.
No extra text. Only JSON.
"""}
,
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)