import re

def extract_lab_values(text: str) -> dict:
    labs = {}

    # Normalize text
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    patterns = {
        "Glucose": r"(glucose[^0-9]{0,50})(\d+\.?\d*)",
        "Cholesterol": r"(cholesterol[^0-9]{0,50})(\d+\.?\d*)",
        "Triglycerides": r"(triglycerides[^0-9]{0,50})(\d+\.?\d*)",
        "BMI": r"(bmi[^0-9]{0,50})(\d+\.?\d*)",
        "HbA1c": r"(hba1c[^0-9]{0,50})(\d+\.?\d*)",
        "Vitamin D": r"(vitamin\s*d[^0-9]{0,50})(\d+\.?\d*)",
        "Creatinine": r"(creatinine[^0-9]{0,50})(\d+\.?\d*)",
        "eGFR": r"(egfr[^0-9]{0,50})(\d+\.?\d*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(2))
            labs[key] = value

    return labs

