from fastapi import APIRouter, HTTPException
from app.schemas import Documento, DocumentoCreate, DocumentoUpdate, SearchRequest
from app.services.milvus_service import (
    milvus_list_docs, milvus_get_doc, milvus_create_doc, milvus_update_doc, milvus_delete_doc, milvus_search_docs
)

router = APIRouter()

@router.get("/documentos", response_model=list[Documento])
def listar_documentos():
    return milvus_list_docs()

@router.get("/documentos/{id}", response_model=Documento)
def obtener_documento(id: str):
    doc = milvus_get_doc(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc

@router.post("/documentos", response_model=Documento)
def crear_documento(doc: DocumentoCreate):
    return milvus_create_doc(doc)

@router.put("/documentos/{id}", response_model=Documento)
def actualizar_documento(id: str, doc: DocumentoUpdate):
    return milvus_update_doc(id, doc)

@router.delete("/documentos/{id}")
def eliminar_documento(id: str):
    milvus_delete_doc(id)
    return {"detail": "Documento eliminado"}

@router.post("/search", response_model=list[Documento])
def busqueda_vectorial(req: SearchRequest):
    return milvus_search_docs(req)
