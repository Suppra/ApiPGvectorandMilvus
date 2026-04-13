import os
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from app.schemas import DocumentoCreate, DocumentoUpdate, SearchRequest, Documento
from dotenv import load_dotenv
import uuid

load_dotenv()

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = os.getenv("MILVUS_COLLECTION", "documentos_milvus_api")

connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

# Definición de esquema
fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=64),
    FieldSchema(name="titulo", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="contenido", dtype=DataType.VARCHAR, max_length=1024),
    FieldSchema(name="categoria", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=4)
]
schema = CollectionSchema(fields, description="Colección de documentos para demo Milvus")


# Crear colección si no existe
if COLLECTION_NAME not in utility.list_collections():
    col = Collection(COLLECTION_NAME, schema)
    col.flush()
else:
    col = Collection(COLLECTION_NAME)

col.load()

def milvus_list_docs():
    expr = "id != ''"
    results = col.query(expr, output_fields=["id", "titulo", "contenido", "categoria", "embedding"])
    return [Documento(**r) for r in results]

def milvus_get_doc(id: str):
    results = col.query(f"id == '{id}'", output_fields=["id", "titulo", "contenido", "categoria", "embedding"])
    if results:
        return Documento(**results[0])
    return None

def milvus_create_doc(doc: DocumentoCreate):
    doc_id = doc.id or str(uuid.uuid4())
    data = [
        [doc_id],
        [doc.titulo],
        [doc.contenido],
        [doc.categoria],
        [doc.embedding]
    ]
    col.insert(data)
    col.flush()
    return milvus_get_doc(doc_id)

def milvus_update_doc(id: str, doc: DocumentoUpdate):
    # Milvus no soporta update directo, se elimina y se inserta de nuevo
    milvus_delete_doc(id)
    doc_data = doc.dict(exclude_unset=True)
    doc_data['id'] = id
    # Recuperar datos antiguos si faltan campos
    old = milvus_get_doc(id)
    if old:
        for k, v in old.dict().items():
            if k not in doc_data or doc_data[k] is None:
                doc_data[k] = v
    return milvus_create_doc(DocumentoCreate(**doc_data))

def milvus_delete_doc(id: str):
    col.delete(f"id == '{id}'")
    col.flush()

def milvus_search_docs(req: SearchRequest):
    search_params = {"metric_type": "L2", "params": {"ef": 32}}
    expr = None
    if req.categoria:
        expr = f"categoria == '{req.categoria}'"
    results = col.search(
        data=[req.embedding],
        anns_field="embedding",
        param=search_params,
        limit=req.top_k,
        expr=expr,
        output_fields=["id", "titulo", "contenido", "categoria", "embedding"]
    )
    docs = []
    for hits in results:
        for hit in hits:
            docs.append(Documento(**hit.entity))
    return docs
