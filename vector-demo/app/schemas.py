from typing import List, Optional
from pydantic import BaseModel, Field, validator

class DocumentoBase(BaseModel):
    titulo: str
    contenido: str
    categoria: str
    embedding: List[float] = Field(..., min_items=4, max_items=4)

    @validator('embedding')
    def embedding_length(cls, v):
        if len(v) != 4:
            raise ValueError('El embedding debe tener dimensión 4')
        return v

class DocumentoCreate(DocumentoBase):
    id: Optional[str] = None

class DocumentoUpdate(BaseModel):
    titulo: Optional[str]
    contenido: Optional[str]
    categoria: Optional[str]
    embedding: Optional[List[float]]

class Documento(DocumentoBase):
    id: str
    class Config:
        orm_mode = True

class SearchRequest(BaseModel):
    embedding: List[float] = Field(..., min_items=4, max_items=4)
    categoria: Optional[str] = None
    top_k: int = 3
