from PIL import Image
import pytesseract
import re
import os
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image_path = r"C:\temp\img"

files = [f for f in os.listdir(image_path) if f.lower().endswith(".jpg")]

for f in files:
    path = os.path.join(image_path, f)
    image = Image.open(path)

    width, height = image.size
    crop_box = (0, 0, width, 900)
    img_croped = image.crop(crop_box)

    text = pytesseract.image_to_string(img_croped, lang="eng")

    match = re.search(r"N[°o]\s+(\d{6})", text)
    toStr = ''
    toStr = str(match.group(1)) if match  else "número da nota não encontrada"
    
    initials = toStr[0:3]
    
    if match.group(1).startswith(initials):
        initial_folder = Path(initials)
        initial_folder.mkdir(parents=True, exist_ok=True)
        file_name = initial_folder / f"Nota {toStr}.jpg"
        image.save(file_name)
        # print(f"{f}: Número encontrado = {match.group(1)}")
    else:
        print(f"{f}: Núemro da Nota {image} não encontrada!")

