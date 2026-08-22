from PIL import Image

imgs = [
    Image.open("data/images/paper/MPV_612_EMENDA_148.png"),
    Image.open("data/images/paper/PEC_6_EMENDA_57.png"),
    Image.open("data/images/paper/PLP_69_EMENDA_917.png")
]

altura = max(img.height for img in imgs)
largura = sum(img.width for img in imgs)

resultado = Image.new("RGB", (largura, altura), "white")

x = 0
for img in imgs:
    resultado.paste(img, (x, 0))
    x += img.width

resultado.save("data/images/paper/comparacao_emendas.png")