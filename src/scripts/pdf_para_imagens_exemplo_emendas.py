from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image, ImageOps

# PDFs
pdfs = [
    "data/pdfs/MPV_612_2013/EMENDA_148_-_MPV_612_2013.pdf",
    "data/pdfs/PEC_6_2019/EMENDA_212_-_PEC_6_2019.pdf",
    "data/pdfs/PLP_68_2024/EMENDA_917-U_-_PLP_68_2024.pdf",
]

# Crop individual para cada documento
# (left%, top%, right%, bottom%)
crops = [
    (0.12, 0.03, 0.95, 1.00),  # MPV: remove 6% da esquerda
    (0.1, 0.02, 1.00, 1.00),  # PEC: remove 8% da esquerda
    (0.00, 0.02, 1.00, 1.00),  # PLP: sem corte
]

zoom = 3.0
mat = fitz.Matrix(zoom, zoom)

imagens = []

for pdf_path, crop in zip(pdfs, crops):

    doc = fitz.open(pdf_path)
    page = doc[0]

    left, top, right, bottom = crop

    crop_rect = fitz.Rect(
        page.rect.width * left,
        page.rect.height * top,
        page.rect.width * right,
        page.rect.height * bottom,
    )

    pix = page.get_pixmap(
        matrix=mat,
        clip=crop_rect,
        alpha=False,
    )

    img = Image.frombytes(
        "RGB",
        [pix.width, pix.height],
        pix.samples,
    )

    imagens.append(img)

    doc.close()

# Altura comum para todos
altura_final = 1200

imagens_redim = []

for img in imagens:

    nova_largura = int(
        img.width * altura_final / img.height
    )

    img = img.resize(
        (nova_largura, altura_final),
        Image.LANCZOS,
    )

    # margem branca externa
    img = ImageOps.expand(
        img,
        border=12,
        fill="white",
    )

    # borda preta fina
    img = ImageOps.expand(
        img,
        border=1,
        fill="black",
    )

    imagens_redim.append(img)

espaco = 30

largura_total = (
    sum(img.width for img in imagens_redim)
    + espaco * (len(imagens_redim) - 1)
)

altura_canvas = max(img.height for img in imagens_redim)

canvas = Image.new(
    "RGB",
    (largura_total, altura_canvas),
    "white",
)

x = 0

for img in imagens_redim:

    y = (altura_canvas - img.height) // 2

    canvas.paste(img, (x, y))

    x += img.width + espaco

saida = "comparacao_emendas_2.png"

canvas.save(
    saida,
    dpi=(300, 300),
)

print(f"Imagem salva em: {saida}")