def analyze_conditions(entities):
    conditions = []

    def get_value(keywords):
        for test_name, data in entities.items():
            for keyword in keywords:
                if keyword in test_name.lower():
                    val = data.get("value")

                    if isinstance(val, list):
                        val = val[0] if len(val) > 0 else None

                    try:
                        return float(val)
                    except (ValueError, TypeError):
                        continue 
        return None

    glucose = get_value(["glucose", "fasting glucose"])
    hba1c = get_value(["hba1c", "glycated"])
    hemoglobin = get_value(["hemoglobin", "hb"])
    ldl = get_value(["ldl"])
    hdl = get_value(["hdl"])
    triglycerides = get_value(["triglycerides"]) 
    vitamin_d = get_value(["vitamin d"])
    vitamin_b12 = get_value(["vitamin b12", "b12"])
    tsh = get_value(["tsh"])
    creatinine = get_value(["creatinine"])

    if glucose is not None:
        if glucose > 110: conditions.append("High Blood Sugar (Hyperglycemia)")
        elif glucose < 70: conditions.append("Low Blood Sugar (Hypoglycemia)")

    if hba1c is not None:
        if hba1c >= 6.5: conditions.append("Diabetes")
        elif 5.7 <= hba1c < 6.5: conditions.append("Prediabetes")

    if hemoglobin is not None:
        if hemoglobin < 13: conditions.append("Anemia Risk (Low Hemoglobin)")
        elif hemoglobin > 17: conditions.append("High Hemoglobin")

    if ldl is not None:
        if ldl > 130: conditions.append("High LDL Cholesterol")
        elif ldl < 40: conditions.append("Low LDL Cholesterol")

    if hdl is not None:
        if hdl < 40: conditions.append("Low HDL Cholesterol")
        elif hdl > 80: conditions.append("High HDL Cholesterol")

    if triglycerides is not None:
        if triglycerides > 150: conditions.append("High Triglycerides")

    if vitamin_d is not None:
        if vitamin_d < 20: conditions.append("Vitamin D Deficiency")

    if vitamin_b12 is not None:
        if vitamin_b12 < 200: conditions.append("Vitamin B12 Deficiency")

    if tsh is not None:
        if tsh > 4.5: conditions.append("Hypothyroidism Risk")
        elif tsh < 0.4: conditions.append("Hyperthyroidism Risk")

    if creatinine is not None:
        if creatinine > 1.3: conditions.append("Possible Kidney Function Impairment")

    return conditions