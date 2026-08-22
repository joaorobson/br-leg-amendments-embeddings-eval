import fitz
import os
import json
import pytesseract

from PIL import Image
from data_collector.models import Region


class TextExtractor:
    def __init__(self, pdfs_path=None, lang="por", document_root="data"):
        self.pdfs_path = pdfs_path
        self.lang = lang
        self.document_root = document_root

        print(f"[INIT] TextExtractor inicializado")
        print(f"[INIT] pdfs_path={self.pdfs_path}")
        print(f"[INIT] lang={self.lang}")
        print(f"[INIT] document_root={self.document_root}")

    @staticmethod
    def store_txt(content, folder, filename):

        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[STORE] Pasta criada: {folder}")

        filepath = os.path.join(folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[STORE] Arquivo salvo: {filepath}")

    def _ls_to_local_path(self, ls_path):

        prefix = "/data/local-files/?d="
        relative = ls_path.replace(prefix, "")
        local_path = os.path.join(self.document_root, relative)

        print(f"[PATH] LS -> Local")
        print(f"       origem: {ls_path}")
        print(f"       local : {local_path}")

        return local_path

    def extract_page_with_ocr(self, page, zoom=3):

        print(f"[OCR] Renderizando página com zoom={zoom}")

        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        print(f"[OCR] Aplicando pytesseract...")

        text = pytesseract.image_to_string(img, lang=self.lang)

        print(f"[OCR] Extração concluída ({len(text)} chars)")

        return text

    def extract(self, storage_path):

        print(f"[PDF] Iniciando processamento de PDFs")

        for filename in os.listdir(self.pdfs_path):

            if not filename.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(self.pdfs_path, filename)

            print(f"\n[PDF] Processando: {filename}")

            doc = fitz.open(pdf_path)

            print(f"[PDF] Total páginas: {len(doc)}")

            first_page_text = doc[0].get_text().strip()

            use_ocr = len(first_page_text) < 100

            print(f"[PDF] OCR necessário? {use_ocr}")

            all_text = ""

            for page_num, page in enumerate(doc):

                print(f"[PDF] Página {page_num}")

                if use_ocr:
                    text = self.extract_page_with_ocr(page)
                else:
                    text = page.get_text()
                    print(f"[PDF] Texto nativo extraído ({len(text)} chars)")

                all_text += text + "\n"

            txt_filename = os.path.splitext(filename)[0] + ".txt"

            self.store_txt(
                all_text,
                storage_path,
                txt_filename
            )

    def _convert_bbox(self, bbox, img_w, img_h):

        region = Region(
            label=bbox["rectanglelabels"][0],
            x=int((bbox["x"] / 100) * img_w),
            y=int((bbox["y"] / 100) * img_h),
            width=int((bbox["width"] / 100) * img_w),
            height=int((bbox["height"] / 100) * img_h)
        )

        print(
            f"[BBOX] {region.label} "
            f"x={region.x} y={region.y} "
            f"w={region.width} h={region.height}"
        )

        return region

    def extract_region_text(self, image, region):

        print(f"[REGION] Recortando região {region.label}")

        crop = image.crop((
            region.x,
            region.y,
            region.x + region.width,
            region.y + region.height
        ))

        print(f"[REGION] OCR em {region.label}...")

        text = pytesseract.image_to_string(
            crop,
            lang=self.lang
        ).strip()

        print(f"[REGION] OCR concluído ({len(text)} chars)")

        return text

    def extract_from_annotations(self, labelstudio_json, storage_path):

        print(f"[LS] Lendo export: {labelstudio_json}")

        with open(labelstudio_json, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        print(f"[LS] Total tasks: {len(tasks)}")

        grouped_output = {}

        for task_idx, task in enumerate(tasks):

            print(f"\n[LS] Task {task_idx+1}/{len(tasks)}")

            if not task.get("annotations"):
                print("[LS] Sem anotações -> ignorando")
                continue

            data = task["data"]

            doc_id = data["doc_id"]

            print(f"[LS] Documento: {doc_id}")
            print(f"[LS] Página: {data['pagina_idx']}")

            if doc_id not in grouped_output:
                grouped_output[doc_id] = {
                    "mpv_nome": data["mpv_nome"],
                    "emenda_nome": data["emenda_nome"],
                    "pages": {}
                }

            image_path = self._ls_to_local_path(data["image"])

            print(f"[IMG] Abrindo: {image_path}")

            image = Image.open(image_path)

            annotation = task["annotations"][0]

            print(
                f"[LS] Regiões encontradas: "
                f"{len(annotation['result'])}"
            )

            page_result = {}

            for region_idx, result in enumerate(annotation["result"]):

                if result["type"] != "rectanglelabels":
                    continue

                region = self._convert_bbox(
                    result["value"],
                    result["original_width"],
                    result["original_height"]
                )

                text = self.extract_region_text(
                    image,
                    region
                )

                print(
                    f"[LS] Região {region_idx+1} "
                    f"label={region.label}"
                )

                # ==================================================
                # CORREÇÃO
                # ==================================================

                page_result.setdefault(region.label, [])

                page_result[region.label].append({
                    "y": region.y,
                    "text": text
                })

            grouped_output[doc_id]["pages"][
                data["pagina_idx"]
            ] = page_result

        print("\n[FINAL] Salvando resultados")

        for doc_id, content in grouped_output.items():

            print(
                f"[DOC] Processando "
                f"{content['emenda_nome']}"
            )

            final_text = []

            for page_idx in sorted(content["pages"]):

                page = content["pages"][page_idx]

                final_text.append(
                    f"=== PÁGINA {page_idx} ===\n"
                )

                # =====================================
                # EMENDA
                # =====================================

                if "Emenda" in page:

                    final_text.append("[EMENDA]\n")

                    emendas = sorted(
                        page["Emenda"],
                        key=lambda x: x["y"]
                    )

                    print(
                        f"[DOC] Página {page_idx}: "
                        f"{len(emendas)} blocos Emenda"
                    )

                    for bloco in emendas:
                        final_text.append(
                            bloco["text"].strip()
                        )
                        final_text.append("\n\n")

                # =====================================
                # JUSTIFICATIVA
                # =====================================

                if "Justificativa" in page:

                    final_text.append(
                        "[JUSTIFICATIVA]\n"
                    )

                    justificativas = sorted(
                        page["Justificativa"],
                        key=lambda x: x["y"]
                    )

                    print(
                        f"[DOC] Página {page_idx}: "
                        f"{len(justificativas)} blocos Justificativa"
                    )

                    for bloco in justificativas:
                        final_text.append(
                            bloco["text"].strip()
                        )
                        final_text.append("\n\n")

            filename = (
                f"{content['emenda_nome']}.txt"
            )

            self.store_txt(
                "".join(final_text),
                storage_path,
                filename
            )

        print("\n[DONE] Processamento concluído")