from pydantic import BaseModel, Field


class Region(BaseModel):
    label: str
    x: int
    y: int
    width: int
    height: int


class PageAnnotation(BaseModel):
    image_path: str
    mpv_nome: str
    emenda_nome: str
    pagina_idx: int
    regions: list[Region] = Field(default_factory=list)