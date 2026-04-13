from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import Documento, DocumentoCreate, DocumentoUpdate, SearchRequest
from app.services.pgvector_service import (
    get_all_docs, get_doc_by_id, create_doc, update_doc, delete_doc, search_similar_docs
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/documentos", response_model=list[Documento])
def listar_documentos(db: Session = Depends(get_db)):
    return get_all_docs(db)

@router.get("/documentos/{id}", response_model=Documento)
def obtener_documento(id: str, db: Session = Depends(get_db)):
    doc = get_doc_by_id(db, id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc

@router.post("/documentos", response_model=Documento)
def crear_documento(doc: DocumentoCreate, db: Session = Depends(get_db)):
    return create_doc(db, doc)

@router.put("/documentos/{id}", response_model=Documento)
def actualizar_documento(id: str, doc: DocumentoUpdate, db: Session = Depends(get_db)):
    return update_doc(db, id, doc)

@router.delete("/documentos/{id}")
def eliminar_documento(id: str, db: Session = Depends(get_db)):
    delete_doc(db, id)
    return {"detail": "Documento eliminado"}

@router.post("/search", response_model=list[Documento])
def busqueda_vectorial(req: SearchRequest, db: Session = Depends(get_db)):
    return search_similar_docs(db, req)
