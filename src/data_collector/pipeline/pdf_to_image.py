import fitz  # PyMuPDF
import os

def convert_pdfs_in_folder(input_folder, output_folder, zoom=4):
    """
    Converte todos os PDFs de uma pasta em imagens PNG de alta qualidade.
    Cada PDF vira uma subpasta com suas páginas.
    """

    os.makedirs(output_folder, exist_ok=True)

    pdf_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(".pdf")
    ]

    mat = fitz.Matrix(zoom, zoom)

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)

        # nome base sem extensão
        pdf_name = os.path.splitext(pdf_file)[0]

        # pasta de saída por PDF
        pdf_out_dir = os.path.join(output_folder, pdf_name)
        os.makedirs(pdf_out_dir, exist_ok=True)

        doc = fitz.open(pdf_path)

        for page_index, page in enumerate(doc):
            pix = page.get_pixmap(matrix=mat, alpha=False)

            out_path = os.path.join(
                pdf_out_dir,
                f"page_{page_index:03d}.png"
            )

            pix.save(out_path)

        print(f"[OK] {pdf_file} -> {len(doc)} páginas")

    print("\nConcluído.")