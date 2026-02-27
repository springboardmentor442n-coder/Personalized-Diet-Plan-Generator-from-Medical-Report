"""
Prompt Templates for AI-NutriCare
Contains all LLM prompts for health analysis, diet generation, and chatbot
"""

def get_health_analysis_prompt(extracted_text, age):
    """
    Generate prompt for health analysis from medical report text
    """
    prompt = f"""
Analyze the following medical report text and patient age to provide a health assessment.

PATIENT AGE: {age} years

MEDICAL REPORT TEXT:
{extracted_text}

Return a JSON object with the following structure:
{{
    "conditions": ["list of detected health conditions"],
    "risk_level": "low/medium/high",
    "recommendations": ["list of 2-3 specific dietary recommendations"]
}}

Rules:
1. Only identify clear medical conditions mentioned in the text
2. Risk level should be based on age and detected conditions
3. Keep recommendations specific and actionable
4. If no clear conditions are found, use empty array for conditions
5. Always provide risk level assessment
6. Return valid JSON only

Example output:
{{
    "conditions": ["diabetes", "hypertension"],
    "risk_level": "medium",
    "recommendations": ["Monitor carbohydrate intake", "Reduce sodium consumption", "Increase fiber-rich foods"]
}}
    """
    return prompt.strip()

def get_diet_plan_prompt(age, diet_preference, metrics, health_analysis, feedback=None):
    """
    Generate prompt for 7-day diet plan creation
    """
    feedback_section = ""
    if feedback:
        feedback_section = f"""
FEEDBACK FROM PREVIOUS PLAN:
{feedback}

Please incorporate this feedback into the new plan.
"""

    prompt = f"""
Create a personalized 7-day diet plan based on the following information:

PATIENT DETAILS:
- Age: {age} years
- Diet Preference: {diet_preference}

HEALTH METRICS:
{metrics}

HEALTH ANALYSIS:
{health_analysis}
{feedback_section}
Generate a complete 7-day diet plan with 4 meals per day (breakfast, lunch, snack, dinner).

DIET PREFERENCE RULES:
- Vegetarian: NO chicken, fish, eggs, meat, or any animal products except dairy
- Non-Vegetarian: Can include both vegetarian and non-vegetarian options

Return a JSON object with this exact structure:
{{
    "day1": {{
        "breakfast": {{"name": "meal name", "calories": 300, "carbs": 45, "protein": 20, "fat": 35}},
        "lunch": {{"name": "meal name", "calories": 400, "carbs": 50, "protein": 25, "fat": 25}},
        "snack": {{"name": "meal name", "calories": 150, "carbs": 60, "protein": 15, "fat": 25}},
        "dinner": {{"name": "meal name", "calories": 350, "carbs": 40, "protein": 30, "fat": 30}}
    }},
    "day2": {{
        "breakfast": {{"name": "meal name", "calories": 320, "carbs": 50, "protein": 20, "fat": 30}},
        "lunch": {{"name": "meal name", "calories": 420, "carbs": 45, "protein": 30, "fat": 25}},
        "snack": {{"name": "meal name", "calories": 140, "carbs": 65, "protein": 10, "fat": 25}},
        "dinner": {{"name": "meal name", "calories": 380, "carbs": 35, "protein": 35, "fat": 30}}
    }},
    "day3": {{
        "breakfast": {{"name": "meal name", "calories": 310, "carbs": 55, "protein": 15, "fat": 30}},
        "lunch": {{"name": "meal name", "calories": 450, "carbs": 40, "protein": 35, "fat": 25}},
        "snack": {{"name": "meal name", "calories": 160, "carbs": 70, "protein": 10, "fat": 20}},
        "dinner": {{"name": "meal name", "calories": 360, "carbs": 30, "protein": 40, "fat": 30}}
    }},
    "day4": {{
        "breakfast": {{"name": "meal name", "calories": 330, "carbs": 45, "protein": 25, "fat": 30}},
        "lunch": {{"name": "meal name", "calories": 410, "carbs": 50, "protein": 25, "fat": 25}},
        "snack": {{"name": "meal name", "calories": 145, "carbs": 60, "protein": 15, "fat": 25}},
        "dinner": {{"name": "meal name", "calories": 370, "carbs": 35, "protein": 35, "fat": 30}}
    }},
    "day5": {{
        "breakfast": {{"name": "meal name", "calories": 315, "carbs": 50, "protein": 20, "fat": 30}},
        "lunch": {{"name": "meal name", "calories": 440, "carbs": 45, "protein": 30, "fat": 25}},
        "snack": {{"name": "meal name", "calories": 155, "carbs": 65, "protein": 15, "fat": 20}},
        "dinner": {{"name": "meal name", "calories": 390, "carbs": 40, "protein": 30, "fat": 30}}
    }},
    "day6": {{
        "breakfast": {{"name": "meal name", "calories": 325, "carbs": 48, "protein": 22, "fat": 30}},
        "lunch": {{"name": "meal name", "calories": 430, "carbs": 42, "protein": 32, "fat": 26}},
        "snack": {{"name": "meal name", "calories": 150, "carbs": 62, "protein": 12, "fat": 26}},
        "dinner": {{"name": "meal name", "calories": 375, "carbs": 38, "protein": 32, "fat": 30}}
    }},
    "day7": {{
        "breakfast": {{"name": "meal name", "calories": 305, "carbs": 52, "protein": 18, "fat": 30}},
        "lunch": {{"name": "meal name", "calories": 415, "carbs": 47, "protein": 28, "fat": 25}},
        "snack": {{"name": "meal name", "calories": 165, "carbs": 68, "protein": 12, "fat": 20}},
        "dinner": {{"name": "meal name", "calories": 385, "carbs": 36, "protein": 34, "fat": 30}}
    }}
}}

REQUIREMENTS:
1. Calories per meal: Breakfast (300-330), Lunch (400-450), Snack (140-165), Dinner (350-390)
2. Macros must add up to 100% for each meal
3. Provide diverse, realistic meal names
4. Consider the patient's age group and health conditions
5. Ensure vegetarian meals contain NO animal products except dairy
6. Include variety across the 7 days
7. Return valid JSON only

AGE GROUP CONSIDERATIONS:
- Under 30: Higher carbs for energy, moderate protein
- 30-50: Balanced macros, focus on metabolism
- Over 50: Lower carbs, higher protein, heart-healthy options
    """
    return prompt.strip()

def get_chatbot_prompt(message, context):
    """
    Generate prompt for RAG chatbot responses
    """
    prompt = f"""
You are an AI nutrition assistant for AI-NutriCare. Answer the user's question based on their personal context and general nutrition knowledge.

USER'S PERSONAL CONTEXT:
{context}

USER'S QUESTION:
{message}

INSTRUCTIONS:
1. Use the user's personal context (age, diet preference, health metrics, diet plan) to provide personalized answers
2. If asked about meal alternatives, suggest 2-3 specific alternatives that fit their diet preference
3. Keep responses concise and helpful (2-4 sentences)
4. If the question is outside nutrition/health scope, politely redirect to nutrition topics
5. Always consider their vegetarian/non-vegetarian preference
6. Provide actionable, practical advice

RESPONSE GUIDELINES:
- For health metrics: Explain what the values mean and implications
- For diet plan questions: Reference their specific plan and explain benefits
- For alternatives: Suggest meals with similar nutrition profiles
- For general nutrition: Relate to their specific situation

Respond naturally, not in JSON format. Be friendly and professional.
    """
    return prompt.strip()

def get_meal_alternative_prompt(meal_name, day, meal_type, diet_preference, health_conditions):
    """
    Generate prompt specifically for meal alternatives
    """
    prompt = f"""
The user wants alternatives to this meal from their diet plan:
- Original Meal: {meal_name}
- Day: {day}
- Meal Type: {meal_type}
- Diet Preference: {diet_preference}
- Health Conditions: {health_conditions}

Provide 3 alternative meals that:
1. Have similar calorie and macro profiles
2. Match their diet preference ({diet_preference})
3. Are suitable for their health conditions
4. Are practical and realistic

Format your response as:
"Here are 3 alternatives for your {meal_type}:
1. [Meal name] - [brief description]
2. [Meal name] - [brief description]  
3. [Meal name] - [brief description]

All alternatives provide similar nutrition to your original {meal_name}."
    """
    return prompt.strip()

# Validation prompts
def validate_json_structure(json_data, expected_structure):
    """
    Validate that JSON data matches expected structure
    """
    if expected_structure == "health_analysis":
        required_keys = ["conditions", "risk_level", "recommendations"]
        return all(key in json_data for key in required_keys)
    
    elif expected_structure == "diet_plan":
        required_days = [f"day{i}" for i in range(1, 8)]
        if not all(day in json_data for day in required_days):
            return False
        
        required_meals = ["breakfast", "lunch", "snack", "dinner"]
        meal_keys = ["name", "calories", "carbs", "protein", "fat"]
        
        for day in required_days:
            if not all(meal in json_data[day] for meal in required_meals):
                return False
            for meal in required_meals:
                if not all(key in json_data[day][meal] for key in meal_keys):
                    return False
        
        return True
    
    return False

# Constants for prompt optimization
PROMPT_SETTINGS = {
    'health_analysis': {
        'max_tokens': 800,
        'temperature': 0,
        'timeout': 15
    },
    'diet_plan': {
        'max_tokens': 1500,
        'temperature': 0,
        'timeout': 25
    },
    'chatbot': {
        'max_tokens': 400,
        'temperature': 0.1,
        'timeout': 10
    }
}

def get_prompt_settings(prompt_type):
    """Get optimized settings for different prompt types"""
    return PROMPT_SETTINGS.get(prompt_type, {
        'max_tokens': 800,
        'temperature': 0,
        'timeout': 15
    })