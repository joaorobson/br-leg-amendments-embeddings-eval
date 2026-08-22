from data_collector.pipeline import AmendmenstsRetriever

# Código MATE
propostitions_codes = [
    '164914',  # PLP 68/2024
    '137999',   # PEC 6/2019
    '112122'    # MPV 612/2013
]

propositions_names = {
    '164914': 'PLP_68_2024',
    '137999': 'PEC_6_2019',
    '112122': 'MPV_612_2013'
}

amendments_to_consider = {
    '164914': [],
    '137999': set(list(range(1, 270))),
    '112122': set(list(range(1, 221)))
}

PDFS_PATH = "data/pdfs"
METADATA_PATH = "data/datasets"

if __name__ == "__main__":
    for code, name in propositions_names.items():
        print(code, name)
    retriever = AmendmenstsRetriever(code, name)
    retriever.get_amendments_list(amendments_to_consider[code])
    retriever.store_metadata(f"{METADATA_PATH}/{name}_metadata.parquet")
    retriever.get_amendments_pdfs(PDFS_PATH)