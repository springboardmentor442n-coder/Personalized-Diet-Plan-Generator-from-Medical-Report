# condition_detector.py

def detect_conditions(values):
    conditions = []

    if values["hemoglobin"] and values["hemoglobin"] < 12:
        conditions.append("Anemia")

    if values["glucose"] and values["glucose"] > 126:
        conditions.append("Diabetes Risk")

    if values["tsh"] and values["tsh"] > 4:
        conditions.append("Thyroid Imbalance")

    if not conditions:
        conditions.append("Normal")

    return conditions


def assess_risk(values):
    return {
        "Heart Risk": "Moderate",
        "Diabetes Risk": "High" if values["glucose"] and values["glucose"] > 126 else "Low"
    }
