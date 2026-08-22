# A Comparative Evaluation of Embedding Models for Retrieval and Clustering of Brazilian Legislative Amendments

[🇧🇷 Português](README.md)

## Environment Setup

* Install dependencies:

    ```
    uv sync
    ```

## Data Collection

* Collect amendment metadata and PDFs

    * Script:

        ```
        uv run python scripts/retrieve_amendments.py
        ```

    * Outputs:

        * [MPV 612/2013 metadata](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/MPV_612_2013_metadata.parquet)
        * [PEC 6/2019 metadata](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PEC_6_2019_metadata.parquet)
        * [PLP 68/2024 metadata](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PLP_68_2024_metadata.parquet)

* Extract raw text from PDFs

    * Script:

        ```
        uv run python scripts/extract_text.py
        ```

    * Outputs:

        * [MPV 612/2013 texts](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/tree/main/data/txts/MPV_612_2013/extracted_txts)
        * [PEC 6/2019 texts](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/tree/main/data/txts/PEC_6_2019)
        * [PLP 68/2024 texts](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/tree/main/data/txts/PLP_68_2024)

* Generate datasets with amendment texts

    * Script:

        ```
        uv run python scripts/generate_dataset.py
        ```

    * Outputs:

        * [MPV 612/2013 dataset with raw text](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/MPV_612_2013_textos_emendas.parquet)
        * [PEC 6/2019 dataset with raw text](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PEC_6_2019_textos_emendas.parquet)
        * [PLP 68/2024 dataset with raw text](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PLP_68_2024_textos_emendas.parquet)

## Data Preprocessing and Consolidation

### Texts

#### MPV 612/2013

* Generate images of the amendment PDF pages:

    * Script:

        ```
        uv run python scripts/pdfs_pages_to_images.py
        ```

    * [Output JSON](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/MPV_612_2013_label_studio.json)

* Annotate regions of interest using [Label Studio](https://labelstud.io/):

    * [JSON with image paths (uploaded to Label Studio)](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/MPV_612_2013_label_studio.json)

    * [JSON with manually generated annotations](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/roi_emendas_mpv_612_label_studio.json)

* Extract text from the regions of interest:

    ```
    uv run python scripts/extract_text_from_images.py
    ```

* [Notebook for generating the dataset with extracted and preprocessed texts](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20MPV%20612.ipynb)

#### PLP 68/2024 and PEC 6/2019

* [PEC 6/2019 - Notebook for generating the dataset with extracted and preprocessed texts](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20PEC%206.ipynb)

* [PLP 68/2024 - Notebook for generating the dataset with extracted and preprocessed texts](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20PLP%2068.ipynb)

### Topics

* [Original documents containing amendment topics](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/tree/main/data/quadros_emendas)

* [Preprocessing and generation of the dataset with topics](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Extra%C3%A7%C3%A3o%20dos%20temas.ipynb)

* Extracted topics:

    * [MPV 612/2013 topics](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/MPV_612_2013.parquet)

    * [PEC 6/2019 topics](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/PEC_6_2019.parquet)

    * [PLP 68/2024 topics](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/PLP_68_2024.parquet)

    * [PLP 68/2024 topic hierarchy](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/PLP_68_hierarquia.csv)

### Final Dataset

* Final dataset used for embedding generation and the *retrieval* and *clustering* tasks, containing:

    * Raw text extracted from amendments (Metadata + Changes + Justification)

    * Preprocessed amendment texts

        * Text without Metadata (Changes + Justification)
        * Text without Metadata and Justification

    * Amendment topic

* [Notebook for generating the final dataset](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Dataset-Final.ipynb)

## Selection of Open-Source Embedding Models

* [Ranking construction (Clustering + Retrieval)](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Open-Source-Embeddings-Models-Selection-MMTEB.ipynb)

## Embedding Generation

* [Open-Source Models](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Open-Source-Embeddings.ipynb)

* [Proprietary Models](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Closed-Source-Embeddings.ipynb)