import os
import pandas as pd
import re

class DatasetGenerator:
    @staticmethod
    def extract_project_code(filename):
        match = re.search(r'(PL|PLP|PEC|PLC|MP|PDL|PDC|PRC|MPV)_\d+_\d{4}', filename)
        return match.group(0) if match else None
    
    def txts_to_parquet(self, input_folder, output_parquet_path):
        records = []

        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".txt"):
                    txt_path = os.path.join(root, file)
                    try:
                        with open(txt_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        subfolder = os.path.relpath(root, input_folder)

                        records.append({
                            "num_emenda": int(re.search(r"EMENDA_(\d+)", file).group(1)),
                            "materia": DatasetGenerator.extract_project_code(file),
                            #"materia": subfolder,
                            "nome_arquivo": file,
                            "texto": content
                        })
                    except Exception as e:
                        print(f"Error reading {txt_path}: {e}")

        df = pd.DataFrame(records)
        df.to_parquet(output_parquet_path, index=False)
        print(f"Saved {len(df)} rows to {output_parquet_path}")

