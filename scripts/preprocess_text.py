import re
import pandas as pd

def extract_until_any(text, stop_words):
    lower_text = text.lower()
    matches = []

    for word in stop_words:
        idx = lower_text.find(word.lower())
        if idx != -1:
            matches.append(idx)

    if not matches:
        return text

    first_stop = min(matches)
    return text[:first_stop]

def remove_title(text):
    pattern = r'^Gabinete do Senador .+?\nEMENDA Nº[^\n]*\n\(ao PL \d+/\d{4}\)\n'
    return re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)

def extract_after_pl(text):
    pattern = r'(?:\((?:ao)?\s*(?:substitutivo ao)?\s*(?:Projeto de Lei|PLP?|Projeto de Lei Complementar)\s*(?:n[ºo]\.?)?\s*[\d,\.]+/?(?:,?\s*de\s*|\s*/)\d{4}\))(.*)'
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return text  # Return original text if no match

def remove_lexedit_id(text):
    cleaned = re.sub(r'SF/\d+\.\d+-\d+\s+\(LexEdit\*?\)', '', text)
    return cleaned

def remove_digital_signature(text):
    pattern = r'Assinado eletronicamente, por .*?\nPara verificar as assinaturas, acesse https://legis\.senado\.gov\.br/autenticadoc-legis/\d+'
    cleaned = re.sub(pattern, '', text)
    return cleaned.strip()


df = pd.read_parquet("data/PLP_68_2024_textos_emendas.parquet")

# Só emendas com temas definidos no quadro comparativo
df = df[df.num_emenda <= 1998].reset_index(drop=True)

just_variacoes = ["justificação", "justificativa", "j u s t i f i c a ç ã o", "j u s t i f i c a ç ã", "JUSTIFICAÇÃ\nO"]
df["texto_sem_justificativa"] = df.texto.apply(lambda x: extract_until_any(x,  just_variacoes))

df["texto_preprocessado"] = df.texto_sem_justificativa.apply(extract_after_pl)