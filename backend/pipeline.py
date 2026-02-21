from backend.pdf_reader import extract_text_from_pdf
from backend.extraction import extract_structured_data
from backend.analyzer import (
    analyze_report,
    add_abnormal_summary,
    calculate_health_score
)

def run_pipeline(pdf_path):

    # Step 1: Extract raw text
    raw_text = extract_text_from_pdf(pdf_path)

    # Step 2: Structure extraction
    structured_data = extract_structured_data(raw_text)

    # Step 3: Interpretation + severity
    structured_data = analyze_report(structured_data)

    # Step 4: Abnormal summary
    structured_data = add_abnormal_summary(structured_data)

    # Step 5: Health score
    structured_data = calculate_health_score(structured_data)

    return structured_data