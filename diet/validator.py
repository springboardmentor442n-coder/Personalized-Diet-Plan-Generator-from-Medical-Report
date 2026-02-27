"""
Diet Plan Validator Module
Validates diet plans for consistency, nutritional balance, and dietary restrictions
"""
import json
import re

class DietValidator:
    
    # Non-vegetarian ingredients to check against
    NON_VEG_KEYWORDS = [
        'chicken', 'fish', 'mutton', 'lamb', 'beef', 'pork', 'turkey', 'duck',
        'egg', 'eggs', 'prawn', 'shrimp', 'crab', 'lobster', 'tuna', 'salmon',
        'bacon', 'sausage', 'ham', 'meat', 'seafood', 'anchovy'
    ]
    
    def __init__(self):
        self.validation_errors = []
        self.warnings = []
    
    def validate_diet_plan(self, diet_plan, diet_preference):
        """
        Main validation function for diet plans
        """
        self.validation_errors = []
        self.warnings = []
        
        if not diet_plan or not isinstance(diet_plan, dict):
            self.validation_errors.append("Invalid diet plan format")
            return False, self.validation_errors, self.warnings
        
        # Validate structure
        structure_valid = self._validate_structure(diet_plan)
        
        # Validate dietary restrictions
        diet_restrictions_valid = self._validate_dietary_restrictions(diet_plan, diet_preference)
        
        # Validate nutritional balance
        nutrition_valid = self._validate_nutrition(diet_plan)
        
        # Validate calorie ranges
        calorie_valid = self._validate_calorie_ranges(diet_plan)
        
        # Check for variety
        self._check_meal_variety(diet_plan)
        
        is_valid = structure_valid and diet_restrictions_valid and nutrition_valid and calorie_valid
        
        return is_valid, self.validation_errors, self.warnings
    
    def _validate_structure(self, diet_plan):
        """Validate the basic structure of the diet plan"""
        required_days = [f'day{i}' for i in range(1, 8)]
        required_meals = ['breakfast', 'lunch', 'snack', 'dinner']
        required_meal_keys = ['name', 'calories', 'carbs', 'protein', 'fat']
        
        # Check all days are present
        for day in required_days:
            if day not in diet_plan:
                self.validation_errors.append(f"Missing {day} in diet plan")
                return False
            
            # Check all meals are present for each day
            for meal in required_meals:
                if meal not in diet_plan[day]:
                    self.validation_errors.append(f"Missing {meal} in {day}")
                    return False
                
                # Check all meal keys are present
                meal_data = diet_plan[day][meal]
                if not isinstance(meal_data, dict):
                    self.validation_errors.append(f"Invalid meal data format for {day} {meal}")
                    return False
                
                for key in required_meal_keys:
                    if key not in meal_data:
                        self.validation_errors.append(f"Missing {key} in {day} {meal}")
                        return False
        
        return True
    
    def _validate_dietary_restrictions(self, diet_plan, diet_preference):
        """Validate dietary restrictions are followed"""
        if diet_preference == 'vegetarian':
            for day_key, day_meals in diet_plan.items():
                for meal_key, meal_data in day_meals.items():
                    if isinstance(meal_data, dict) and 'name' in meal_data:
                        meal_name = meal_data['name'].lower()
                        
                        # Check for non-vegetarian keywords
                        for keyword in self.NON_VEG_KEYWORDS:
                            if keyword in meal_name:
                                self.validation_errors.append(
                                    f"Non-vegetarian ingredient '{keyword}' found in {day_key} {meal_key}: {meal_data['name']}"
                                )
                                return False
        
        return True
    
    def _validate_nutrition(self, diet_plan):
        """Validate nutritional balance of meals"""
        for day_key, day_meals in diet_plan.items():
            for meal_key, meal_data in day_meals.items():
                if isinstance(meal_data, dict):
                    # Validate macro percentages
                    carbs = meal_data.get('carbs', 0)
                    protein = meal_data.get('protein', 0)
                    fat = meal_data.get('fat', 0)
                    
                    # Check if percentages are reasonable
                    if not (0 <= carbs <= 100 and 0 <= protein <= 100 and 0 <= fat <= 100):
                        self.validation_errors.append(
                            f"Invalid macro percentages in {day_key} {meal_key}: C:{carbs}% P:{protein}% F:{fat}%"
                        )
                        return False
                    
                    # Check if percentages roughly add up to 100 (allow some tolerance)
                    total_macros = carbs + protein + fat
                    if not (90 <= total_macros <= 110):
                        self.warnings.append(
                            f"Macro percentages don't add up to ~100% in {day_key} {meal_key}: {total_macros}%"
                        )
                    
                    # Check for extreme values
                    if carbs > 80:
                        self.warnings.append(f"Very high carbs ({carbs}%) in {day_key} {meal_key}")
                    if fat > 70:
                        self.warnings.append(f"Very high fat ({fat}%) in {day_key} {meal_key}")
                    if protein > 60:
                        self.warnings.append(f"Very high protein ({protein}%) in {day_key} {meal_key}")
        
        return True
    
    def _validate_calorie_ranges(self, diet_plan):
        """Validate calorie ranges for different meal types"""
        calorie_ranges = {
            'breakfast': (250, 400),
            'lunch': (350, 500),
            'snack': (100, 200),
            'dinner': (300, 450)
        }
        
        for day_key, day_meals in diet_plan.items():
            for meal_key, meal_data in day_meals.items():
                if isinstance(meal_data, dict) and 'calories' in meal_data:
                    calories = meal_data.get('calories', 0)
                    
                    if meal_key in calorie_ranges:
                        min_cal, max_cal = calorie_ranges[meal_key]
                        
                        if not (min_cal <= calories <= max_cal):
                            self.warnings.append(
                                f"Calories out of typical range for {day_key} {meal_key}: {calories} (expected {min_cal}-{max_cal})"
                            )
                        
                        # Check for extremely low or high calories
                        if calories < 50:
                            self.validation_errors.append(
                                f"Extremely low calories ({calories}) in {day_key} {meal_key}"
                            )
                            return False
                        
                        if calories > 800:
                            self.validation_errors.append(
                                f"Extremely high calories ({calories}) in {day_key} {meal_key}"
                            )
                            return False
        
        return True
    
    def _check_meal_variety(self, diet_plan):
        """Check for meal variety across the week"""
        all_meals = []
        
        # Collect all meal names
        for day_key, day_meals in diet_plan.items():
            for meal_key, meal_data in day_meals.items():
                if isinstance(meal_data, dict) and 'name' in meal_data:
                    meal_name = meal_data['name'].lower().strip()
                    all_meals.append((meal_key, meal_name))
        
        # Check for repeated meals
        meal_counts = {}
        for meal_type, meal_name in all_meals:
            key = f"{meal_type}:{meal_name}"
            meal_counts[key] = meal_counts.get(key, 0) + 1
        
        # Warn about repeated meals
        for meal_key, count in meal_counts.items():
            if count > 1:
                meal_type, meal_name = meal_key.split(':', 1)
                self.warnings.append(f"Repeated meal: '{meal_name}' appears {count} times as {meal_type}")
    
    def calculate_weekly_nutrition(self, diet_plan):
        """Calculate weekly nutrition summary"""
        total_calories = 0
        total_carb_calories = 0
        total_protein_calories = 0
        total_fat_calories = 0
        meal_count = 0
        
        for day_key, day_meals in diet_plan.items():
            for meal_key, meal_data in day_meals.items():
                if isinstance(meal_data, dict) and 'calories' in meal_data:
                    calories = meal_data.get('calories', 0)
                    carbs_pct = meal_data.get('carbs', 0)
                    protein_pct = meal_data.get('protein', 0)
                    fat_pct = meal_data.get('fat', 0)
                    
                    total_calories += calories
                    total_carb_calories += (carbs_pct * calories / 100)
                    total_protein_calories += (protein_pct * calories / 100)
                    total_fat_calories += (fat_pct * calories / 100)
                    meal_count += 1
        
        if total_calories > 0:
            avg_daily_calories = total_calories / 7
            weekly_avg_carbs = (total_carb_calories / total_calories) * 100
            weekly_avg_protein = (total_protein_calories / total_calories) * 100
            weekly_avg_fat = (total_fat_calories / total_calories) * 100
            
            return {
                'total_weekly_calories': round(total_calories),
                'avg_daily_calories': round(avg_daily_calories),
                'weekly_avg_carbs': round(weekly_avg_carbs, 1),
                'weekly_avg_protein': round(weekly_avg_protein, 1),
                'weekly_avg_fat': round(weekly_avg_fat, 1),
                'total_meals': meal_count
            }
        
        return {}


def validate_diet_plan(diet_plan_raw, diet_preference):
    """
    Main function to validate and format diet plan
    """
    validator = DietValidator()
    
    # If the input is already a dict, use it directly
    if isinstance(diet_plan_raw, dict):
        diet_plan = diet_plan_raw
    else:
        # Try to parse JSON string
        try:
            if isinstance(diet_plan_raw, str):
                diet_plan = json.loads(diet_plan_raw)
            else:
                raise ValueError("Invalid diet plan format")
        except json.JSONDecodeError as e:
            return {
                'error': f'Invalid JSON format: {str(e)}',
                'diet_plan': None
            }
    
    # Validate the diet plan
    is_valid, errors, warnings = validator.validate_diet_plan(diet_plan, diet_preference)
    
    if not is_valid:
        return {
            'error': f'Diet plan validation failed: {"; ".join(errors)}',
            'warnings': warnings,
            'diet_plan': diet_plan  # Return plan anyway for debugging
        }
    
    # Calculate nutrition summary
    nutrition_summary = validator.calculate_weekly_nutrition(diet_plan)
    
    # Add validation info to the result
    result = dict(diet_plan)
    result['validation'] = {
        'is_valid': is_valid,
        'errors': errors,
        'warnings': warnings,
        'nutrition_summary': nutrition_summary
    }
    
    return result