def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        return round((10 * weight) + (6.25 * height) - (5 * age) + 5, 0)
    else:
        return round((10 * weight) + (6.25 * height) - (5 * age) - 161, 0)


def calculate_tdee(bmr, activity_level="moderate"):
    activity_rates = {
        "sedentary": 1.2,
        "moderate": 1.55,
        "active": 1.725
    }
    return round(bmr * activity_rates.get(activity_level, 1.55), 0)





def generate_diet(medical_data, diet_type, country, region, age, weight, height, gender):

    diet = {}

    # ================= BMI =================
    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)

    # ================= BMR & TDEE =================
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr)

    # ================= Sugar Status =================
    hba1c = medical_data.get("HbA1c")

    if hba1c is None:
        sugar_status = "Not Available"
    elif hba1c < 5.7:
        sugar_status = "Normal"
    elif hba1c < 6.5:
        sugar_status = "Prediabetic Risk"
    else:
        sugar_status = "High Diabetes Risk"

# ================= Cholesterol Status =================
    chol = medical_data.get("Total Cholesterol")

    if chol is None:
        chol_status = "Not Available"
    elif chol < 200:
        chol_status = "Normal"
    elif chol < 240:
        chol_status = "Borderline High"
    else:
        chol_status = "High"

    # ================= Overall Risk =================
    risk_score = 0

    if bmi_status in ["Overweight", "Obese"]:
        risk_score += 1
    if hba1c and hba1c >= 5.7:
        risk_score += 1
    if chol and chol >= 200:
        risk_score += 1

    if risk_score == 0:
        overall_risk = "Low"
    elif risk_score == 1:
        overall_risk = "Moderate"
    else:
        overall_risk = "High"

    # ================= Initialize Lists =================
    breakfast_list = []
    lunch_list = []
    dinner_list = []

    snack_list = [
        "Fruit bowl",
        "Mixed nuts",
        "Greek yogurt",
        "Buttermilk",
        "Green tea & almonds",
        "Coconut water",
        "Protein smoothie"
    ]

    # ====================================================
    # 🇮🇳 INDIA
    # ====================================================
    if country == "India":

        # -------- SOUTH INDIA --------
        if region == "South":

            if diet_type == "Vegetarian":
                breakfast_list = [
                    "Idli with sambar",
                    "Rava dosa",
                    "Upma",
                    "Pongal",
                    "Vegetable uttapam",
                    "Appam with stew",
                    "Lemon rice"
                ]
                lunch_list = [
                    "Sambar rice",
                    "Curd rice",
                    "Vegetable biryani",
                    "Rasam with rice",
                    "Avial with rice",
                    "Puliyodarai",
                    "Coconut rice"
                ]
                dinner_list = [
                    "Chapati & veg kurma",
                    "Tomato soup & salad",
                    "Vegetable kootu",
                    "Paneer curry",
                    "Lentil dosa",
                    "Spinach dal",
                    "Mixed veg stir fry"
                ]

            else:
                breakfast_list = [
                    "Egg dosa",
                    "Omelette with idli",
                    "Boiled eggs",
                    "Chicken sandwich",
                    "Egg uttapam",
                    "Egg appam",
                    "Scrambled eggs"
                ]
                lunch_list = [
                    "Chicken curry & rice",
                    "Fish curry",
                    "Egg curry rice",
                    "Prawn masala",
                    "Grilled fish",
                    "Chicken biryani (moderate)",
                    "Mutton curry (light)"
                ]
                dinner_list = [
                    "Grilled chicken",
                    "Fish with vegetables",
                    "Egg curry",
                    "Chicken soup",
                    "Prawn stir fry",
                    "Chicken salad",
                    "Baked fish"
                ]

        # -------- NORTH INDIA --------
        elif region == "North":

            if diet_type == "Vegetarian":
                breakfast_list = [
                    "Paneer paratha",
                    "Poha",
                    "Vegetable sandwich",
                    "Besan chilla",
                    "Oats porridge",
                    "Stuffed paratha",
                    "Upma"
                ]
                lunch_list = [
                    "Dal makhani & roti",
                    "Rajma chawal",
                    "Chole & rice",
                    "Vegetable pulao",
                    "Kadhi chawal",
                    "Palak paneer & roti",
                    "Mix veg curry"
                ]
                dinner_list = [
                    "Chapati & paneer",
                    "Vegetable soup",
                    "Tofu stir fry",
                    "Dal & salad",
                    "Grilled vegetables",
                    "Khichdi",
                    "Mushroom curry"
                ]

            else:
                breakfast_list = [
                    "Boiled eggs",
                    "Omelette & toast",
                    "Chicken sandwich",
                    "Egg bhurji",
                    "Egg paratha",
                    "Protein smoothie",
                    "Scrambled eggs"
                ]
                lunch_list = [
                    "Chicken curry & roti",
                    "Grilled chicken",
                    "Fish tikka",
                    "Chicken pulao",
                    "Egg curry",
                    "Tandoori chicken",
                    "Lean chicken bowl"
                ]
                dinner_list = [
                    "Grilled fish",
                    "Chicken soup",
                    "Egg curry",
                    "Chicken salad",
                    "Baked chicken",
                    "Fish curry",
                    "Lean chicken stir fry"
                ]

        # -------- EAST INDIA --------
        elif region == "East":

            if diet_type == "Vegetarian":
                breakfast_list = [
                    "Poha",
                    "Sprouts salad",
                    "Vegetable sandwich",
                    "Oats porridge",
                    "Upma",
                    "Fruit bowl",
                    "Idli"
                ]
                lunch_list = [
                    "Rice & dal",
                    "Vegetable curry",
                    "Rajma rice",
                    "Khichdi",
                    "Palak rice",
                    "Chole rice",
                    "Veg pulao"
                ]
                dinner_list = [
                    "Chapati & sabzi",
                    "Vegetable soup",
                    "Paneer curry",
                    "Tofu stir fry",
                    "Dal & salad",
                    "Light khichdi",
                    "Mixed vegetables"
                ]

            else:
                breakfast_list = [
                    "Boiled eggs",
                    "Egg sandwich",
                    "Omelette",
                    "Chicken wrap",
                    "Scrambled eggs",
                    "Egg toast",
                    "Protein smoothie"
                ]
                lunch_list = [
                    "Fish curry & rice",
                    "Chicken curry",
                    "Egg curry",
                    "Grilled fish",
                    "Chicken rice bowl",
                    "Prawn curry",
                    "Lean chicken"
                ]
                dinner_list = [
                    "Grilled fish",
                    "Chicken soup",
                    "Egg curry",
                    "Fish stew",
                    "Chicken salad",
                    "Baked fish",
                    "Light chicken curry"
                ]

        # -------- WEST INDIA --------
        else:

            if diet_type == "Vegetarian":
                breakfast_list = [
                    "Dhokla",
                    "Thepla",
                    "Upma",
                    "Vegetable poha",
                    "Oats",
                    "Fruit smoothie",
                    "Sprouts"
                ]
                lunch_list = [
                    "Dal & roti",
                    "Vegetable pulao",
                    "Kadhi & rice",
                    "Bhindi sabzi",
                    "Rajma & rice",
                    "Mixed veg curry",
                    "Khichdi"
                ]
                dinner_list = [
                    "Chapati & paneer",
                    "Vegetable soup",
                    "Tofu stir fry",
                    "Dal & salad",
                    "Grilled vegetables",
                    "Light sabzi",
                    "Mushroom curry"
                ]

            else:
                breakfast_list = [
                    "Boiled eggs",
                    "Egg bhurji",
                    "Chicken sandwich",
                    "Protein smoothie",
                    "Omelette",
                    "Egg wrap",
                    "Scrambled eggs"
                ]
                lunch_list = [
                    "Chicken curry",
                    "Fish fry (light)",
                    "Grilled chicken",
                    "Egg curry",
                    "Chicken pulao",
                    "Lean mutton (light)",
                    "Fish curry"
                ]
                dinner_list = [
                    "Grilled fish",
                    "Chicken soup",
                    "Egg curry",
                    "Chicken salad",
                    "Baked fish",
                    "Lean chicken",
                    "Vegetable chicken stir fry"
                ]

    # ====================================================
    # 🇺🇸 USA
    # ====================================================
    elif country == "USA":

        if diet_type == "Vegetarian":
            breakfast_list = [
                "Avocado toast",
                "Oatmeal with berries",
                "Smoothie bowl",
                "Peanut butter toast",
                "Greek yogurt & fruit",
                "Granola bowl",
                "Chia pudding"
            ]
            lunch_list = [
                "Quinoa salad",
                "Veggie wrap",
                "Tofu bowl",
                "Lentil soup",
                "Veggie burger",
                "Chickpea salad",
                "Brown rice bowl"
            ]
            dinner_list = [
                "Grilled tofu",
                "Veg stir fry",
                "Vegetable pasta",
                "Mushroom risotto",
                "Stuffed peppers",
                "Baked sweet potato",
                "Vegetable tacos"
            ]

        else:
            breakfast_list = [
                "Scrambled eggs",
                "Turkey sandwich",
                "Protein smoothie",
                "Boiled eggs",
                "Egg white omelette",
                "Chicken wrap",
                "Greek yogurt & nuts"
            ]
            lunch_list = [
                "Grilled chicken salad",
                "Salmon bowl",
                "Turkey sandwich",
                "Chicken rice bowl",
                "Fish tacos",
                "Lean steak",
                "Chicken quinoa bowl"
            ]
            dinner_list = [
                "Baked salmon",
                "Grilled chicken",
                "Lean steak",
                "Shrimp stir fry",
                "Chicken pasta",
                "Turkey meatballs",
                "Fish & vegetables"
            ]

    # ====================================================
    # 🇬🇧 UK
    # ====================================================
    elif country == "UK":

        if diet_type == "Vegetarian":
            breakfast_list = [
                "Porridge with berries",
                "Whole grain toast",
                "Fruit smoothie",
                "Avocado toast",
                "Greek yogurt",
                "Chia pudding",
                "Oat pancakes"
            ]
            lunch_list = [
                "Vegetable soup",
                "Lentil curry",
                "Quinoa salad",
                "Veg sandwich",
                "Tofu stir fry",
                "Baked beans & toast",
                "Veg pasta"
            ]
            dinner_list = [
                "Grilled vegetables",
                "Stuffed peppers",
                "Vegetable pie",
                "Tofu bowl",
                "Mushroom risotto",
                "Veg curry",
                "Baked sweet potato"
            ]

        else:
            breakfast_list = [
                "Boiled eggs",
                "Scrambled eggs",
                "Grilled chicken toast",
                "Protein smoothie",
                "Turkey sandwich",
                "Egg sandwich",
                "Greek yogurt"
            ]
            lunch_list = [
                "Grilled chicken",
                "Fish & vegetables",
                "Chicken sandwich",
                "Salmon salad",
                "Turkey wrap",
                "Lean steak",
                "Chicken rice bowl"
            ]
            dinner_list = [
                "Baked salmon",
                "Grilled chicken",
                "Fish pie (light)",
                "Chicken soup",
                "Turkey meatballs",
                "Shrimp stir fry",
                "Lean steak"
            ]

    # ====================================================
    # Build 7-Day Plan
    # ====================================================
    weekly_plan = {}

    for day in range(7):
        weekly_plan[f"Day {day+1}"] = {
            "Breakfast": breakfast_list[day],
            "Mid-Morning Snack": snack_list[day],
            "Lunch": lunch_list[day],
            "Evening Snack": "Green tea",
            "Dinner": dinner_list[day]
        }

    # ================= Alerts =================
    alerts = []

    if chol and chol > 200:
        alerts.append("⚠️ High Cholesterol: Reduce fried and saturated fats.")

    if hba1c and hba1c >= 5.7:
        alerts.append("⚠️ Elevated Sugar Levels: Limit refined carbs and sugar.")

    if bmi_status in ["Overweight", "Obese"]:
        alerts.append("⚠️ BMI indicates weight management recommended.")

    # ================= Health Tips =================
    tips = [
        "💧 Drink 2.5–3 liters of water daily",
        "🚶 Walk 8,000–10,000 steps daily",
        "😴 Sleep 7–8 hours",
        "🥗 Increase fiber intake",
        "🩺 Monitor blood parameters monthly"
    ]
     # ================= Final Dictionary =================
    diet["Weekly Plan"] = weekly_plan
    diet["Alerts"] = alerts
    diet["Tips"] = tips
    diet["Condition"] = medical_data.get("Condition", "Normal")
    diet["BMI"] = bmi
    diet["BMI Status"] = bmi_status
    diet["BMR"] = bmr
    diet["TDEE"] = tdee
    diet["Sugar Status"] = sugar_status
    diet["Cholesterol Status"] = chol_status
    diet["Overall Risk"] = overall_risk
    diet["Age"] = age
    diet["Weight"] = weight
    diet["Height"] = height
    diet["Gender"] = gender

    return diet
