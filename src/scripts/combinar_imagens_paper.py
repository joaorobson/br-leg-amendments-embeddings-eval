from PIL import Image

imgs = [
    Image.open("data/images/Paper/MPV_612_EMENDA_148.png"),
    Image.open("data/images/Paper/PEC_6_EMENDA_57.png"),
    Image.open("data/images/Paper/PLP_69_EMENDA_917.png")
]

altura = max(img.height for img in imgs)
largura = sum(img.width for img in imgs)

resultado = Image.new("RGB", (largura, altura), "white")

x = 0
for img in imgs:
    resultado.paste(img, (x, 0))
    x += img.width

resultado.save("comparacao.png")