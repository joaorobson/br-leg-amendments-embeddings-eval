# A Comparative Evaluation of Embedding Models for Retrieval and Clustering of Brazilian Legislative Amendments

## Configuração do ambiente

* Instalação das dependências:
```
uv sync
```

## Coleta dos dados

* Coleta de metadados e PDFs
```
uv run python scripts/retrieve_amendments.py
```
* Extração do texto bruto dos PDFs
```
uv run python scripts/extract_text.py
```
* Gerar dataset com textos
```
uv run python scripts/generate_dataset.py
```

## Pré-processamento e consolidação dos dados

### Textos
#### MPV 612/2013

* Gerar imagens das páginas dos PDFs das emendas:
    * Script:
        ```
        uv run python scripts/pdfs_pages_to_images.py
        ```
    * JSON de saída: data/json/MPV_612_2013_label_studio.json
* Anotar das regiões de interesse no [Label Studio](https://labelstud.io/):
    * [JSON com caminhos das imagens (upload no Label Studio)](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/MPV_612_2013_label_studio.json)
    * [JSON com anotações geradas manualmente](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/data/json/roi_emendas_mpv_612_label_studio.json)
* Extrair texto das regiões de interesse:
```
uv run python scripts/extract_text_from_images.py
```
* [Gerar dataset com textos extraídos e pré-processados](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20MPV%20612.ipynb)

#### PLP 68/2024 e PEC 6/2019

[PEC 6/2019](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20PEC%206.ipynb)
[PLP 68/2024](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Pr%C3%A9-processamento%20-%20PLP%2068.ipynb)


### Temas

* [Documentos originais com temas das emendas](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/tree/main/data/quadros_emendas)
* [Pré-processamento e geração do dataset](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Extra%C3%A7%C3%A3o%20dos%20temas.ipynb)

### Dataset final

[Geração do dataset final](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/preprocessing/Dataset-Final.ipynb)

## Escolha dos modelos de embedding open-source

* [Montagem do ranking (Clustering + Retrieval)](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Open-Source-Embeddings-Models-Selection-MMTEB.ipynb)


## Geração dos embeddings

* [Open Source](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Open-Source-Embeddings.ipynb)
* [Proprietários](https://github.com/joaorobson/br-leg-amendments-embeddings-eval/blob/main/notebooks/embeddings/Closed-Source-Embeddings.ipynb)