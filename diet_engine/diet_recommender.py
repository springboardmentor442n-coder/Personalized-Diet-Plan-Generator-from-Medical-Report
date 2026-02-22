from medical_rules import analyze_conditions

IMPORTANT_TESTS = [
    "glucose", "hba1c", "cholesterol",
    "ldl", "hdl", "triglycerides",
    "vitamin d", "vitamin b12",
    "creatinine", "tsh"
]

def filter_relevant_entities(entities):
    return {
        k: v for k, v in entities.items()
        if any(test in k.lower() for test in IMPORTANT_TESTS)
    }


def generate_diet_plan(entities, bmi=None, bmi_category=None):

    filtered_entities = filter_relevant_entities(entities)
    conditions = analyze_conditions(filtered_entities)

    return {
        "BMI": bmi,
        "BMI Category": bmi_category,
        "Detected Conditions": conditions,
        "Extracted Medical Values": entities
    }
