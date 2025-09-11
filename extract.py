from PIL import Image
import pytesseract
import re
import os
from pathlib import Path

def extractInvoices():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    stack = []

    image_path = r"C:\temp\img"

    files = [f for f in os.listdir(image_path) if f.lower().endswith(".jpg")]

    for f in files:
        path = os.path.join(image_path, f)
        image = Image.open(path)

        width, height = image.size
        crop_box = (0, 0, width, 900)
        img_croped = image.crop(crop_box)

        text = pytesseract.image_to_string(img_croped, lang="eng")
        
        savFileToTxt(text, f)

        invoiceSixNumbers = re.search(r"N[°o]\s+(\d{6})", text)
        invoiceTreeNumbers = re.search(r"N[°o]\s+(\d{3})", text)
        
        if invoiceSixNumbers:
            stack.append(invoiceSixNumbers.group(1))
        elif invoiceTreeNumbers:
            stack.append(invoiceTreeNumbers.group(1))
        else:
            stack.append(f"err {f}")
        
        
        for s in stack:
            createAndSaveToFolder(s, image, f)

        
def createAndSaveToFolder(elem, image, file):
    if len(elem) == 3:
        folder_name = Path("Três Digitos")
        folder_name.mkdir(parents=True, exist_ok=True)
        file_name = folder_name / f"Nota{elem}.jpg"
        image.save(file_name)
            
    initials = elem[0:3]
            
    if initials.startswith("err"):
        folder_name = Path("Não encontrados")
        folder_name.mkdir(parents=True, exist_ok=True)
        file_name = folder_name / f"{file} não encontrado.jpg"
        image.save(file_name)
    elif elem.startswith(initials) and not elem.startswith("err"):
        initial_folder = Path(initials)
        initial_folder.mkdir(parents=True, exist_ok=True)
        file_name = initial_folder / f"Nota {elem}.jpg"
        image.save(file_name)


def savFileToTxt(text, file):
    pasta_destino = "textos_extraidos"
    file_name = f"{file}.txt"
    caminho_arquivo = os.path.join(pasta_destino, file_name)
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino) 
    
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(text)
            print(f"Texto salvo com sucesso em: {caminho_arquivo}")
    except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")
            
extractInvoices()
                

