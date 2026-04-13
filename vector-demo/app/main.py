import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import pgvector_router, milvus_router

load_dotenv()

app = FastAPI(
    title="Comparativa de Motores Vectoriales: pgvector vs Milvus",
    description="API REST CRUD y búsqueda vectorial sobre PostgreSQL+pgvector y Milvus. Proyecto académico.",
    version="1.0.0"
)

app.include_router(pgvector_router.router, prefix="/pgvector", tags=["pgvector"])
app.include_router(milvus_router.router, prefix="/milvus", tags=["milvus"])
