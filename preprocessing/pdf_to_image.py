from pdf2image import convert_from_path

POPPLER_PATH = r"C:\\Users\\hp5cd\\Downloads\\Release-25.12.0-0\\poppler-25.12.0\\Library\\bin"

def pdf_to_images(pdf_path, dpi=120):
    pages = convert_from_path(
        pdf_path,
        dpi=dpi,
        poppler_path=POPPLER_PATH
    )
    return pages  
