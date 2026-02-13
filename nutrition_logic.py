def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(bmr, activity_level):
    rates = {
        "sedentary": 1.2,
        "moderate": 1.55,
        "active": 1.725
    }
    return bmr * rates.get(activity_level, 1.2)
