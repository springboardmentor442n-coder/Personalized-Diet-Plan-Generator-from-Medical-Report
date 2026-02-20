import fitz  # PyMuPDF
import os

pdf_path = "data/blood_test_report.pdf"
output_folder = "data"

doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    pix = page.get_pixmap()
    image_path = os.path.join(output_folder, f"page_{page_num}.png")
    pix.save(image_path)

print("PDF converted to images successfully!")
