import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.database import Base
from sqlalchemy import Column, String, Text
from pgvector.sqlalchemy import Vector
from app.schemas import DocumentoCreate, DocumentoUpdate, SearchRequest

class DocumentoPG(Base):
    __tablename__ = "documentos"
    id = Column(String, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    contenido = Column(Text, nullable=False)
    categoria = Column(String, nullable=False)
    embedding = Column(Vector(4), nullable=False)

Base.metadata.create_all = lambda bind=None: None  # Evita crear tablas automáticamente

def get_all_docs(db: Session):
    return db.query(DocumentoPG).all()

def get_doc_by_id(db: Session, id: str):
    return db.query(DocumentoPG).filter(DocumentoPG.id == id).first()

def create_doc(db: Session, doc: DocumentoCreate):
    doc_id = doc.id or str(uuid.uuid4())
    db_doc = DocumentoPG(
        id=doc_id,
        titulo=doc.titulo,
        contenido=doc.contenido,
        categoria=doc.categoria,
        embedding=doc.embedding
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def update_doc(db: Session, id: str, doc: DocumentoUpdate):
    db_doc = db.query(DocumentoPG).filter(DocumentoPG.id == id).first()
    if not db_doc:
        raise Exception("Documento no encontrado")
    for field, value in doc.dict(exclude_unset=True).items():
        setattr(db_doc, field, value)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def delete_doc(db: Session, id: str):
    db_doc = db.query(DocumentoPG).filter(DocumentoPG.id == id).first()
    if db_doc:
        db.delete(db_doc)
        db.commit()

def search_similar_docs(db: Session, req: SearchRequest):
    query = db.query(DocumentoPG)
    if req.categoria:
        query = query.filter(DocumentoPG.categoria == req.categoria)
    # Ordenar por similitud (distancia L2)
    query = query.order_by(DocumentoPG.embedding.l2_distance(req.embedding))
    return query.limit(req.top_k).all()
