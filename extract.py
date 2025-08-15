from PIL import Image
import pytesseract
import re
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pasta_imagens = r"C:\Users\dyhego.silva\Documents\Python\extractnumbers\img"

arquivos = [f for f in os.listdir(pasta_imagens) if f.lower().endswith(".jpg")]

for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagem = Image.open(caminho)

    largura, altura = imagem.size
    crop_box = (0, 0, largura, 900)
    imagem_cortada = imagem.crop(crop_box)

    texto = pytesseract.image_to_string(imagem_cortada, lang="eng")

    match = re.search(r"N[°o]\s+(\d{6})", texto)
    
    if match:
        print(f"{arquivo}: Número encontrado = {match.group(1)}")
    else:
        print(f"{arquivo}: Número não encontrado")

