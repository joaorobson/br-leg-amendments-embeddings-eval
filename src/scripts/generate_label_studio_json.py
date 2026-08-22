import os
import json

BASE_DIR = "data/images/MPV_612_2013"
OUTPUT_JSON_PATH = "data/json/MPV_612_2013_label_studio.json"

URL_PREFIX = "/data/local-files/?d=images/MPV_612_2013/"
MPV_NOME = "MPV_612_2013"

tasks = []

for emenda_folder in sorted(os.listdir(BASE_DIR)):
    emenda_path = os.path.join(BASE_DIR, emenda_folder)

    if not os.path.isdir(emenda_path):
        continue

    imagens = sorted([
        arquivo for arquivo in os.listdir(emenda_path)
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    total_paginas = len(imagens)

    for idx, arquivo in enumerate(imagens):
        url_formatada = f"{URL_PREFIX}{emenda_folder}/{arquivo}"

        task = {
            "data": {
                "image": url_formatada,

                # referência global
                "mpv_nome": MPV_NOME,

                # agrupamento lógico
                "emenda_nome": emenda_folder,

                # rastreabilidade
                "pagina_idx": idx,
                "pagina_nome": arquivo,
                "total_paginas_emenda": total_paginas,

                # id único reconstruível
                "doc_id": f"{MPV_NOME}__{emenda_folder}",
                "page_id": f"{MPV_NOME}__{emenda_folder}__p{idx:03d}"
            }
        }

        tasks.append(task)

with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

print(f"Sucesso! {len(tasks)} tasks geradas.")
print(f"Arquivo salvo em: {OUTPUT_JSON_PATH}")