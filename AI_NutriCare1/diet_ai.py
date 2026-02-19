import os
from groq import Groq

# Groq client (API key from environment variable)
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_ai_diet(age, gender, weight, food_type, values, conditions):

    # Food preference rule
    if food_type == "Vegetarian":
        food_rule = (
            "Generate strictly vegetarian meals only. "
            "Do NOT include eggs, chicken, fish, or meat."
        )
    elif food_type == "Non-Vegetarian":
        food_rule = (
            "Include non-vegetarian foods such as eggs, chicken, or fish."
        )
    else:
        food_rule = (
            "You may include both vegetarian and non-vegetarian meals."
        )

    prompt = f"""
You are a nutrition expert.

Create a 7-day personalized diet plan based on the following details:

User Details:
- Age: {age}
- Gender: {gender}
- Weight: {weight} kg
- Food Preference: {food_type}

Food Rules:
{food_rule}

Medical Lab Values:
{values}

Detected Medical Conditions:
{conditions}

Instructions:
- Generate exactly 7 days
- Use this exact format for every day
- Do NOT use bullets, dashes, or extra symbols

FORMAT (MANDATORY):
Day 1
Breakfast: <food>
Lunch: <food>
Dinner: <food>
Calories: <number> kcal
Protine: <number> g
Carbs: <number> g
Fats: <number> g
Repeat the same format strictly until Day 7.

"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
