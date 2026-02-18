# backend/analysis.py

def evaluate_health(labs):

    status = {}

    for key, value in labs.items():

        if key == "Glucose":
            if value >= 126:
                status[key] = "High"
            elif value >= 100:
                status[key] = "Prediabetic"
            else:
                status[key] = "Normal"

        elif key == "HbA1c":
            if value >= 6.5:
                status[key] = "Diabetic"
            elif value >= 5.7:
                status[key] = "Prediabetic"
            else:
                status[key] = "Normal"

        elif key == "Cholesterol":
            if value >= 240:
                status[key] = "High"
            elif value >= 200:
                status[key] = "Borderline"
            else:
                status[key] = "Normal"

        elif key == "Vitamin D":
            if value < 20:
                status[key] = "Deficient"
            elif value < 30:
                status[key] = "Insufficient"
            else:
                status[key] = "Normal"

        elif key == "Creatinine":
            if value > 1.3:
                status[key] = "High"
            else:
                status[key] = "Normal"

        elif key == "eGFR":
            if value < 60:
                status[key] = "Kidney Risk"
            else:
                status[key] = "Normal"

        else:
            status[key] = "Check"

    return status


def calculate_risk_score(health_status):

    score = 0

    for condition in health_status.values():

        if condition in ["High", "Diabetic", "Kidney Risk"]:
            score += 20
        elif condition in ["Borderline", "Prediabetic", "Insufficient"]:
            score += 10
        elif condition == "Deficient":
            score += 15

    return min(score, 100)
