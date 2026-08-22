from pathlib import Path
import fitz  # PyMuPDF

def pdf_tem_texto(pdf_path):
    try:
        doc = fitz.open(pdf_path)

        for pagina in doc:
            texto = pagina.get_text().strip()
            if len(texto) >= 100:
                doc.close()
                return True

        doc.close()
        print(pdf_path)
        print(texto)
        return False

    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
        return False


pastas = [
    Path("data/pdfs/PEC_6_2019"),
]

for pasta in pastas:
    pdfs = list(pasta.glob("*.pdf"))

    total = len(pdfs)
    com_texto = 0
    sem_texto = 0

    for pdf in pdfs:
        if pdf_tem_texto(pdf):
            com_texto += 1
        else:
            sem_texto += 1

    print(f"\nPasta: {pasta}")
    print(f"Total PDFs: {total}")
    print(f"Com camada de texto: {com_texto}")
    print(f"Sem camada de texto: {sem_texto}")
    print(f"% com texto: {100 * com_texto / total:.2f}%")