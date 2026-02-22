import re

def clean_ocr_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", text)

    text = re.sub(r"mg\s*/\s*d\s*l", "mg/dl", text)
    text = re.sub(r"\s*%\s*", " %", text)

    text = re.sub(r"\s+", " ", text)

    replacements = {
        "hba1 c": "hba1c",
        "hb a1c": "hba1c",
        "ld l": "ldl",
        "hdl l": "hdl",
        "cholest erol": "cholesterol",
        "fast ing": "fasting",
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    medical_terms = [
        "hba1c",
        "fasting glucose",
        "ldl cholesterol",
        "hdl cholesterol",
        "blood pressure",
        "weight",
        "height",
    ]

    for term in medical_terms:
        text = re.sub(rf'\b{re.escape(term)}\b', term.title(), text, flags=re.IGNORECASE)

    return text.strip()
