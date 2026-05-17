from tasks import TextExtractor

pdf_folders = [ "data/pdfs/PEC_6_2019"]
txts_folders = [ "data/txts/PEC_6_2019"]

for pdf_folder, txts_folder in zip(pdf_folders, txts_folders):
    extractor = TextExtractor(pdf_folder)
    extractor.extract(txts_folder)