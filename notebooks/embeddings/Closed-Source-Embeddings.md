```python
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import tiktoken
import numpy as np
from tqdm import tqdm
from google.genai import types
import os
```


```python
df = pd.read_parquet("../../data/datasets/embeddings.parquet")
```


```python
df.columns
```




    Index(['num_emenda', 'materia', 'texto', 'texto_preprocessado',
           'texto_preprocessado_sem_justificativa', 'tema', 'tema_macro',
           'tema_nivel_2', 'embedding__codefuse_ai__F2LLM_v2_14B__texto',
           'embedding__codefuse_ai__F2LLM_v2_14B__texto_preprocessado',
           'embedding__codefuse_ai__F2LLM_v2_14B__texto_preprocessado_sem_justificativa',
           'embedding__Octen__Octen_Embedding_8B__texto',
           'embedding__Octen__Octen_Embedding_8B__texto_preprocessado',
           'embedding__Octen__Octen_Embedding_8B__texto_preprocessado_sem_justificativa',
           'embedding__Qwen__Qwen3_Embedding_8B__texto',
           'embedding__Qwen__Qwen3_Embedding_8B__texto_preprocessado',
           'embedding__Qwen__Qwen3_Embedding_8B__texto_preprocessado_sem_justificativa',
           'embedding__nvidia__llama_embed_nemotron_8b__texto',
           'embedding__nvidia__llama_embed_nemotron_8b__texto_preprocessado',
           'embedding__nvidia__llama_embed_nemotron_8b__texto_preprocessado_sem_justificativa',
           'embedding__jinaai__jina_embeddings_v5_text_small__clustering__texto',
           'embedding__jinaai__jina_embeddings_v5_text_small__clustering__texto_preprocessado',
           'embedding__jinaai__jina_embeddings_v5_text_small__clustering__texto_preprocessado_sem_justificativa',
           'embedding__jinaai__jina_embeddings_v5_text_small__text_matching__texto',
           'embedding__jinaai__jina_embeddings_v5_text_small__text_matching__texto_preprocessado',
           'embedding__jinaai__jina_embeddings_v5_text_small__text_matching__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__trunc128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__trunc128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__trunc128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__meanpool128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__meanpool128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__meanpool128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__trunc128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__trunc128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__trunc128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__meanpool128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__meanpool128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__meanpool128__texto_preprocessado_sem_justificativa',
           'embedding__joaorobson__harrier_oss_v1_27b__texto',
           'embedding__joaorobson__harrier_oss_v1_27b__texto_preprocessado',
           'embedding__joaorobson__harrier_oss_v1_27b__texto_preprocessado_sem_justificativa',
           'embedding__joaorobson__KaLM_Embedding_Gemma3_12B_2511__texto',
           'embedding__joaorobson__KaLM_Embedding_Gemma3_12B_2511__texto_preprocessado',
           'embedding__joaorobson__KaLM_Embedding_Gemma3_12B_2511__texto_preprocessado_sem_justificativa',
           'embedding__openai__text_embedding_3_large__trunc8192__texto',
           'embedding__openai__text_embedding_3_large__trunc8192__texto_preprocessado',
           'embedding__openai__text_embedding_3_large__trunc8192__texto_preprocessado_sem_justificativa',
           'embedding__openai__text_embedding_3_large__meanpool8192__texto',
           'embedding__openai__text_embedding_3_large__meanpool8192__texto_preprocessado',
           'embedding__openai__text_embedding_3_large__meanpool8192__texto_preprocessado_sem_justificativa',
           'gemini_embedding_2_chunk_boundaries__texto',
           'gemini_embedding_2_chunk_boundaries__texto_preprocessado',
           'gemini_embedding_2_chunk_boundaries__texto_preprocessado_sem_justificativa',
           'embedding__google__gemini_embedding_2__trunc8192__texto',
           'embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado',
           'embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado_sem_justificativa',
           'embedding__google__gemini_embedding_2__meanpool8192__texto',
           'embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado',
           'embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder__trunc128__texto',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder__trunc128__texto_preprocessado',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder__trunc128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder__meanpool128__texto',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder__meanpool128__texto_preprocessado',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder__meanpool128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder_ir__trunc128__texto',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder_ir__trunc128__texto_preprocessado',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder_ir__trunc128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder_ir__meanpool128__texto',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder_ir__meanpool128__texto_preprocessado',
           'embedding__PORTULAN__serafim_335m_portuguese_pt_sentence_encoder_ir__meanpool128__texto_preprocessado_sem_justificativa',
           'embedding__josedossantos__bertimbau_tuned__trunc512__texto',
           'embedding__josedossantos__bertimbau_tuned__trunc512__texto_preprocessado',
           'embedding__josedossantos__bertimbau_tuned__trunc512__texto_preprocessado_sem_justificativa',
           'embedding__josedossantos__bertimbau_tuned__meanpool512__texto',
           'embedding__josedossantos__bertimbau_tuned__meanpool512__texto_preprocessado',
           'embedding__josedossantos__bertimbau_tuned__meanpool512__texto_preprocessado_sem_justificativa',
           'embedding__ICT_TIME_and_Querit__ICT_TIME_and_Querit_embedding_v1__texto',
           'embedding__ICT_TIME_and_Querit__ICT_TIME_and_Querit_embedding_v1__texto_preprocessado',
           'embedding__ICT_TIME_and_Querit__ICT_TIME_and_Querit_embedding_v1__texto_preprocessado_sem_justificativa'],
          dtype='object')



## OpenAI


```python
enc = tiktoken.encoding_for_model("text-embedding-3-large")
```


```python
import tiktoken
import pandas as pd

# -----------------------------
# Configuração
# -----------------------------
model = "text-embedding-3-large"
enc = tiktoken.encoding_for_model(model)

# As 3 colunas de texto originais
colunas_alvo = [
    "texto", 
    "texto_preprocessado", 
    "texto_preprocessado_sem_justificativa"
]

# -----------------------------
# Função de Contagem
# -----------------------------
def contar_tokens_coluna(df, col_name):
    if col_name not in df.columns:
        print(f"⚠️ Coluna '{col_name}' não encontrada no DataFrame.")
        return 0
        
    # Transforma em string, trata nulos e conta os tokens de cada linha
    total_tokens = df[col_name].fillna("").astype(str).apply(lambda x: len(enc.encode(x))).sum()
    return total_tokens

# -----------------------------
# Execução e Relatório
# -----------------------------
grand_total = 0
relatorio = []

print("📊 Contando tokens...\n")

for col in colunas_alvo:
    total_col = contar_tokens_coluna(df, col)
    grand_total += total_col
    relatorio.append({"Coluna": col, "Total de Tokens": f"{total_col:,}"})

# Exibe o resultado formatado em tabela
df_relatorio = pd.DataFrame(relatorio)
print(df_relatorio.to_string(index=False))

print("-" * 50)
print(f"🚀 TOTAL GERAL (3 Colunas): {grand_total:,} tokens")
```

    📊 Contando tokens...
    
                                   Coluna Total de Tokens
                                    texto       3,325,969
                      texto_preprocessado       2,775,688
    texto_preprocessado_sem_justificativa         738,879
    --------------------------------------------------
    🚀 TOTAL GERAL (3 Colunas): 6,840,536 tokens
    


```python
api_key = os.environ["OPENAI_API_KEY"]
```


```python
client = OpenAI(api_key=api_key)

```


```python
# Inicializa cliente


# Exemplo de dataframe
df = pd.DataFrame({
    "texto": [
        "Projeto de lei sobre tributação de energia",
    ]
})

# Função para embedding
def get_embedding(texto, model="text-embedding-3-large"):
    response = client.embeddings.create(
        model=model,
        input=texto
    )
    return response.data[0].embedding

# Gerar embeddings com barra de progresso
emb = get_embedding("flamengo")
```


```python
len(emb)
```




    3072




```python
import numpy as np
import tiktoken
from tqdm import tqdm
from openai import OpenAI

# Inicialização (Certifique-se de ter a api_key definida)
client = OpenAI(api_key=api_key)

MODEL = "text-embedding-3-large"
MAX_INPUT_TOKENS = 8192
MAX_REQUEST_TOKENS = 300_000

enc = tiktoken.encoding_for_model(MODEL)

def process_and_count_tokens(text, max_tokens=MAX_INPUT_TOKENS):
    """
    Tokeniza o texto uma única vez, trunca se necessário,
    e retorna o texto processado, a contagem de tokens e se foi truncado.
    """
    # Garante que o input seja string para evitar quebras com NaN ou None
    text = str(text) if text is not None else ""
    
    tokens = enc.encode(text)
    was_truncated = len(tokens) > max_tokens

    if was_truncated:
        tokens = tokens[:max_tokens]
        text = enc.decode(tokens)
        
    return text, len(tokens), was_truncated


def normalize_embedding(vec):
    """
    Opcional. Os modelos text-embedding-3 já retornam por padrão
    embeddings normalizados, mas mantém a segurança se houver pós-processamento.
    """
    vec = np.asarray(vec, dtype=np.float32)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec.tolist()
    return (vec / norm).tolist()


def create_batches(texts, token_counts, max_batch_tokens=MAX_REQUEST_TOKENS):
    batches = []
    current_texts = []
    current_indices = []
    current_tokens = 0

    for idx, (text, n_tokens) in enumerate(zip(texts, token_counts)):
        # Se um único texto sozinho estourar o limite (caso mude o MAX_REQUEST_TOKENS)
        if n_tokens > max_batch_tokens:
            print(f"Aviso: Texto no índice {idx} individualmente excede o limite do batch.")

        if current_texts and current_tokens + n_tokens > max_batch_tokens:
            batches.append((current_indices, current_texts))
            current_indices = []
            current_texts = []
            current_tokens = 0

        current_indices.append(idx)
        current_texts.append(text)
        current_tokens += n_tokens

    if current_texts:
        batches.append((current_indices, current_texts))

    return batches


def embed_column(df, input_col, output_col, normalize=False):
    # Copia para evitar o warning 'SettingWithCopyWarning' do Pandas
    df = df.copy()
    
    texts = []
    token_counts = []
    trunc_flags = []

    # ------------------------------------
    # Pré-processamento (Otimizado: apenas uma chamada ao tiktoken)
    # ------------------------------------
    for text in df[input_col]:
        processed_text, n_tokens, truncated = process_and_count_tokens(text)
        texts.append(processed_text)
        token_counts.append(n_tokens)
        trunc_flags.append(truncated)

    print(
        f"\n[{input_col}]: {sum(trunc_flags)} textos truncados de {len(texts)} totais."
    )

    # ------------------------------------
    # Cria batches
    # ------------------------------------
    batches = create_batches(texts, token_counts, MAX_REQUEST_TOKENS)
    embeddings = [None] * len(texts)

    # ------------------------------------
    # Chama API
    # ------------------------------------
    for indices, batch_texts in tqdm(batches, desc=f"Embedding {input_col}"):
        response = client.embeddings.create(
            model=MODEL,
            input=batch_texts
        )

        for idx, emb_obj in zip(indices, response.data):
            emb = emb_obj.embedding
            if normalize:
                emb = normalize_embedding(emb)
            embeddings[idx] = emb

    df[output_col] = embeddings
    return df

```


```python


# ============================================================
# Colunas a processar
# ============================================================
cols = [
    ("texto", "embedding__openai__text_embedding_3_large__trunc8192__texto"),
    ("texto_preprocessado", "embedding__openai__text_embedding_3_large__trunc8192__texto_preprocessado"),
    ("texto_preprocessado_sem_justificativa", "embedding__openai__text_embedding_3_large__trunc8192__texto_preprocessado_sem_justificativa"),
]

# ============================================================
# Execução Segura
# ============================================================
# Criando o subset de teste

for col_in, col_out in cols:
    # Checa direto no df_teste para evitar inconsistências
    if col_in not in df.columns:
        print(f"Coluna '{col_in}' não encontrada no DataFrame. Pulando...")
        continue

    df = embed_column(
        df=df,
        input_col=col_in,
        output_col=col_out,
        normalize=False,
    )

print("\nConcluído com sucesso!")
```

    
    [texto]: 12 textos truncados de 2462 totais.
    

    Embedding texto: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 12/12 [02:02<00:00, 10.21s/it]
    

    
    [texto_preprocessado]: 8 textos truncados de 2462 totais.
    

    Embedding texto_preprocessado: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [02:24<00:00, 14.46s/it]
    

    
    [texto_preprocessado_sem_justificativa]: 2 textos truncados de 2462 totais.
    

    Embedding texto_preprocessado_sem_justificativa: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:52<00:00, 17.43s/it]

    
    Concluído com sucesso!
    

    
    


```python
def embed_text_meanpool(
    text,
    chunk_tokens=8192,
    normalize=True,
):
    """
    Divide um documento em chunks e faz mean pooling
    dos embeddings retornados pela OpenAI.
    """

    text = str(text) if text is not None else ""

    token_ids = enc.encode(text)

    if len(token_ids) == 0:
        token_ids = enc.encode(" ")

    chunks = [
        token_ids[i:i + chunk_tokens]
        for i in range(
            0,
            len(token_ids),
            chunk_tokens
        )
    ]

    chunk_texts = [
        enc.decode(chunk)
        for chunk in chunks
    ]

    response = client.embeddings.create(
        model=MODEL,
        input=chunk_texts
    )

    chunk_embeddings = np.asarray(
        [x.embedding for x in response.data],
        dtype=np.float32
    )

    doc_embedding = chunk_embeddings.mean(
        axis=0
    )

    if normalize:
        norm = np.linalg.norm(
            doc_embedding
        )

        if norm > 0:
            doc_embedding = (
                doc_embedding / norm
            )

    return doc_embedding.tolist()

def embed_column_meanpool(
    df,
    input_col,
    output_col,
    chunk_tokens=8192,
):
    df = df.copy()

    embeddings = []

    texts = (
        df[input_col]
        .fillna("")
        .astype(str)
        .tolist()
    )

    for idx, text in enumerate(
        tqdm(
            texts,
            desc=f"MeanPool {input_col}"
        )
    ):

        emb = embed_text_meanpool(
            text=text,
            chunk_tokens=chunk_tokens,
            normalize=True,
        )

        embeddings.append(emb)

        if idx % 500 == 0:
            print(
                f"{idx}/{len(texts)}"
            )

    df[output_col] = embeddings

    return df
```


```python
cols_meanpool = [
    (
        "texto",
        "embedding__openai__text_embedding_3_large__meanpool8192__texto"
    ),
    (
        "texto_preprocessado",
        "embedding__openai__text_embedding_3_large__meanpool8192__texto_preprocessado"
    ),
    (
        "texto_preprocessado_sem_justificativa",
        "embedding__openai__text_embedding_3_large__meanpool8192__texto_preprocessado_sem_justificativa"
    ),
]

for col_in, col_out in cols_meanpool:

    if col_in not in df.columns:
        print(
            f"Coluna '{col_in}' não encontrada. Pulando..."
        )
        continue

    if col_out not in df.columns:
        df = embed_column_meanpool(
            df=df,
            input_col=col_in,
            output_col=col_out,
            chunk_tokens=8192,
        )
    else:
        print(f"{col_out} já processada...")

print("\nConcluído com sucesso!")
```

    embedding__openai__text_embedding_3_large__meanpool8192__texto já processada...
    

    MeanPool texto_preprocessado:   0%|                                                                                                                                   | 1/2462 [00:01<1:11:01,  1.73s/it]

    0/2462
    

    MeanPool texto_preprocessado:  20%|██████████████████████████▋                                                                                                        | 501/2462 [16:32<21:47,  1.50it/s]

    500/2462
    

    MeanPool texto_preprocessado:  41%|████████████████████████████████████████████████████▊                                                                             | 1001/2462 [25:19<20:51,  1.17it/s]

    1000/2462
    

    MeanPool texto_preprocessado:  61%|███████████████████████████████████████████████████████████████████████████████▎                                                  | 1501/2462 [34:58<09:11,  1.74it/s]

    1500/2462
    

    MeanPool texto_preprocessado:  81%|█████████████████████████████████████████████████████████████████████████████████████████████████████████▋                        | 2001/2462 [40:41<05:21,  1.43it/s]

    2000/2462
    

    MeanPool texto_preprocessado: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [46:28<00:00,  1.13s/it]
    MeanPool texto_preprocessado_sem_justificativa:   0%|                                                                                                                 | 1/2462 [00:01<1:20:05,  1.95s/it]

    0/2462
    

    MeanPool texto_preprocessado_sem_justificativa:  20%|██████████████████████▉                                                                                          | 501/2462 [05:59<16:26,  1.99it/s]

    500/2462
    

    MeanPool texto_preprocessado_sem_justificativa:  41%|█████████████████████████████████████████████▌                                                                  | 1001/2462 [11:20<14:13,  1.71it/s]

    1000/2462
    

    MeanPool texto_preprocessado_sem_justificativa:  61%|████████████████████████████████████████████████████████████████████▎                                           | 1501/2462 [26:34<10:17,  1.56it/s]

    1500/2462
    

    MeanPool texto_preprocessado_sem_justificativa:  81%|███████████████████████████████████████████████████████████████████████████████████████████                     | 2001/2462 [31:48<04:11,  1.83it/s]

    2000/2462
    

    MeanPool texto_preprocessado_sem_justificativa: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [36:30<00:00,  1.12it/s]

    
    Concluído com sucesso!
    

    
    


```python
df_gemini.to_parquet("../data/datasets/embeddings.parquet")
```

## Google


```python
from google import genai


google_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

result = google_client.models.embed_content(
        model="gemini-embedding-2",
        contents="What is the meaning of life?"
)

print(result.embeddings)
```

    [ContentEmbedding(
      values=[
        -0.016332133,
        -0.0043764366,
        -0.0011324773,
        -0.011240026,
        0.00029597108,
        <... 3067 more items ...>,
      ]
    )]
    


```python
import math
import json
from tqdm import tqdm

CHUNK_TOKENS = 8192

def count_tokens(text, model="gemini-embedding-2"):
    result = google_client.models.count_tokens(
        model=model,
        contents=text
    )

    return result.total_tokens


def find_chunk_boundaries(
    text,
    model="gemini-embedding-2",
    chunk_tokens=CHUNK_TOKENS,
):
    """
    Retorna uma lista de offsets em caracteres.

    Exemplo:
    [0, 35211, 70182, 105901, len(text)]

    Cada intervalo contém aproximadamente
    chunk_tokens tokens.
    """

    text = str(text) if text is not None else ""

    if len(text) == 0:
        return [0]

    total_tokens = count_tokens(
        text=text,
        model=model
    )

    if total_tokens <= chunk_tokens:
        return [0, len(text)]

    boundaries = [0]

    target_tokens_list = list(
        range(
            chunk_tokens,
            total_tokens,
            chunk_tokens
        )
    )

    previous_pos = 0

    for target_tokens in target_tokens_list:

        low = previous_pos
        high = len(text)

        best_pos = previous_pos

        while low <= high:

            mid = (low + high) // 2

            current_tokens = count_tokens(
                text=text[:mid],
                model=model
            )

            if current_tokens <= target_tokens:
                best_pos = mid
                low = mid + 1
            else:
                high = mid - 1

        boundaries.append(best_pos)
        previous_pos = best_pos

    boundaries.append(len(text))

    return boundaries
```


```python
COLS = [
    "texto",
    "texto_preprocessado",
    "texto_preprocessado_sem_justificativa",
]

for col in COLS:

    out_col = f"gemini_embedding_2_chunk_boundaries__{col}"

    boundaries_all = []

    for text in tqdm(
        df[col],
        desc=f"Boundary {col}"
    ):

        boundaries = find_chunk_boundaries(
            text=text,
            model="gemini-embedding-2",
            chunk_tokens=8192,
        )

        boundaries_all.append(
            boundaries
        )

    df[out_col] = boundaries_all
```

    Boundary texto: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [14:28<00:00,  2.84it/s]
    Boundary texto_preprocessado: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [14:29<00:00,  2.83it/s]
    Boundary texto_preprocessado_sem_justificativa: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [11:34<00:00,  3.54it/s]
    


```python
texto_teste = """
Art. 1º Esta Lei estabelece normas gerais para a gestão,
monitoramento e transparência de programas públicos.

Art. 2º Os órgãos da administração pública deverão publicar,
em formato aberto, os dados relativos à execução orçamentária,
financeira e patrimonial.

Art. 3º Esta Lei entra em vigor na data de sua publicação.
""" * 1000  # força um texto grande

texto_truncado, n_tokens, truncado = (
    truncate_to_gemini_limit(texto_teste)
)

print("Texto original:")
print(len(texto_teste), "caracteres")

print("\nResultado:")
print("Truncado?", truncado)
print("Tokens:", n_tokens)
print("Caracteres finais:", len(texto_truncado))

# conferência final
tokens_finais = google_client.models.count_tokens(
    model="gemini-embedding-2",
    contents=texto_truncado
).total_tokens

print("Tokens conferidos:", tokens_finais)
```

    Texto original:
    322000 caracteres
    
    Resultado:
    Truncado? True
    Tokens: 8192
    Caracteres finais: 32550
    Tokens conferidos: 8192
    


```python
import numpy as np

from tqdm import tqdm
from google.genai import types

MODEL = "gemini-embedding-2"

MAX_INPUT_TOKENS = 8192
MAX_BATCH_TOKENS = 100_000
MAX_BATCH_DOCS = 20


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def normalize_embedding(vec):

    vec = np.asarray(
        vec,
        dtype=np.float32
    )

    norm = np.linalg.norm(vec)

    if norm > 0:
        vec = vec / norm

    return vec.tolist()


# ============================================================
# TRUNCAMENTO VIA BOUNDARIES
# ============================================================

def truncate_using_boundaries(
    text,
    boundaries,
):
    text = str(text) if text is not None else ""

    if not boundaries:
        return text, False

    # cabe inteiro
    if len(boundaries) <= 2:
        return text, False

    # pega apenas o primeiro chunk (~8192 tokens)
    truncated_text = text[
        boundaries[0]:
        boundaries[1]
    ]

    return truncated_text, True


# ============================================================
# BATCHES
# ============================================================

def create_batches(
    texts,
    token_counts,
    max_batch_tokens=MAX_BATCH_TOKENS,
    max_batch_docs=MAX_BATCH_DOCS,
):

    batches = []

    current_texts = []
    current_indices = []
    current_tokens = 0

    for idx, (text, n_tokens) in enumerate(
        zip(texts, token_counts)
    ):

        flush = (
            len(current_texts) >= max_batch_docs
            or current_tokens + n_tokens > max_batch_tokens
        )

        if current_texts and flush:

            batches.append(
                (
                    current_indices,
                    current_texts
                )
            )

            current_texts = []
            current_indices = []
            current_tokens = 0

        current_indices.append(idx)

        current_texts.append(text)

        current_tokens += n_tokens

    if current_texts:

        batches.append(
            (
                current_indices,
                current_texts
            )
        )

    return batches


# ============================================================
# EMBEDDINGS
# ============================================================

def embed_column_gemini(
    df,
    input_col,
    boundaries_col,
    output_col,
    normalize=False,
):

    texts = []
    token_counts = []
    trunc_flags = []

    print(
        f"\nPreparando {input_col}"
    )

    iterator = zip(
        df[input_col],
        df[boundaries_col]
    )

    for text, boundaries in tqdm(
        iterator,
        total=len(df),
        desc=f"Preparando {input_col}"
    ):

        processed_text, truncated = (
            truncate_using_boundaries(
                text=text,
                boundaries=boundaries
            )
        )

        texts.append(
            processed_text
        )

        trunc_flags.append(
            truncated
        )

        # estimativa apenas para batching
        if truncated:

            token_counts.append(
                MAX_INPUT_TOKENS
            )

        else:

            token_counts.append(
                max(
                    1,
                    len(processed_text) // 4
                )
            )

    print(
        f"\n[{input_col}] "
        f"{sum(trunc_flags)} truncados "
        f"de {len(texts)}"
    )

    batches = create_batches(
        texts=texts,
        token_counts=token_counts
    )

    print(
        f"{len(batches)} batches"
    )

    embeddings = [None] * len(texts)

    for indices, batch_texts in tqdm(
        batches,
        desc=f"Embedding {input_col}"
    ):

        contents = [
            types.Content(
                parts=[
                    types.Part.from_text(
                        text=t
                    )
                ]
            )
            for t in batch_texts
        ]

        result = (
            google_client
            .models
            .embed_content(
                model=MODEL,
                contents=contents
            )
        )

        if len(result.embeddings) != len(batch_texts):

            raise RuntimeError(
                f"Esperados {len(batch_texts)} embeddings, "
                f"recebidos {len(result.embeddings)}."
            )

        for idx, emb in zip(
            indices,
            result.embeddings
        ):

            vec = emb.values

            if normalize:

                vec = normalize_embedding(
                    vec
                )

            embeddings[idx] = vec

    df[output_col] = embeddings

    return df


# ============================================================
# COLUNAS
# ============================================================

cols = [
    (
        "texto",
        "gemini_embedding_2_chunk_boundaries__texto",
        "embedding__google__gemini_embedding_2__trunc8192__texto"
    ),
    (
        "texto_preprocessado",
        "gemini_embedding_2_chunk_boundaries__texto_preprocessado",
        "embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado"
    ),
    (
        "texto_preprocessado_sem_justificativa",
        "gemini_embedding_2_chunk_boundaries__texto_preprocessado_sem_justificativa",
        "embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado_sem_justificativa"
    ),
]


# ============================================================
# EXECUÇÃO
# ============================================================

df_gemini = df.copy()

for (
    input_col,
    boundaries_col,
    output_col
) in cols:

    if input_col not in df_gemini.columns:

        print(
            f"Coluna '{input_col}' não encontrada."
        )

        continue

    if boundaries_col not in df_gemini.columns:

        print(
            f"Coluna '{boundaries_col}' não encontrada."
        )

        continue

    if output_col in df_gemini.columns:

        print(
            f"[OK] {output_col}"
        )

        continue

    df_gemini = embed_column_gemini(
        df=df_gemini,
        input_col=input_col,
        boundaries_col=boundaries_col,
        output_col=output_col,
        normalize=False,
    )

    print(
        f"Concluído: {output_col}"
    )

print(
    "\nProcessamento finalizado."
)
```

    
    Preparando texto
    

    Preparando texto: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [00:00<00:00, 307662.27it/s]
    

    
    [texto] 11 truncados de 2462
    124 batches
    

    Embedding texto: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 124/124 [05:03<00:00,  2.45s/it]
    

    Concluído: embedding__google__gemini_embedding_2__trunc8192__texto
    
    Preparando texto_preprocessado
    

    Preparando texto_preprocessado: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [00:00<00:00, 307909.96it/s]
    

    
    [texto_preprocessado] 8 truncados de 2462
    124 batches
    

    Embedding texto_preprocessado: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 124/124 [04:26<00:00,  2.15s/it]
    

    Concluído: embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado
    
    Preparando texto_preprocessado_sem_justificativa
    

    Preparando texto_preprocessado_sem_justificativa: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 2462/2462 [00:00<00:00, 352063.57it/s]
    

    
    [texto_preprocessado_sem_justificativa] 1 truncados de 2462
    124 batches
    

    Embedding texto_preprocessado_sem_justificativa: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 124/124 [03:20<00:00,  1.62s/it]

    Concluído: embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado_sem_justificativa
    
    Processamento finalizado.
    

    
    

### Mean Pool


```python
df_gemini.to_parquet("../data/datasets/embeddings.parquet", index=False)
```


```python
import time
import numpy as np
import random
from tqdm import tqdm
from collections import defaultdict
from google.genai import types
from google.genai.errors import ClientError

MODEL = "gemini-embedding-2"

# =========================
# LIMITES (SEGURO)
# =========================

TPM_LIMIT = 1_000_000
SAFETY_FACTOR = 0.4
TPM_BUDGET = int(TPM_LIMIT * SAFETY_FACTOR)

MAX_CHUNKS_PER_BATCH = 6
MIN_REQUEST_INTERVAL = 0.4  # controle de burst/RPM

# =========================
# RATE LIMITER GLOBAL
# =========================

window_start = time.time()
tokens_used = 0
last_request_time = 0


def wait_if_needed(batch_tokens_estimate):
    global window_start, tokens_used, last_request_time

    now = time.time()

    # -------------------------
    # throttle de burst (RPM)
    # -------------------------
    elapsed = now - last_request_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)

    last_request_time = time.time()

    # -------------------------
    # reset janela TPM
    # -------------------------
    if now - window_start >= 60:
        window_start = now
        tokens_used = 0

    # -------------------------
    # controle TPM
    # -------------------------
    if tokens_used + batch_tokens_estimate > TPM_BUDGET:
        sleep_time = 60 - (now - window_start)

        if sleep_time > 0:
            print(f"⏳ TPM atingido. Dormindo {sleep_time:.1f}s")
            time.sleep(sleep_time)

        window_start = time.time()
        tokens_used = 0

    tokens_used += batch_tokens_estimate


# =========================
# RETRY ROBUSTO
# =========================

def embed_with_retry(contents, max_retries=6):
    for i in range(max_retries):
        try:
            return google_client.models.embed_content(
                model=MODEL,
                contents=contents
            )

        except ClientError as e:
            if getattr(e, "status_code", None) == 429 or "RESOURCE_EXHAUSTED" in str(e):
                sleep = min(60, (2 ** i) + random.uniform(0, 1))
                print(f"[429] retry {i+1}/{max_retries} → sleep {sleep:.2f}s")
                time.sleep(sleep)
            else:
                raise

    raise RuntimeError("Max retries exceeded")


# =========================
# NORMALIZAÇÃO
# =========================

def normalize(vec):
    vec = np.asarray(vec, dtype=np.float32)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec.tolist()


# =========================
# CHUNKS
# =========================

def extract_chunks(text, boundaries):
    text = str(text) if text is not None else ""

    if not boundaries or len(boundaries) <= 2:
        return [text]

    return [text[s:e] for s, e in zip(boundaries[:-1], boundaries[1:])]


def build_chunks(df, text_col, boundary_col):
    all_chunks = []
    doc_ids = []

    for doc_id, (text, boundaries) in enumerate(zip(df[text_col], df[boundary_col])):
        chunks = extract_chunks(text, boundaries)

        for c in chunks:
            all_chunks.append(c)
            doc_ids.append(doc_id)

    return all_chunks, doc_ids


def batch_chunks(chunks):
    for i in range(0, len(chunks), MAX_CHUNKS_PER_BATCH):
        yield i, chunks[i:i + MAX_CHUNKS_PER_BATCH]


def estimate_tokens(text):
    return int(len(text.split()) * 1.3)


# =========================
# PIPELINE PRINCIPAL
# =========================

def embed_meanpool_gemini(
    df,
    text_col,
    boundary_col,
    output_col,
    normalize_vec=True
):

    print(f"\nProcessando: {text_col}")

    all_chunks, chunk_doc_ids = build_chunks(df, text_col, boundary_col)

    print(f"Total chunks: {len(all_chunks)}")

    doc_vectors = defaultdict(list)

    batches = list(batch_chunks(all_chunks))

    print(f"Batches: {len(batches)}")

    for start_idx, batch in tqdm(batches, desc="Embedding chunks"):

        # estimativa mais segura de tokens
        batch_tokens_estimate = sum(estimate_tokens(t) for t in batch)

        wait_if_needed(batch_tokens_estimate)

        contents = [
            types.Content(parts=[types.Part.from_text(text=t)])
            for t in batch
        ]

        result = embed_with_retry(contents)

        for emb, doc_id in zip(
            result.embeddings,
            chunk_doc_ids[start_idx:start_idx + len(batch)]
        ):
            doc_vectors[doc_id].append(emb.values)

    # =========================
    # MEAN POOL FINAL
    # =========================

    final_embeddings = []

    for i in range(len(df)):
        vecs = doc_vectors[i]

        if not vecs:
            final_embeddings.append(None)
            continue

        vecs = np.asarray(vecs, dtype=np.float32)
        mean_vec = vecs.mean(axis=0)

        if normalize_vec:
            mean_vec = normalize(mean_vec)

        final_embeddings.append(mean_vec)

    df[output_col] = final_embeddings
    return df


# =========================
# EXECUÇÃO
# =========================

cols = [
    (
        "texto",
        "gemini_embedding_2_chunk_boundaries__texto",
        "embedding__google__gemini_embedding_2__meanpool8192__texto"
    ),
    (
        "texto_preprocessado",
        "gemini_embedding_2_chunk_boundaries__texto_preprocessado",
        "embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado"
    ),
    (
        "texto_preprocessado_sem_justificativa",
        "gemini_embedding_2_chunk_boundaries__texto_preprocessado_sem_justificativa",
        "embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado_sem_justificativa"
    ),
]

for text_col, boundary_col, out_col in cols:

    if out_col in df_gemini.columns:
        print(f"[OK] {out_col}")
        continue

    df_gemini = embed_meanpool_gemini(
        df=df_gemini,
        text_col=text_col,
        boundary_col=boundary_col,
        output_col=out_col,
        normalize_vec=False
    )

    print(f"Concluído: {out_col}")

print("\nFinalizado")
```

    
    Processando: texto
    Total chunks: 2473
    Batches: 413
    

    Embedding chunks:  25%|███████████████████████████████████▌                                                                                                            | 102/413 [03:55<16:24,  3.17s/it]

    [429] retry 1/6 → sleep 1.51s
    

    Embedding chunks:  77%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████▌                                | 320/413 [09:52<02:56,  1.90s/it]

    [429] retry 1/6 → sleep 1.73s
    

    Embedding chunks: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 413/413 [12:09<00:00,  1.77s/it]
    

    Concluído: embedding__google__gemini_embedding_2__meanpool8192__texto
    
    Processando: texto_preprocessado
    Total chunks: 2470
    Batches: 412
    

    Embedding chunks:  29%|█████████████████████████████████████████▏                                                                                                      | 118/412 [02:45<12:55,  2.64s/it]

    [429] retry 1/6 → sleep 1.12s
    [429] retry 2/6 → sleep 2.14s
    

    Embedding chunks:  92%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊            | 377/412 [08:45<01:36,  2.76s/it]

    [429] retry 1/6 → sleep 1.22s
    

    Embedding chunks: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 412/412 [09:26<00:00,  1.37s/it]
    

    Concluído: embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado
    
    Processando: texto_preprocessado_sem_justificativa
    Total chunks: 2463
    Batches: 411
    

    Embedding chunks:  12%|█████████████████▉                                                                                                                               | 51/411 [01:21<21:29,  3.58s/it]

    [429] retry 1/6 → sleep 1.27s
    

    Embedding chunks:  48%|█████████████████████████████████████████████████████████████████████                                                                           | 197/411 [04:15<09:23,  2.64s/it]

    [429] retry 1/6 → sleep 1.39s
    [429] retry 2/6 → sleep 2.47s
    

    Embedding chunks:  60%|██████████████████████████████████████████████████████████████████████████████████████▌                                                         | 247/411 [05:15<06:39,  2.43s/it]

    [429] retry 1/6 → sleep 1.43s
    [429] retry 2/6 → sleep 2.21s
    

    Embedding chunks:  85%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉                      | 348/411 [07:16<02:29,  2.37s/it]

    [429] retry 1/6 → sleep 1.30s
    [429] retry 2/6 → sleep 2.13s
    

    Embedding chunks: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 411/411 [08:30<00:00,  1.24s/it]
    

    Concluído: embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado_sem_justificativa
    
    Finalizado
    


```python
df_gemini.columns
```




    Index(['num_emenda', 'materia', 'texto', 'texto_preprocessado',
           'texto_preprocessado_sem_justificativa', 'tema', 'tema_macro',
           'tema_nivel_2', 'embedding__codefuse_ai__F2LLM_v2_14B__texto',
           'embedding__codefuse_ai__F2LLM_v2_14B__texto_preprocessado',
           'embedding__codefuse_ai__F2LLM_v2_14B__texto_preprocessado_sem_justificativa',
           'embedding__Octen__Octen_Embedding_8B__texto',
           'embedding__Octen__Octen_Embedding_8B__texto_preprocessado',
           'embedding__Octen__Octen_Embedding_8B__texto_preprocessado_sem_justificativa',
           'embedding__Qwen__Qwen3_Embedding_8B__texto',
           'embedding__Qwen__Qwen3_Embedding_8B__texto_preprocessado',
           'embedding__Qwen__Qwen3_Embedding_8B__texto_preprocessado_sem_justificativa',
           'embedding__nvidia__llama_embed_nemotron_8b__texto',
           'embedding__nvidia__llama_embed_nemotron_8b__texto_preprocessado',
           'embedding__nvidia__llama_embed_nemotron_8b__texto_preprocessado_sem_justificativa',
           'embedding__jinaai__jina_embeddings_v5_text_small__clustering__texto',
           'embedding__jinaai__jina_embeddings_v5_text_small__clustering__texto_preprocessado',
           'embedding__jinaai__jina_embeddings_v5_text_small__clustering__texto_preprocessado_sem_justificativa',
           'embedding__jinaai__jina_embeddings_v5_text_small__text_matching__texto',
           'embedding__jinaai__jina_embeddings_v5_text_small__text_matching__texto_preprocessado',
           'embedding__jinaai__jina_embeddings_v5_text_small__text_matching__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__trunc128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__trunc128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__trunc128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__meanpool128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__meanpool128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder__meanpool128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__trunc128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__trunc128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__trunc128__texto_preprocessado_sem_justificativa',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__meanpool128__texto',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__meanpool128__texto_preprocessado',
           'embedding__PORTULAN__serafim_900m_portuguese_pt_sentence_encoder_ir__meanpool128__texto_preprocessado_sem_justificativa',
           'embedding__joaorobson__harrier_oss_v1_27b__texto',
           'embedding__joaorobson__harrier_oss_v1_27b__texto_preprocessado',
           'embedding__joaorobson__harrier_oss_v1_27b__texto_preprocessado_sem_justificativa',
           'embedding__joaorobson__KaLM_Embedding_Gemma3_12B_2511__texto',
           'embedding__joaorobson__KaLM_Embedding_Gemma3_12B_2511__texto_preprocessado',
           'embedding__joaorobson__KaLM_Embedding_Gemma3_12B_2511__texto_preprocessado_sem_justificativa',
           'embedding__openai__text_embedding_3_large__trunc8192__texto',
           'embedding__openai__text_embedding_3_large__trunc8192__texto_preprocessado',
           'embedding__openai__text_embedding_3_large__trunc8192__texto_preprocessado_sem_justificativa',
           'embedding__openai__text_embedding_3_large__meanpool8192__texto',
           'embedding__openai__text_embedding_3_large__meanpool8192__texto_preprocessado',
           'embedding__openai__text_embedding_3_large__meanpool8192__texto_preprocessado_sem_justificativa',
           'gemini_embedding_2_chunk_boundaries__texto',
           'gemini_embedding_2_chunk_boundaries__texto_preprocessado',
           'gemini_embedding_2_chunk_boundaries__texto_preprocessado_sem_justificativa',
           'embedding__google__gemini_embedding_2__trunc8192__texto',
           'embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado',
           'embedding__google__gemini_embedding_2__trunc8192__texto_preprocessado_sem_justificativa',
           'embedding__google__gemini_embedding_2__meanpool8192__texto',
           'embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado',
           'embedding__google__gemini_embedding_2__meanpool8192__texto_preprocessado_sem_justificativa'],
          dtype='object')


