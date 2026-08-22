from tasks import LabelStudioJsonParser

parser = LabelStudioJsonParser(
    json_path="data/json/roi_emendas_mpv_612_label_studio.json",
    document_root="data/images/MPV_612_2013"
)

pages = parser.parse()
print(len(pages))