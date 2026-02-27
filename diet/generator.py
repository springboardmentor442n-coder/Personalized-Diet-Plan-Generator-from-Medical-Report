"""
Diet Plan Generator Module
Handles diet plan generation using LLM and validation
"""
import json
from llm.prompts import get_diet_plan_prompt, get_prompt_settings, validate_json_structure

class DietGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        
    def generate_diet_plan(self, age, diet_preference, metrics=None, health_analysis=None, feedback=None):
        """
        Generate a complete 7-day diet plan
        """
        try:
            # Get the prompt
            prompt = get_diet_plan_prompt(age, diet_preference, metrics, health_analysis, feedback)
            
            # Get optimized settings for diet plan generation
            settings = get_prompt_settings('diet_plan')
            
            # Generate diet plan using LLM
            diet_plan_raw = self.llm_client.get_completion(
                prompt,
                temperature=settings['temperature'],
                max_tokens=settings['max_tokens']
            )
            
            # Validate the generated plan
            if isinstance(diet_plan_raw, dict) and not diet_plan_raw.get('error'):
                return diet_plan_raw
            else:
                # If there's an error or invalid format, return a fallback
                return self._get_fallback_diet_plan(age, diet_preference)
                
        except Exception as e:
            print(f"Error generating diet plan: {e}")
            return self._get_fallback_diet_plan(age, diet_preference)
    
    def _get_fallback_diet_plan(self, age, diet_preference):
        """
        Provide a fallback diet plan if LLM generation fails
        """
        if diet_preference == 'vegetarian':
            return self._get_vegetarian_fallback(age)
        else:
            return self._get_non_vegetarian_fallback(age)
    
    def _get_vegetarian_fallback(self, age):
        """Fallback vegetarian diet plan"""
        base_plan = {
            "day1": {
                "breakfast": {"name": "Oatmeal with fruits and nuts", "calories": 310, "carbs": 55, "protein": 15, "fat": 30},
                "lunch": {"name": "Quinoa vegetable bowl", "calories": 420, "carbs": 50, "protein": 25, "fat": 25},
                "snack": {"name": "Greek yogurt with berries", "calories": 150, "carbs": 60, "protein": 20, "fat": 20},
                "dinner": {"name": "Lentil curry with brown rice", "calories": 380, "carbs": 45, "protein": 30, "fat": 25}
            },
            "day2": {
                "breakfast": {"name": "Vegetable upma with coconut", "calories": 300, "carbs": 50, "protein": 20, "fat": 30},
                "lunch": {"name": "Chickpea and vegetable stir-fry", "calories": 410, "carbs": 45, "protein": 30, "fat": 25},
                "snack": {"name": "Mixed nuts and dried fruits", "calories": 160, "carbs": 30, "protein": 15, "fat": 55},
                "dinner": {"name": "Paneer and spinach curry", "calories": 370, "carbs": 25, "protein": 35, "fat": 40}
            },
            "day3": {
                "breakfast": {"name": "Idli with sambar and chutney", "calories": 320, "carbs": 55, "protein": 18, "fat": 27},
                "lunch": {"name": "Vegetable biryani with raita", "calories": 440, "carbs": 60, "protein": 15, "fat": 25},
                "snack": {"name": "Roasted chickpeas", "calories": 145, "carbs": 50, "protein": 25, "fat": 25},
                "dinner": {"name": "Mixed vegetables with roti", "calories": 350, "carbs": 40, "protein": 20, "fat": 40}
            },
            "day4": {
                "breakfast": {"name": "Poha with vegetables", "calories": 315, "carbs": 52, "protein": 18, "fat": 30},
                "lunch": {"name": "Rajma with rice", "calories": 430, "carbs": 55, "protein": 25, "fat": 20},
                "snack": {"name": "Vegetable sandwich", "calories": 155, "carbs": 65, "protein": 15, "fat": 20},
                "dinner": {"name": "Palak paneer with chapati", "calories": 360, "carbs": 30, "protein": 30, "fat": 40}
            },
            "day5": {
                "breakfast": {"name": "Dosa with coconut chutney", "calories": 305, "carbs": 60, "protein": 15, "fat": 25},
                "lunch": {"name": "Chole bhature", "calories": 450, "carbs": 50, "protein": 20, "fat": 30},
                "snack": {"name": "Fruit salad with nuts", "calories": 140, "carbs": 70, "protein": 10, "fat": 20},
                "dinner": {"name": "Vegetable khichdi", "calories": 340, "carbs": 50, "protein": 25, "fat": 25}
            },
            "day6": {
                "breakfast": {"name": "Paratha with curd", "calories": 325, "carbs": 45, "protein": 20, "fat": 35},
                "lunch": {"name": "Sambar rice with vegetables", "calories": 415, "carbs": 55, "protein": 20, "fat": 25},
                "snack": {"name": "Masala tea with biscuits", "calories": 150, "carbs": 60, "protein": 10, "fat": 30},
                "dinner": {"name": "Aloo gobi with roti", "calories": 375, "carbs": 50, "protein": 15, "fat": 35}
            },
            "day7": {
                "breakfast": {"name": "Upma with vegetables", "calories": 310, "carbs": 55, "protein": 15, "fat": 30},
                "lunch": {"name": "Vegetable pulao", "calories": 425, "carbs": 60, "protein": 15, "fat": 25},
                "snack": {"name": "Sprouts salad", "calories": 165, "carbs": 45, "protein": 30, "fat": 25},
                "dinner": {"name": "Dal tadka with rice", "calories": 385, "carbs": 50, "protein": 25, "fat": 25}
            }
        }
        
        # Adjust calories based on age
        if age > 50:
            # Reduce calories for older adults
            for day in base_plan:
                for meal in base_plan[day]:
                    base_plan[day][meal]["calories"] = int(base_plan[day][meal]["calories"] * 0.9)
        elif age < 30:
            # Increase calories for younger adults
            for day in base_plan:
                for meal in base_plan[day]:
                    base_plan[day][meal]["calories"] = int(base_plan[day][meal]["calories"] * 1.1)
        
        return base_plan
    
    def _get_non_vegetarian_fallback(self, age):
        """Fallback non-vegetarian diet plan"""
        base_plan = {
            "day1": {
                "breakfast": {"name": "Scrambled eggs with toast", "calories": 320, "carbs": 35, "protein": 30, "fat": 35},
                "lunch": {"name": "Grilled chicken with quinoa", "calories": 440, "carbs": 40, "protein": 35, "fat": 25},
                "snack": {"name": "Greek yogurt with nuts", "calories": 150, "carbs": 45, "protein": 25, "fat": 30},
                "dinner": {"name": "Fish curry with rice", "calories": 390, "carbs": 35, "protein": 40, "fat": 25}
            },
            "day2": {
                "breakfast": {"name": "Chicken sausage with bread", "calories": 315, "carbs": 40, "protein": 25, "fat": 35},
                "lunch": {"name": "Mutton biryani", "calories": 450, "carbs": 50, "protein": 30, "fat": 20},
                "snack": {"name": "Boiled eggs", "calories": 140, "carbs": 5, "protein": 50, "fat": 45},
                "dinner": {"name": "Chicken stir-fry with vegetables", "calories": 370, "carbs": 25, "protein": 45, "fat": 30}
            },
            "day3": {
                "breakfast": {"name": "Omelette with vegetables", "calories": 310, "carbs": 20, "protein": 35, "fat": 45},
                "lunch": {"name": "Fish fry with rice", "calories": 420, "carbs": 45, "protein": 35, "fat": 20},
                "snack": {"name": "Chicken soup", "calories": 155, "carbs": 30, "protein": 40, "fat": 30},
                "dinner": {"name": "Lamb curry with chapati", "calories": 380, "carbs": 30, "protein": 40, "fat": 30}
            },
            "day4": {
                "breakfast": {"name": "Egg sandwich", "calories": 325, "carbs": 45, "protein": 25, "fat": 30},
                "lunch": {"name": "Chicken tikka with naan", "calories": 435, "carbs": 40, "protein": 35, "fat": 25},
                "snack": {"name": "Tuna salad", "calories": 160, "carbs": 20, "protein": 45, "fat": 35},
                "dinner": {"name": "Prawn curry with rice", "calories": 365, "carbs": 35, "protein": 40, "fat": 25}
            },
            "day5": {
                "breakfast": {"name": "Bacon and eggs", "calories": 330, "carbs": 15, "protein": 30, "fat": 55},
                "lunch": {"name": "Chicken fried rice", "calories": 425, "carbs": 50, "protein": 30, "fat": 20},
                "snack": {"name": "Protein shake", "calories": 145, "carbs": 25, "protein": 50, "fat": 25},
                "dinner": {"name": "Grilled fish with salad", "calories": 350, "carbs": 20, "protein": 50, "fat": 30}
            },
            "day6": {
                "breakfast": {"name": "Egg curry with paratha", "calories": 340, "carbs": 40, "protein": 25, "fat": 35},
                "lunch": {"name": "Beef stew with bread", "calories": 440, "carbs": 35, "protein": 40, "fat": 25},
                "snack": {"name": "Chicken salad", "calories": 150, "carbs": 30, "protein": 40, "fat": 30},
                "dinner": {"name": "Fish tikka with vegetables", "calories": 375, "carbs": 25, "protein": 45, "fat": 30}
            },
            "day7": {
                "breakfast": {"name": "Sausage and eggs", "calories": 335, "carbs": 20, "protein": 35, "fat": 45},
                "lunch": {"name": "Chicken curry with rice", "calories": 430, "carbs": 45, "protein": 35, "fat": 20},
                "snack": {"name": "Hard boiled eggs with crackers", "calories": 165, "carbs": 40, "protein": 30, "fat": 30},
                "dinner": {"name": "Mutton kebabs with salad", "calories": 380, "carbs": 20, "protein": 45, "fat": 35}
            }
        }
        
        # Adjust calories based on age
        if age > 50:
            # Reduce calories for older adults
            for day in base_plan:
                for meal in base_plan[day]:
                    base_plan[day][meal]["calories"] = int(base_plan[day][meal]["calories"] * 0.9)
        elif age < 30:
            # Increase calories for younger adults
            for day in base_plan:
                for meal in base_plan[day]:
                    base_plan[day][meal]["calories"] = int(base_plan[day][meal]["calories"] * 1.1)
        
        return base_plan
    
    def calculate_daily_totals(self, diet_plan):
        """Calculate daily calorie totals for the diet plan"""
        daily_totals = {}
        
        for day_key, day_meals in diet_plan.items():
            if day_key.startswith('day'):
                total_calories = 0
                total_carbs = 0
                total_protein = 0
                total_fat = 0
                
                for meal_name, meal_data in day_meals.items():
                    if isinstance(meal_data, dict) and 'calories' in meal_data:
                        calories = meal_data.get('calories', 0)
                        carbs_pct = meal_data.get('carbs', 0)
                        protein_pct = meal_data.get('protein', 0)
                        fat_pct = meal_data.get('fat', 0)
                        
                        total_calories += calories
                        
                        # Calculate weighted macro percentages
                        total_carbs += (carbs_pct * calories / 100)
                        total_protein += (protein_pct * calories / 100)
                        total_fat += (fat_pct * calories / 100)
                
                # Calculate average macro percentages
                if total_calories > 0:
                    avg_carbs = round((total_carbs / total_calories) * 100, 1)
                    avg_protein = round((total_protein / total_calories) * 100, 1)
                    avg_fat = round((total_fat / total_calories) * 100, 1)
                else:
                    avg_carbs = avg_protein = avg_fat = 0
                
                daily_totals[day_key] = {
                    'total_calories': total_calories,
                    'avg_carbs': avg_carbs,
                    'avg_protein': avg_protein,
                    'avg_fat': avg_fat
                }
        
        return daily_totals