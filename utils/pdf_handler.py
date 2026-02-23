import pdfplumber
import pytesseract
import cv2
import numpy as np
import os
from PIL import Image

# UNCOMMENT the line below and point to your tesseract.exe if you are on Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_report(pdf_path):
    """
    Extracts text from a PDF, using OCR as a fallback for scanned images.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # 1. Try direct text extraction (for digital PDFs)
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text += page_text + "\n"
                else:
                    # 2. Fallback to OCR (for scanned images/reports)
                    # Convert PDF page to high-res image
                    image = page.to_image(resolution=300).original
                    
                    # Convert to OpenCV format (BGR to Grayscale)
                    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                    
                    # Optional: Thresholding to clean up the 'noise' for better OCR
                    _, thresh = cv2.threshold(open_cv_image, 150, 255, cv2.THRESH_BINARY)
                    
                    text += pytesseract.image_to_string(thresh) + "\n"
        return text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"