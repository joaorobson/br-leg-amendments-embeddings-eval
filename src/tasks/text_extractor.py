import fitz
import os
import pytesseract

from PIL import Image

class TextExtractor:
    def __init__(self, pdfs_path, lang="por"):
        self.pdfs_path = pdfs_path
        self.lang = lang

    @staticmethod
    def store_txt(content, folder, filename):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder '{folder}' created.")
        else:
            print(f"Folder '{folder}' already exists.")

        with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
            f.write(content)

    def extract_page_with_ocr(self, page, zoom=3):
        """
        Converte página em imagem e aplica OCR.
        """
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        text = pytesseract.image_to_string(img, lang=self.lang)

        return text

    def extract(self, storage_path):

        for filename in os.listdir(self.pdfs_path):

            if not filename.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(self.pdfs_path, filename)

            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(storage_path, txt_filename)

            print(f"\nProcessing: {filename}")

            doc = fitz.open(pdf_path)

            # =====================================================
            # VERIFICA APENAS A PRIMEIRA PÁGINA
            # =====================================================
            first_page_text = doc[0].get_text().strip()

            use_ocr = len(first_page_text) < 100

            if use_ocr:
                print("PDF escaneado -> usando OCR em todas as páginas")
            else:
                print("PDF com camada de texto")

            # =====================================================
            # EXTRAÇÃO
            # =====================================================
            all_text = ""

            for page_num, page in enumerate(doc):

                if use_ocr:
                    text = self.extract_page_with_ocr(page)
                else:
                    text = page.get_text()

                all_text += text + "\n"

            # =====================================================
            # SALVA TXT
            # =====================================================
            TextExtractor.store_txt(
                all_text,
                storage_path,
                txt_filename
            )

            print(f"Saved: {txt_path}")

