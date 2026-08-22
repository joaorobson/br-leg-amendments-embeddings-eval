# A Comparative Evaluation of Embedding Models for Retrieval and Clustering of Brazilian Legislative Amendments

[🇺🇸 English](README.en-US.md)

## Configuração do ambiente

* Instalação das dependências:
```
uv sync
```

## Coleta dos dados

* Coleta de metadados e PDFs
    * Script:
        ```
        uv run python scripts/retrieve_amendments.py
        ```
    * Saídas:
        * [Metadados da MPV 612/2013](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/MPV_612_2013_metadata.parquet)
        * [Metadados da PEC 6/2019](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PEC_6_2019_metadata.parquet)
        * [Metadados do PLP 68/2024](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PLP_68_2024_metadata.parquet)
* Extração do texto bruto dos PDFs
    * Script:
        ```
        uv run python scripts/extract_text.py
        ```
    * Saída:
        * [Textos da MPV 612/2013](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/tree/main/data/txts/MPV_612_2013/extracted_txts)
        * [Textos da PEC 6/2019](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/txts/PEC_6_2019)
        * [Textos do PLP 68/2024](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/txts/PLP_68_2024)
* Gerar datasets com textos
    * Script:
        ```
        uv run python scripts/generate_dataset.py
        ```
    * Saídas:
        * [Dataset com texto bruto da MPV 612/2013](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/MPV_612_2013_textos_emendas.parquet)
        * [Dataset com texto bruto da PEC 6/2019](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PEC_6_2019_textos_emendas.parquet)
        * [Dataset com texto bruto do PLP 68/2024](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/datasets/PLP_68_2024_textos_emendas.parquet)

## Pré-processamento e consolidação dos dados

### Textos
#### MPV 612/2013

* Gerar imagens das páginas dos PDFs das emendas:
    * Script:
        ```
        uv run python scripts/pdfs_pages_to_images.py
        ```
    * [JSON de saída](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/MPV_612_2013_label_studio.json)
* Anotar das regiões de interesse no [Label Studio](https://labelstud.io/):
    * [JSON com caminhos das imagens (upload no Label Studio)](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/MPV_612_2013_label_studio.json)
    * [JSON com anotações geradas manualmente](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/roi_emendas_mpv_612_label_studio.json)
* Extrair texto das regiões de interesse:
```
uv run python scripts/extract_text_from_images.py
```
* [Geração do dataset com textos extraídos e pré-processados](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20MPV%20612.ipynb)

#### PLP 68/2024 e PEC 6/2019

* [PEC 6/2019 - Geração do dataset com textos extraídos e pré-processados](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20PEC%206.ipynb)
* [PLP 68/2024 - Geração do dataset com textos extraídos e pré-processados](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20PLP%2068.ipynb)


### Temas

* [Documentos originais com temas das emendas](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/tree/main/data/quadros_emendas)
* [Pré-processamento e geração do dataset com temas](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Extra%C3%A7%C3%A3o%20dos%20temas.ipynb)
* Temas extraídos:
    * [Temas da MPV 612/2013](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/MPV_612_2013.parquet)
    * [Temas da PEC 6/2019](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/PEC_6_2019.parquet)
    * [Temas do PLP 68/2024](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/PLP_68_2024.parquet)
    * [Hierarquia de temas do PLP 68/2024](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/temas/PLP_68_hierarquia.csv)


### Dataset final

* Dataset final utilizado na geração dos embeddings e realização das tarefas de *retrieval* e *clustering*, contendo:
    * Textos brutos extraídos das emendas (Metadados + Mudanças + Justificativa)
    * Textos pré-processados das emendas
        * Texto sem Metadados (Mudanças + Justificativa)
        * Texto sem Metadados e Justificativa
    * Tema da emenda
* [Notebook com geração do dataset final](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Dataset-Final.ipynb)

## Escolha dos modelos de embedding open-source

* [Montagem do ranking (Clustering + Retrieval)](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Open-Source-Embeddings-Models-Selection-MMTEB.ipynb)


## Geração dos embeddings

* [Open Source](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Open-Source-Embeddings.ipynb)
* [Proprietários](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Closed-Source-Embeddings.ipynb)