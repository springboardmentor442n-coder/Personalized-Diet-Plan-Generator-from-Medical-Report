from pathlib import Path
from typing import List
from PIL import Image
import pypdfium2 as pdfium
import io
import base64
from groq import Groq
from config import settings
from PyPDF2 import PdfReader

# Initialize Groq client
client = Groq(api_key=settings.GROQ_API_KEY)

# --- OCR PROMPT ---
OCR_PROMPT = """
Act as an accurate OCR engine.
Transcribe the image exactly.
Preserve headings and lab values.
Do NOT summarize.
Return only plain text.
"""

# ---------------------------------------------------
# LOAD DOCUMENT (FOR OCR FALLBACK)
# ---------------------------------------------------
def load_document(file_path: str) -> List[Image.Image]:

    ext = Path(file_path).suffix.lower()

    # PDF Case
    if ext == ".pdf":
        pdf = pdfium.PdfDocument(file_path)
        images = []

        # Process only first page for speed
        for i in range(min(1, len(pdf))):
            page = pdf[i]
            bitmap = page.render(scale=100 / 72)  # reduced resolution
            pil_image = bitmap.to_pil()
            images.append(pil_image)
            page.close()

        return images

    # Image Case
    if ext in [".jpg", ".jpeg", ".png"]:
        return [Image.open(file_path)]

    raise ValueError(f"Unsupported file type: {ext}")


# ---------------------------------------------------
# ENCODE IMAGE FOR GROQ
# ---------------------------------------------------
def encode_pil_image(image: Image.Image) -> str:

    buffer = io.BytesIO()

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(buffer, format="JPEG", quality=70)  # lower quality for speed

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# ---------------------------------------------------
# CALL GROQ VISION OCR
# ---------------------------------------------------
def get_markdown_from_page(image: Image.Image) -> str:

    base64_image = encode_pil_image(image)

    response = client.chat.completions.create(
        model=settings.OCR_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": OCR_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=800,  # reduced for speed
        temperature=0.1
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# MAIN DOCUMENT PROCESSOR
# ---------------------------------------------------
def process_document(file_path: str) -> str:

    # -----------------------------
    # STEP 1: Try Direct PDF Extraction
    # -----------------------------
    try:
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            if text.strip():
                print("✅ Using direct PDF text extraction.")
                return text

    except Exception as e:
        print("Direct PDF extraction failed:", e)

    # -----------------------------
    # STEP 2: Fallback to Vision OCR
    # -----------------------------
    print("⚠️ Falling back to Vision OCR...")

    images = load_document(file_path)
    pages_text = []

    for i, image in enumerate(images):
        print(f"Processing page {i+1} with OCR...")
        text = get_markdown_from_page(image)
        pages_text.append(text)

    return "\n\n".join(pages_text)
