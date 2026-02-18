from groq import Groq
from config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_llm_diet(health_status, region):

    prompt = f"""
You are a clinical nutritionist.

Health conditions:
{health_status}

Region: {region}

Generate a structured 7-day diet plan.
Each day must include:
Breakfast:
Lunch:
Dinner:
Snacks:

Keep it clear and medically appropriate.
Avoid long explanations.
"""

    response = client.chat.completions.create(
        model=settings.DIET_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.3
    )

    return response.choices[0].message.content
