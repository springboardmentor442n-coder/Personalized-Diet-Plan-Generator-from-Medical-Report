import json
import re
with open("outputs/report_data.json","r") as f:
    data=json.load(f)

def analyze_health(data):
    results={}

    # Diabetes Risk
    if data["hba1c"] < 5.7:
        results["diabetes"] = "Low Risk"
    elif data["hba1c"] < 6.5:
        results["diabetes"] = "Pre-Diabetes"
    else:
        results["diabetes"] = "High Risk"

    # Cholesterol
    if data["total_cholesterol"] < 200:
        results["cholesterol"] = "Normal"
    else:
        results["cholesterol"] = "High"
    
      # Vitamin D
    if data["vitamin_d"] < 50:
        results["vitamin_d"] = "Deficient"
    else:
        results["vitamin_d"] = "Sufficient"
    
    # ---- FASTING GLUCOSE ----
    glucose = data.get("fasting_glucose")
    if glucose is not None:
        if glucose < 100:
            results["sugar_level"] = "Normal"
        elif glucose < 126:
            results["sugar_level"] = "Prediabetes"
        else:
            results["sugar_level"] = "High"
    
    # ---- HDL ----
    hdl = data.get("hdl")
    if hdl is not None:
        results["hdl_status"] = "Good" if hdl >= 40 else "Low"
    
    # ---- LDL ----
    ldl = data.get("ldl")
    if ldl is not None:
        if ldl < 100:
            results["ldl_status"] = "Optimal"
        elif ldl < 160:
            results["ldl_status"] = "Borderline"
        else:
            results["ldl_status"] = "High"

    #-----Thyroid------
    tsh=data.get("tsh")
    if tsh is not None:
        if tsh<0.5:
            results["thyroid"]="Hyperthyroid"
        elif tsh>4.5:
            results["thyroid"]="Hypothyroid"
        else:
            results["thyroid"]="Normal"

     # ---- HEMOGLOBIN ----
    hb = data.get("hemoglobin")
    if hb is not None:
        results["hemoglobin"] = "Low (Anemia Risk)" if hb < 13 else "Normal"

        # ---- TRIGLYCERIDES ----
    tg = data.get("triglycerides")
    if tg is not None:
        results["triglycerides_status"] = "Normal" if tg < 150 else "High"
    
    return results

analysis=analyze_health(data)

with open("outputs/analysis.json", "w") as f:
        json.dump(analysis, f, indent=4)

print(analysis)


