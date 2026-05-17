from tasks import DatasetGenerator


dataset_generator = DatasetGenerator()

input_folders = ["data/txts/PEC_6_2019"]

for input_folder in input_folders:
    dataset_generator.txts_to_parquet(input_folder, f"data/datasets/{input_folder.split('/')[-1]}_textos_emendas.parquet")