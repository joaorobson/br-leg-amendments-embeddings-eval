from tasks import DatasetGenerator


dataset_generator = DatasetGenerator()

input_folders = ["data/txts/PLP_68_2024", "data/txts/PEC_6_2019", "data/txts/MPV_612_2013/extracted_txts"]

for input_folder in input_folders:
    dataset_generator.txts_to_parquet(input_folder, f"data/datasets/{input_folder.split('/')[2]}_textos_emendas.parquet")