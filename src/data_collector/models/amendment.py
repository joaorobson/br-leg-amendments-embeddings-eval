from typing import Optional

from pydantic import BaseModel, Field

class Amendment(BaseModel):
    id: int
    id_documento_emenda: int = Field(..., alias="idDocumentoEmenda")
    url_documento_emenda: str = Field(..., alias="urlDocumentoEmenda")
    descricao_documento_emenda: str | None = Field(None, alias="descricaoDocumentoEmenda")
    id_ci_emenda: int = Field(..., alias="idCiEmenda")
    id_ci_emendado: int = Field(..., alias="idCiEmendado")
    id_processo: int = Field(..., alias="idProcesso")
    data_apresentacao: str = Field(..., alias="dataApresentacao")
    codigo_colegiado: int = Field(..., alias="codigoColegiado")
    casa: str
    sigla_colegiado: str = Field(..., alias="siglaColegiado")
    nome_colegiado: str = Field(..., alias="nomeColegiado")
    autoria: str
    numero: str
    identificacao: str
    tipo: str
    turno_apresentacao: str = Field(..., alias="turnoApresentacao")
    decisoes: Optional[list] = None
    subemendas: Optional[list] = None