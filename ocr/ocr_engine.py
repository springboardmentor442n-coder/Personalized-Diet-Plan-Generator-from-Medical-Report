import pytesseract
from PIL import Image
from typing import Iterable, Union

def extract_text_from_images(images: Iterable[Union[str, Image.Image]]) -> str:
    text_chunks = []

    for img in images:
        if isinstance(img, str):
            img = Image.open(img)

        text = pytesseract.image_to_string(
            img,
            lang="eng",
            config="--oem 3 --psm 6"
        )

        text_chunks.append(text)

    return "\n".join(text_chunks).strip()
