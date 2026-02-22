import re
import json
from llm.llm_extractor import call_llm_extraction

GENERIC_PATTERN = re.compile(
    r"([A-Za-z][A-Za-z0-9 ,()/\-]+?)\s+([\d]+\.?[\d]*)\s*(mg/dL|g/dL|%|pg/mL|ng/mL|U/L|mEq/L|fL|thou/mm3|nmol/L|µIU/mL)?",
    re.IGNORECASE
)

def extract_entities_regex(text):
    entities = {}

    matches = GENERIC_PATTERN.findall(text)

    for match in matches:
        test_name = match[0].strip()
        value = float(match[1])
        unit = match[2] if match[2] else ""

        if 0 < value < 10000:
            entities[test_name] = {
                "value": value,
                "unit": unit
            }
    return entities


def extract_entities(text):
    entities = {}

    regex_entities = extract_entities_regex(text)

    if len(regex_entities) < 5:
        llm_entities = call_llm_extraction(text)

        # If LLM returns valid data, use it
        if llm_entities:
            return llm_entities

    return regex_entities
