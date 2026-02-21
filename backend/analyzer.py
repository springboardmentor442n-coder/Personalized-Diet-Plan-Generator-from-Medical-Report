import re


def parse_reference_range(ref_range: str):
    """
    Parse reference range string.
    Supports:
    - "8.7 - 10.4"
    - "<2.00"
    - ">59"
    Returns tuple: (type, lower, upper)
    """

    if not ref_range:
        return None, None, None

    ref_range = ref_range.strip()

    # Range: "8.7 - 10.4"
    range_match = re.match(r"([\d.]+)\s*-\s*([\d.]+)", ref_range)
    if range_match:
        lower = float(range_match.group(1))
        upper = float(range_match.group(2))
        return "range", lower, upper

    # Less than: "<2.00"
    less_match = re.match(r"<\s*([\d.]+)", ref_range)
    if less_match:
        limit = float(less_match.group(1))
        return "less_than", None, limit

    # Greater than: ">59"
    greater_match = re.match(r">\s*([\d.]+)", ref_range)
    if greater_match:
        limit = float(greater_match.group(1))
        return "greater_than", limit, None

    return None, None, None


def determine_interpretation(value_str: str, ref_range: str):
    """
    Determine if value is low, normal, or high.
    """

    try:
        value = float(value_str)
    except (ValueError, TypeError):
        return "unknown"

    range_type, lower, upper = parse_reference_range(ref_range)

    if range_type == "range":
        if value < lower:
            return "low"
        elif value > upper:
            return "high"
        else:
            return "normal"

    elif range_type == "less_than":
        if value < upper:
            return "normal"
        else:
            return "high"

    elif range_type == "greater_than":
        if value > lower:
            return "normal"
        else:
            return "low"

    return "unknown"


def calculate_severity(value, low, high):
    try:
        value = float(value)
        low = float(low)
        high = float(high)

        if low <= value <= high:
            return "normal"

        if value < low:
            deviation = (low - value) / low
        else:
            deviation = (value - high) / high

        # More realistic thresholds
        if deviation < 0.20:
            return "mild"
        elif deviation < 0.50:
            return "moderate"
        else:
            return "critical"

    except:
        return "unknown"

def analyze_report(structured_data: dict) -> dict:
    """
    Add interpretation and severity to each test.
    """

    for test in structured_data.get("tests", []):
        value = test.get("value", "")
        ref_range = test.get("reference_range", "")

        interpretation = determine_interpretation(value, ref_range)
        test["interpretation"] = interpretation

        # Parse range to calculate severity
        range_type, lower, upper = parse_reference_range(ref_range)

        if range_type == "range" and interpretation in ["low", "high"]:
            severity = calculate_severity(value, lower, upper)
        else:
            severity = "normal" if interpretation == "normal" else "unknown"

        test["severity"] = severity

    return structured_data


TEST_WEIGHTS = {
    "T3, Total": 3,
    "T4, Total": 3,
    "TSH": 4,
    "Calcium, Total": 3,
    "Alkaline Phosphatase (ALP)": 2,
    "AST (SGOT)": 1,
    "Basophils": 1,
}

def calculate_health_score(structured_data: dict) -> dict:
    tests = structured_data.get("tests", [])

    total = len(tests)
    normal = sum(1 for t in tests if t.get("interpretation") == "normal")
    abnormal = total - normal

    total_weight = 0
    penalty = 0

    for test in tests:
        weight = TEST_WEIGHTS.get(test["test_name"], 1)
        total_weight += weight

        if test["interpretation"] != "normal":
            if test["severity"] == "mild":
                penalty += 1 * weight
            elif test["severity"] == "moderate":
                penalty += 2 * weight
            elif test["severity"] == "critical":
                penalty += 4 * weight

    if total_weight == 0:
        score = 0
    else:
        score = max(0, int(100 - (penalty / total_weight) * 100))

    structured_data["health_score"] = score
    structured_data["total_tests"] = total
    structured_data["normal_tests"] = normal
    structured_data["abnormal_count"] = abnormal

    return structured_data


def add_abnormal_summary(structured_data: dict) -> dict:

    abnormal = []

    for test in structured_data.get("tests", []):
        if test.get("interpretation") not in ["normal", "unknown"]:
            abnormal.append({
                "test_name": test.get("test_name"),
                "value": test.get("value"),
                "reference_range": test.get("reference_range"),
                "interpretation": test.get("interpretation"),
                "severity": test.get("severity")
            })

    structured_data["abnormal_findings"] = abnormal

    return structured_data