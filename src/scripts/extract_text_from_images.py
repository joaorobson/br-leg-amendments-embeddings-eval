from tasks import TextExtractor

extractor = TextExtractor()

extractor.extract_from_annotations(
    labelstudio_json="data/json/roi_emendas_mpv_612_label_studio.json",
    storage_path="data/txts/MPV_612_2013/txts_from_label_studio_annotations"
)