from tasks import TextExtractor

pdf_folders = [ "data/pdfs/PLP_68_2024", "data/pdfs/PEC_6_2019", "data/pdfs/MPV_612_2013" ]
txts_folders = [ "data/txts/PLP_68_2024", "data/txts/PEC_6_2019", "data/txts/MPV_612_2013/extracted_txts" ]

for pdf_folder, txts_folder in zip(pdf_folders, txts_folders):
    extractor = TextExtractor(pdf_folder)
    extractor.extract(txts_folder)