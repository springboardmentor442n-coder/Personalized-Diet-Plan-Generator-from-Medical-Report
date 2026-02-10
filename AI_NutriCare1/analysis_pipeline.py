from ocr_utils import extract_text
from lab_extractor import extract_lab_values
from condition_detector import detect_conditions, assess_risk
from diet_ai import generate_ai_diet
import pandas as pd

import pandas as pd
import re

import pandas as pd
import re

def parse_to_table(ai_text):
    rows = []

    current_day = None
    row = {}

    for line in ai_text.splitlines():
        line = line.strip()

        if re.match(r"Day\s+\d+", line):
            if row:
                rows.append(row)
            current_day = line
            row = {
                "Day": current_day,
                "Breakfast": "",
                "Lunch": "",
                "Dinner": "",
                "Calories": ""
            }

        elif line.lower().startswith("breakfast"):
            row["Breakfast"] = line.split(":", 1)[-1].strip()

        elif line.lower().startswith("lunch"):
            row["Lunch"] = line.split(":", 1)[-1].strip()

        elif line.lower().startswith("dinner"):
            row["Dinner"] = line.split(":", 1)[-1].strip()

        elif "calorie" in line.lower():
            row["Calories"] = line.split(":", 1)[-1].strip()

    if row:
        rows.append(row)

    return pd.DataFrame(rows)


def analyze_report(file_path, age, gender, weight, food_type):
    text = extract_text(file_path)
    values = extract_lab_values(text)
    conditions = detect_conditions(values)
    risks = assess_risk(values)

    ai_diet = generate_ai_diet(
        age, gender, weight, food_type, values, conditions
    )

    diet_table = parse_to_table(ai_diet)

    return {
        "values": values,
        "conditions": conditions,
        "risks": risks,
        "ai_diet": ai_diet,
        "diet_table": diet_table
    }
