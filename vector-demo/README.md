# vector-demo

Proyecto académico para comparar dos motores vectoriales: **pgvector** (PostgreSQL) y **Milvus**. Incluye instalación, API REST CRUD con FastAPI, documentación Swagger, consultas directas y scripts de prueba para exposición universitaria.

## Objetivos

- Demostrar instalación y uso de pgvector y Milvus en local.
- Exponer una API REST CRUD y búsqueda vectorial para ambos motores.
- Documentar y facilitar pruebas en vivo y comparación.

## Tecnologías

- Python 3.11
- FastAPI
- SQLAlchemy
- pgvector
- pymilvus
- Docker y Docker Compose

## Estructura

- `app/`: Backend FastAPI y lógica de negocio.
- `scripts/`: SQL y scripts de prueba para ambos motores.
- `docs/`: Manuales, guion, pruebas, comparativas y consultas directas.
- `.env.example`: Variables de entorno.
- `requirements.txt`: Dependencias Python.
- `docker-compose.pgvector.yml`: PostgreSQL + pgvector.
- `docker-compose.milvus.yml`: Milvus standalone.

## Instalación rápida

1. Instala **Python 3.11** y **Docker Desktop**.
2. Copia `.env.example` a `.env` y ajusta si es necesario.
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Levanta PostgreSQL+pgvector:
   ```bash
   docker-compose -f docker-compose.pgvector.yml up -d
   ```
5. Levanta Milvus:
   ```bash
   docker-compose -f docker-compose.milvus.yml up -d
   ```
6. Inicializa datos de ejemplo:
   ```bash
   psql -h localhost -U postgres -d vectordb -f scripts/seed_pgvector.sql
   python scripts/milvus_test.py
   ```
7. Corre la API:
   ```bash
   uvicorn app.main:app --reload
   ```
8. Abre Swagger en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Errores comunes antes de exponer

- Usa **Python 3.11** (no 3.13).
- Verifica que los contenedores estén corriendo (`docker ps`).
- Si pymilvus falla, revisa la versión de Milvus y Python.
- Si no conecta a PostgreSQL, revisa variables de entorno y puertos.

## Checklist final antes de la demo

- [ ] Docker Desktop corriendo.
- [ ] Contenedores de pgvector y Milvus activos.
- [ ] Dependencias Python instaladas.
- [ ] `.env` configurado.
- [ ] Datos de ejemplo cargados.
- [ ] API corriendo y Swagger accesible.
- [ ] Scripts de prueba ejecutados sin error.

---

Para detalles, consulta los manuales en `docs/`.
