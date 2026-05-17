import fitz  # PyMuPDF

def imprimir_blocos(caminho_pdf):
    doc = fitz.open(caminho_pdf)

    for page_num, page in enumerate(doc):
        print("\n" + "="*80)
        print(f"PÁGINA {page_num + 1}")
        print("="*80)

        blocks = page.get_text("dict")["blocks"]

        for i, block in enumerate(blocks):
            print(f"\n--- BLOCO {i} ---")
            #print(f"Tipo: {block['type']}")  # 0 = texto, 1 = imagem
            #print(f"BBox: {block['bbox']}")

            if block["type"] == 0:  # bloco de texto
                for j, line in enumerate(block["lines"]):
                    x0, y0, x1, y1 = line["bbox"]
                    #print(f"\n  Linha {j} | bbox: {line['bbox']}")

                    for k, span in enumerate(line["spans"]):
                        #print(f"    Span {k}")
                        print(f"      Texto: {repr(span['text'])}")
                        """ print(f"      Fonte: {span['font']}")
                        print(f"      Tamanho: {span['size']}")
                        print(f"      Flags: {span['flags']}")
                        print(f"      Cor: {span['color']}")
                        print(f"      Origem: {span['origin']}") """

            elif block["type"] == 1:
                print("  (Bloco de imagem)")

    doc.close()


# Execução
for i in range(1, 100):
    imprimir_blocos(f"data/pdfs/PLP_68_2024/EMENDA_{i}-U_-_PLP_68_2024.pdf")
