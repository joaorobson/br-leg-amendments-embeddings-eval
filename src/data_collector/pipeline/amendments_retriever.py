import requests
import os
from data_collector.models import Amendment
import re
import pandas as pd
import time

class AmendmenstsRetriever:
    AMENDMENT_URL = (
        "https://legis.senado.leg.br/dadosabertos/processo/emenda?codigoMateria={}&v=1"
    )

    def __init__(self, proposition_code, proposition_name):
        self.amendment_list = []
        self.proposition_code = proposition_code
        self.proposition_name = proposition_name

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Substitui caracteres inválidos por underscore (_) para gerar nomes de arquivos seguros.
        """
        return re.sub(r'[ \\/:*?"<>|]+', "_", name)

    def get_amendment_pdf(self, url): ...

    @staticmethod
    def get_request(url, headers={}, max_retries=3, backoff=2):
        for attempt in range(max_retries):
            try:
                # O timeout é essencial para não travar o pipeline no 502
                response = requests.get(url, headers=headers, timeout=20)
                
                if response.status_code == 200:
                    return response
                
                print(f"Tentativa {attempt + 1}: Erro {response.status_code} em {url}")
            
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão na tentativa {attempt + 1}: {e}")
            
            # Espera exponencial para aliviar o servidor do Senado
            time.sleep(backoff * (attempt + 1))
        
        return None

    def get_amendments_list(self, amendments_to_consider=[]):
        response = AmendmenstsRetriever.get_request(
            self.AMENDMENT_URL.format(self.proposition_code),
            {"Accept": "application/json"}
        )
        
        # Se a resposta for nula (falhou nos retries), interrompe
        if not response:
            print("Erro crítico: Não foi possível recuperar a lista de emendas.")
            return

        try:
            dados = response.json()
            if amendments_to_consider:
                self.amendment_list = [
                    Amendment(**am) for am in dados
                    if int(am.get("numero", -1)) in amendments_to_consider
                ]
            else:
                self.amendment_list = [Amendment(**am) for am in dados]
        except Exception as e:
            print(f"Erro ao processar JSON da lista: {e}")

    @staticmethod
    def store_pdf(content, folder, filename):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder '{folder}' created.")

        with open(os.path.join(folder, filename), "wb") as f:
            f.write(content)

    def get_amendments_pdfs(self, path):
        folder = os.path.join(path, self.proposition_name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for amendment in self.amendment_list:
            filename = f"{AmendmenstsRetriever.sanitize_filename(amendment.identificacao)}.pdf"
            full_path = os.path.join(folder, filename)

            if os.path.exists(full_path):
                continue

            print(f"Baixando: {amendment.url_documento_emenda}")
            
            # Chama o método com a lógica de repetição
            response = AmendmenstsRetriever.get_request(amendment.url_documento_emenda)
            
            if response and response.status_code == 200:
                if b"<html>" not in response.content[:100]:
                    AmendmenstsRetriever.store_pdf(response.content, folder, filename)
                else:
                    print(f"Aviso: O link {amendment.identificacao} retornou HTML em vez de PDF.")

    def store_metadata(self, path):
        df = pd.DataFrame([am.model_dump() for am in self.amendment_list])
        df.to_parquet(path)
