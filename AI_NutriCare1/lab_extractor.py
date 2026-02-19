import re

def extract_lab_values(text):
    return {
        "hemoglobin": _find(text, r"hemoglobin\s*[:\-]?\s*(\d+\.?\d*)"),
        "glucose": _find(text, r"glucose\s*[:\-]?\s*(\d+\.?\d*)"),
        "tsh": _find(text, r"tsh\s*[:\-]?\s*(\d+\.?\d*)")
    }

def _find(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1)) if match else None
