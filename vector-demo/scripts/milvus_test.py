import os
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
from dotenv import load_dotenv
import uuid

load_dotenv()

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = os.getenv("MILVUS_COLLECTION", "documentos_milvus_api")

connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=64),
    FieldSchema(name="titulo", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="contenido", dtype=DataType.VARCHAR, max_length=1024),
    FieldSchema(name="categoria", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=4)
]
schema = CollectionSchema(fields, description="Colección de documentos para demo Milvus")


from pymilvus import utility
if COLLECTION_NAME not in utility.list_collections():
    col = Collection(COLLECTION_NAME, schema)
    col.flush()

else:
    col = Collection(COLLECTION_NAME)

# Crear índice HNSW si no existe
if not col.has_index():
    index_params = {
        "metric_type": "L2",
        "index_type": "HNSW",
        "params": {"M": 8, "efConstruction": 64}
    }
    col.create_index(field_name="embedding", index_params=index_params)

col.load()

def print_docs(msg):
    print(f"\n--- {msg} ---")
    docs = col.query("id != ''", output_fields=["id", "titulo", "contenido", "categoria", "embedding"])
    for d in docs:
        print(d)

# 1. Insertar documentos de ejemplo
example_docs = [
    {"id": "1", "titulo": "Introducción a PostgreSQL", "contenido": "PostgreSQL es una base de datos relacional avanzada.", "categoria": "PostgreSQL", "embedding": [0.9,0.1,0.1,0.2]},
    {"id": "2", "titulo": "¿Qué es Milvus?", "contenido": "Milvus es un motor vectorial open source.", "categoria": "Milvus", "embedding": [0.8,0.2,0.9,0.1]},
    {"id": "3", "titulo": "FastAPI para APIs REST", "contenido": "FastAPI permite crear APIs rápidas y documentadas.", "categoria": "FastAPI", "embedding": [0.1,0.9,0.2,0.8]},
    {"id": "4", "titulo": "Swagger y documentación", "contenido": "Swagger genera documentación interactiva.", "categoria": "Swagger", "embedding": [0.2,0.8,0.1,0.9]}
]

ids = [d["id"] for d in example_docs]
col.delete(f"id in {ids}")
col.flush()

insert_data = [
    [d["id"] for d in example_docs],
    [d["titulo"] for d in example_docs],
    [d["contenido"] for d in example_docs],
    [d["categoria"] for d in example_docs],
    [d["embedding"] for d in example_docs]
]
col.insert(insert_data)
col.flush()
print_docs("Documentos insertados")

# 2. Consulta por id
print("\nConsulta por id='2':")
print(col.query("id == '2'", output_fields=["id", "titulo", "contenido", "categoria", "embedding"]))

# 3. Búsqueda vectorial
print("\nBúsqueda vectorial por similitud:")
search_params = {"metric_type": "L2", "params": {"ef": 32}}
results = col.search(
    data=[[0.8,0.2,0.9,0.1]],
    anns_field="embedding",
    param=search_params,
    limit=2,
    output_fields=["id", "titulo", "contenido", "categoria", "embedding"]
)
for hits in results:
    for hit in hits:
        print(hit.entity)

# 4. Eliminar un registro
print("\nEliminando id='3'")
col.delete("id == '3'")
col.flush()
print_docs("Después de eliminar id=3")
