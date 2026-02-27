"""
OCR Text Extraction Module
Handles extraction of text from PDF and image files
"""
import os
import pdfplumber
import pytesseract
from PIL import Image
import re

def extract_text_from_pdf(filepath):
    """Extract text from PDF using pdfplumber"""
    try:
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_image(filepath):
    """Extract text from image using pytesseract OCR"""
    try:
        # Open and process image
        image = Image.open(filepath)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using OCR
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def extract_text_from_file(filepath):
    """
    Main function to extract text from any supported file type
    Supports: PDF, PNG, JPG, JPEG
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    file_extension = os.path.splitext(filepath)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(filepath)
    elif file_extension in ['.png', '.jpg', '.jpeg']:
        return extract_text_from_image(filepath)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def clean_extracted_text(text):
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    # Remove special characters that might interfere with parsing
    text = re.sub(r'[^\w\s\.\,\:\-\(\)\/]', ' ', text)
    
    # Normalize multiple spaces
    text = re.sub(r' +', ' ', text)
    
    return text.strip()

def extract_and_clean_text(filepath):
    """Extract and clean text from file in one step"""
    raw_text = extract_text_from_file(filepath)
    cleaned_text = clean_extracted_text(raw_text)
    
    # Basic validation - ensure we got some text
    if len(cleaned_text) < 10:
        raise ValueError("Extracted text is too short or empty. Please check if the file contains readable text.")
    
    return cleaned_text