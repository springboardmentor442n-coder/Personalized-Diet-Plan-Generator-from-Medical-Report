from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import uuid
import time
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'demo-secret-key-nutricare'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global storage for session data
session_data = {}

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_dynamic_diet_plan(days, diet_preference, plan_variation, variation_offset=0):
    """Generate dynamic diet plan based on number of days with meal variation"""
    
    # Base meal options for different diet preferences
    vegetarian_meals = {
        "breakfast_options": [
            "Oatmeal with fruits and nuts (310 kcal)",
            "Greek yogurt parfait with granola and berries (350 kcal)",
            "Whole grain avocado toast with cherry tomatoes (340 kcal)",
            "Smoothie bowl with banana, spinach, and chia seeds (320 kcal)",
            "Whole wheat pancakes with fresh fruit compote (370 kcal)",
            "Overnight muesli with fresh fruits and nuts (330 kcal)"
        ],
        "lunch_options": [
            "Quinoa vegetable bowl (420 kcal)",
            "Red lentil soup with whole grain bread (380 kcal)",
            "Chickpea curry with brown rice (450 kcal)",
            "Mediterranean wrap with hummus and sprouts (400 kcal)",
            "Three-bean salad with olive oil dressing (410 kcal)",
            "Spinach and mushroom curry with roti (420 kcal)"
        ],
        "dinner_options": [
            "Lentil curry with brown rice (380 kcal)",
            "Stir-fried vegetables with quinoa (360 kcal)",
            "Grilled tofu with sweet potato mash (390 kcal)",
            "Stuffed bell peppers with quinoa (370 kcal)",
            "Whole grain pasta primavera (380 kcal)",
            "Millet pilaf with grilled vegetables (360 kcal)"
        ],
        "snack_options": [
            "Greek yogurt with berries (150 kcal)",
            "Mixed nuts and dried fruits (120 kcal)",
            "Fresh fruit smoothie (180 kcal)",
            "Roasted pumpkin seeds (100 kcal)",
            "Herbal tea with healthy trail mix (140 kcal)",
            "Fresh vegetable juice (95 kcal)"
        ]
    }
    
    non_vegetarian_meals = {
        "breakfast_options": [
            "Scrambled eggs with whole grain toast (340 kcal)",
            "Greek yogurt with granola and berries (350 kcal)",
            "Protein smoothie with banana and oats (360 kcal)",
            "Whole grain avocado toast with boiled egg (380 kcal)",
            "Omelette with vegetables and cheese (320 kcal)",
            "Chicken sausage with whole grain bread (370 kcal)"
        ],
        "lunch_options": [
            "Grilled chicken with quinoa salad (450 kcal)",
            "Fish curry with brown rice (420 kcal)",
            "Chicken wrap with vegetables (430 kcal)",
            "Tuna salad with mixed greens (380 kcal)",
            "Grilled salmon with sweet potato (460 kcal)",
            "Turkey sandwich with avocado (400 kcal)"
        ],
        "dinner_options": [
            "Baked chicken with steamed vegetables (400 kcal)",
            "Fish with quinoa and asparagus (390 kcal)",
            "Lean beef stir-fry with brown rice (420 kcal)",
            "Grilled turkey with roasted vegetables (380 kcal)",
            "Baked cod with mashed cauliflower (360 kcal)",
            "Chicken breast with sweet potato (410 kcal)"
        ],
        "snack_options": [
            "Greek yogurt with berries (150 kcal)",
            "Protein shake with fruits (180 kcal)",
            "Hard-boiled eggs with crackers (160 kcal)",
            "Cottage cheese with nuts (140 kcal)",
            "Turkey roll-ups with vegetables (120 kcal)",
            "Protein bar with natural ingredients (170 kcal)"
        ]
    }
    
    # Select meal options based on diet preference
    meals = vegetarian_meals if diet_preference == 'vegetarian' else non_vegetarian_meals
    
    # Day themes
    themes = [
        "Balanced Nutrition", "Anti-inflammatory Focus", "Protein Power Day", 
        "Fiber Rich & Cleansing", "Heart Healthy Focus", "Weekend Wellness",
        "Weekly Reset", "Energy Boost Day", "Detox Day", "Muscle Building",
        "Brain Health Focus", "Digestive Wellness", "Immunity Boost", "Recovery Day"
    ]
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    diet_plan = {}
    
    for day in range(1, days + 1):
        # Use modulo to cycle through options with variation offset for different meals
        breakfast_idx = (day - 1 + variation_offset) % len(meals["breakfast_options"])
        lunch_idx = (day - 1 + variation_offset * 2) % len(meals["lunch_options"])  # Different offset for lunch
        dinner_idx = (day - 1 + variation_offset * 3) % len(meals["dinner_options"])  # Different offset for dinner
        snack_idx = (day - 1 + variation_offset) % len(meals["snack_options"])
        
        breakfast = meals["breakfast_options"][breakfast_idx]
        lunch = meals["lunch_options"][lunch_idx]
        dinner = meals["dinner_options"][dinner_idx]
        snack = meals["snack_options"][snack_idx]
        
        # Calculate daily total (extract calories and sum)
        breakfast_cal = int(breakfast.split('(')[1].split(' ')[0]) if '(' in breakfast else 320
        lunch_cal = int(lunch.split('(')[1].split(' ')[0]) if '(' in lunch else 400
        dinner_cal = int(dinner.split('(')[1].split(' ')[0]) if '(' in dinner else 380
        snack_cal = int(snack.split('(')[1].split(' ')[0]) if '(' in snack else 140
        daily_total = breakfast_cal + lunch_cal + dinner_cal + snack_cal
        
        # Get day name and theme
        day_name = day_names[(day - 1) % 7] if day <= 7 else f"Day {day}"
        theme = themes[(day - 1) % len(themes)]
        
        diet_plan[f"Day {day}"] = {
            "theme": f"{day_name} - {theme}",
            "Breakfast": breakfast,
            "Lunch": lunch,
            "Dinner": dinner,
            "Snack": snack,
            "daily_total": f"{daily_total} kcal",
            "hydration": "2.5L water + herbal teas"
        }
    
    return diet_plan

@app.route('/')
def index():
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    
    return render_template('interactive_dashboard.html', session_id=session_id)

@app.route('/api/process_file', methods=['POST'])
def api_process_file():
    try:
        session_id = session.get('session_id', str(uuid.uuid4()))
        session['session_id'] = session_id
        
        # Simulate processing delay for realistic experience
        time.sleep(2)
        
        # Handle file upload and analysis
        analysis_result = {
            "file_processed": False,
            "file_name": "",
            "file_type": "",
            "file_size": "",
            "extracted_data": {}
        }
        
        if 'medical_report' in request.files:
            file = request.files['medical_report']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Get file info
                file_size = os.path.getsize(filepath)
                file_size_mb = round(file_size / (1024*1024), 2)
                
                # Simulate medical report analysis with realistic extracted data
                analysis_result = {
                    "file_processed": True,
                    "file_name": filename,
                    "file_type": filename.split('.')[-1].upper(),
                    "file_size": f"{file_size_mb} MB",
                    "processing_time": "2.3 seconds",
                    "extracted_data": {
                        "patient_info": {
                            "name": "Patient Analysis Complete",
                            "age_range": "25-35 years (detected from context)",
                            "gender": "Auto-detected from medical context"
                        },
                        "health_metrics": {
                            "blood_pressure": "Normal range (120/80 mmHg)",
                            "cholesterol": "Total: 180 mg/dL (Good)",
                            "blood_sugar": "Fasting: 95 mg/dL (Normal)",
                            "bmi_category": "Normal weight range"
                        },
                        "health_conditions": [
                            "No major health concerns detected",
                            "Cardiovascular health: Good",
                            "Metabolic profile: Normal"
                        ],
                        "allergies": [
                            "No food allergies mentioned",
                            "No drug allergies noted"
                        ],
                        "current_medications": [
                            "Daily multivitamin",
                            "Vitamin D supplement"
                        ],
                        "medical_recommendations": [
                            "Maintain current healthy lifestyle",
                            "Continue regular exercise routine",
                            "Balanced nutrition recommended",
                            "Annual health checkups advised"
                        ]
                    },
                    "ai_insights": {
                        "nutrition_focus": "Preventive nutrition and wellness maintenance",
                        "dietary_priorities": [
                            "Maintain balanced macronutrients",
                            "Focus on whole foods",
                            "Adequate hydration",
                            "Regular meal timing"
                        ],
                        "risk_factors": "Low risk profile",
                        "diet_suitability": "Suitable for both vegetarian and non-vegetarian diets"
                    }
                }
            else:
                return jsonify({
                    "success": False, 
                    "error": "Invalid file format. Please upload PDF, PNG, JPG, or JPEG files."
                }), 400
        else:
            return jsonify({
                "success": False, 
                "error": "No file uploaded. Please select a medical report to upload."
            }), 400
        
        return jsonify({
            "success": True,
            "analysis": analysis_result,
            "message": "Medical report processed successfully!",
            "next_step": "generate_plan"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate_plan', methods=['POST'])
def api_generate_plan():
    try:
        session_id = session.get('session_id', str(uuid.uuid4()))
        session['session_id'] = session_id
        
        # Get form data (make age and diet preference optional)
        data = request.json
        age = data.get('age', 30)  # Default age if not provided
        diet_preference = data.get('diet_preference', 'vegetarian')  # Default preference
        health_goals = data.get('health_goals', ['general_wellness'])
        plan_days = data.get('plan_days', 7)  # Default to 7 days if not provided
        variation_offset = data.get('variation_offset', 0)  # For generating different meal variations
        
        # Simulate AI processing time
        time.sleep(3)
        
        # Generate diet plan with dynamic number of days
        variations = ['energizing', 'detox', 'protein-rich', 'heart-healthy', 'metabolism-boost']
        plan_variation = variations[int(time.time()) % len(variations)]
        
        # Generate dynamic diet plan with variation offset
        diet_plan = generate_dynamic_diet_plan(plan_days, diet_preference, plan_variation, variation_offset)
        
        demo_plan = {
            "generation_info": {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "processing_time": "3.2 seconds",
                "ai_model": "NutriCare AI v2.0",
                "personalization_level": "High",
                "plan_variation": plan_variation,
                "plan_duration": f"{plan_days} days"
            },
            "patient_profile": {
                "age": age,
                "diet_preference": diet_preference,
                "health_goals": health_goals,
                "plan_days": plan_days,
                "calorie_target": f"{1800 + (int(age)//10) * 100} - {2000 + (int(age)//10) * 100} kcal/day",
                "nutrition_focus": f"Balanced macronutrients with {plan_variation} emphasis"
            },
            "health_analysis": {
                "summary": f"Comprehensive {plan_variation} nutrition plan for {age}-year-old with {diet_preference} dietary preference ({plan_days} days)",
                "bmi_recommendations": "Maintain healthy weight through balanced nutrition",
                "metabolic_insights": "Optimized meal timing for sustained energy levels",
                "key_recommendations": [
                    "Maintain portion control with balanced macronutrients",
                    "Include 30-45 minutes of daily physical activity",
                    "Consume 8-10 glasses of water throughout the day",
                    "Eat meals at consistent intervals (every 3-4 hours)",
                    "Include variety in food choices for optimal micronutrient intake",
                    "Practice mindful eating and proper meal timing",
                    "Focus on fiber-rich foods for digestive health"
                ]
            },
            "nutrition_targets": {
                "protein": "1.2-1.6g per kg body weight",
                "carbohydrates": "45-65% of total calories",
                "fats": "20-35% of total calories (focus on healthy fats)",
                "fiber": "25-35g daily",
                "water": "8-10 glasses (2-2.5 liters) daily"
            },
            "diet_plan": diet_plan,
            "weekly_insights": {
                "variety_score": "Excellent - diverse food items",
                "nutrition_balance": "Optimal macro and micronutrient distribution",
                "calorie_consistency": f"Consistent daily calorie range for {plan_days} days",
                "meal_timing": "Structured meal pattern for sustained energy",
                "plan_focus": f"{plan_variation.title()} nutrition approach"
            }
        }
        
        # Store plan in session for chatbot access
        if session_id not in session_data:
            session_data[session_id] = {}
        session_data[session_id]['current_plan'] = demo_plan
        
        return jsonify({
            "success": True,
            "diet_plan": demo_plan,
            "message": f"{plan_days}-day {plan_variation} diet plan generated successfully!",
            "plan_id": f"NutriPlan_{session_id}_{int(time.time())}"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/chat_message', methods=['POST'])
def api_chat_message():
    try:
        session_id = session.get('session_id')
        data = request.json
        user_message = data.get('message', '').lower()
        
        # Check if user has a current diet plan for personalized responses
        current_plan = None
        if session_id and session_id in session_data and 'current_plan' in session_data[session_id]:
            current_plan = session_data[session_id]['current_plan']
        
        # Enhanced nutrition expert responses with diet plan awareness
        nutrition_responses = {
            "weight loss": "🎯 Weight Loss Strategy: 1) Create moderate calorie deficit (300-500 kcal) 2) Increase protein to 1.6g/kg body weight 3) Add fiber-rich foods 4) Avoid liquid calories 5) Practice portion control 6) Include strength training 7) Stay hydrated 8) Get adequate sleep",
            "weight gain": "💪 Healthy Weight Gain: 1) Increase calorie intake by 300-500 kcal 2) Add healthy fats (nuts, avocado, olive oil) 3) Include protein at every meal 4) Eat every 2-3 hours 5) Add smoothies and shakes 6) Focus on calorie-dense whole foods 7) Include resistance training",
            "diabetes": "🩺 Diabetes Management: 1) Choose low glycemic foods (GI <55) 2) Avoid refined sugars and white flour 3) Include high-fiber foods 4) Eat complex carbs with protein 5) Monitor portion sizes 6) Maintain regular meal timing 7) Stay hydrated 8) Include cinnamon and fenugreek",
            "protein": "🥜 Protein Sources: Vegetarian - lentils (18g/cup), chickpeas (15g/cup), quinoa (8g/cup), tofu (20g/cup), Greek yogurt (20g/cup), nuts & seeds. Non-vegetarian - chicken breast (25g/100g), fish (20-25g/100g), eggs (6g each). Target: 0.8-1.6g per kg body weight",
            "vitamins": "🌟 Essential Vitamins: Vitamin D (sunlight, fortified foods), B12 (animal products, supplements), Vitamin C (citrus, berries - 90mg daily), Iron (leafy greens, legumes - 18mg women, 8mg men), Calcium (dairy, sesame - 1200mg), Omega-3 (walnuts, flaxseeds)",
            "hydration": "💧 Hydration Guide: 8-10 glasses daily (35ml per kg body weight), increase with exercise, monitor urine color (pale yellow = good), include herbal teas, coconut water, water-rich foods (cucumber, watermelon), limit caffeine and alcohol",
        }
        
        # Diet plan specific responses
        if current_plan and any(word in user_message for word in ["plan", "diet", "meal", "today", "tomorrow", "day"]):
            if "today" in user_message or "day 1" in user_message:
                day1_meals = current_plan['diet_plan']['Day 1']
                bot_response = f"📋 Your Day 1 Plan (Theme: {day1_meals['theme']}):\\n\\n🌅 Breakfast: {day1_meals['Breakfast']}\\n☕ Mid-Morning: {day1_meals['Mid-Morning']}\\n🍽️ Lunch: {day1_meals['Lunch']}\\n🥤 Evening: {day1_meals['Evening']}\\n🌙 Dinner: {day1_meals['Dinner']}\\n\\n💧 Daily Target: {day1_meals['daily_total']} | {day1_meals['hydration']}"
            elif "nutrition target" in user_message or "target" in user_message:
                targets = current_plan['nutrition_targets']
                bot_response = f"🎯 Your Nutrition Targets:\\n\\n🥩 Protein: {targets['protein']}\\n🍞 Carbs: {targets['carbohydrates']}\\n🥜 Fats: {targets['fats']}\\n🌾 Fiber: {targets['fiber']}\\n💧 Water: {targets['water']}"
            elif "shopping" in user_message or "grocery" in user_message:
                shopping_items = current_plan['shopping_list'][:4]  # First 4 items
                bot_response = f"🛒 Your Shopping List (Top Items):\\n\\n" + "\\n".join([f"✅ {item}" for item in shopping_items]) + "\\n\\nWould you like to see the complete shopping list?"
            elif "recommend" in user_message or "advice" in user_message:
                recommendations = current_plan['health_analysis']['key_recommendations'][:3]
                bot_response = f"💡 Based on your {current_plan['generation_info']['plan_variation']} diet plan:\\n\\n" + "\\n".join([f"• {rec}" for rec in recommendations])
            else:
                plan_focus = current_plan['generation_info']['plan_variation']
                bot_response = f"📖 I can help you with your current {current_plan['patient_profile']['diet_preference']} {plan_focus} diet plan! Ask me about today's meals, nutrition targets, shopping list, or specific dietary advice. What would you like to know?"
        else:
            # Find matching response from general nutrition knowledge
            bot_response = None
            for keyword, response in nutrition_responses.items():
                if any(word in user_message for word in keyword.split()):
                    bot_response = response
                    break
        
        # Default responses for common greetings and questions
        if not bot_response:
            if any(word in user_message for word in ["hello", "hi", "hey", "greetings"]):
                plan_context = f" I can also help with your current {current_plan['patient_profile']['diet_preference']} diet plan!" if current_plan else ""
                bot_response = f"👋 Hello! I'm your AI nutrition expert. I can help with personalized diet advice, weight management, diabetes nutrition, protein guidance, vitamins, hydration, and much more.{plan_context} What specific nutrition topic would you like to explore?"
            elif any(word in user_message for word in ["thank", "thanks"]):
                bot_response = "🙏 You're very welcome! Remember, small consistent changes create lasting health improvements. I'm here whenever you need nutrition guidance. Stay healthy!"
            elif any(word in user_message for word in ["help", "assist"]):
                bot_response = "💡 I can help with: Weight management • Diabetes nutrition • Protein sources • Vitamins & minerals • Hydration • Meal timing • Heart health • Energy optimization. Just ask your specific question!"
            else:
                bot_response = f"🤖 I understand you're asking about nutrition. For personalized advice: Focus on whole foods, stay hydrated, eat balanced meals, and maintain consistency. Could you ask a more specific nutrition question so I can provide detailed guidance?"
        
        return jsonify({
            "response": bot_response,
            "status": "success",
            "timestamp": datetime.now().strftime("%H:%M"),
            "response_type": "nutrition_expert",
            "has_diet_plan": current_plan is not None
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    print("🥗 AI-NutriCare Interactive Dashboard Starting...")
    print("📱 Web Interface: http://localhost:5000")
    print("🎯 Features: Multi-Step Workflow → File Upload → Processing → Diet Plan → Chat")
    print("💬 AI Nutrition Expert: Advanced Q&A with diet plan context")
    print("⚡ Interactive: Beautiful UX with step-by-step processing")
    print("🎨 Modern Design: Animations, transitions, and responsive layout")
    print("🔄 Regenerate Plans: Multiple diet plan variations available")
    print("📋 Optional Fields: Age and diet preference are now optional")
    print("💡 Smart Chat: Chatbot knows about your personalized diet plan")
    print("=" * 80)
    

    app.run(host='0.0.0.0', port=5000, debug=True)
