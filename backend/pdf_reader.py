import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract full raw text from a PDF file.
    Returns combined text of all pages.
    """

    full_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()

            if page_text:
                full_text.append(f"\n\n--- PAGE {page_number} ---\n\n")
                full_text.append(page_text)

    return "\n".join(full_text)
