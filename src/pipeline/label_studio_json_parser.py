import json
import os
from dataclasses import dataclass
from typing import List

from PIL import Image
import pytesseract
from models import Region, PageAnnotation

class LabelStudioJsonParser:

    def __init__(self, json_path, document_root="data"):
        self.json_path = json_path
        self.document_root = document_root

    def _ls_to_local_path(self, ls_path):
        """
        Converte:
        /data/local-files/?d=images/...
        para:
        data/images/...
        """
        prefix = "/data/local-files/?d="
        relative = ls_path.replace(prefix, "")
        return os.path.join(self.document_root, relative)

    def _convert_bbox(self, bbox, img_w, img_h):
        """
        Label Studio salva bbox em %
        Converte para pixels
        """
        return Region(
            label=bbox["rectanglelabels"][0],
            x=int((bbox["x"] / 100) * img_w),
            y=int((bbox["y"] / 100) * img_h),
            width=int((bbox["width"] / 100) * img_w),
            height=int((bbox["height"] / 100) * img_h)
        )

    def parse(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        pages = []

        for task in tasks:

            if not task.get("annotations"):
                continue

            data = task["data"]

            image_path = self._ls_to_local_path(data["image"])

            annotation = task["annotations"][0]

            page_regions = []

            for result in annotation["result"]:

                if result["type"] != "rectanglelabels":
                    continue

                region = self._convert_bbox(
                    result["value"],
                    result["original_width"],
                    result["original_height"]
                )

                page_regions.append(region)

            pages.append(
                PageAnnotation(
                    image_path=image_path,
                    mpv_nome=data["mpv_nome"],
                    emenda_nome=data["emenda_nome"],
                    pagina_idx=data["pagina_idx"],
                    regions=page_regions
                )
            )

        return pages