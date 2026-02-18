import re

def extract_lab_values(text: str) -> dict:
    labs = {}

    patterns = {
    "Glucose": r"Glucose\s*[:\-]?\s*(\d+\.?\d*)",
    "Cholesterol": r"Cholesterol\s*[:\-]?\s*(\d+\.?\d*)",
    "Triglycerides": r"Triglycerides\s*[:\-]?\s*(\d+\.?\d*)",
    "BMI": r"BMI\s*[:\-]?\s*(\d+\.?\d*)",
    "HbA1c": r"HbA1c\s*[:\-]?\s*(\d+\.?\d*)",
    "Vitamin D": r"Vitamin\s*D\s*[:\-]?\s*(\d+\.?\d*)",
    "Creatinine": r"Creatinine\s*[:\-]?\s*(\d+\.?\d*)",
    "eGFR": r"eGFR\s*[:\-]?\s*(\d+\.?\d*)"
}


    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            labs[key] = float(match.group(1))

    return labs
