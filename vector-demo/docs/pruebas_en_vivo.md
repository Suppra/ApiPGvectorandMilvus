# Pruebas en vivo para la exposición

## 1. Abrir Docker Desktop y verificar que esté corriendo.

## 2. Levantar los motores
- En terminal:
  ```bash
  docker-compose -f docker-compose.pgvector.yml up -d
  docker-compose -f docker-compose.milvus.yml up -d
  ```
- Verifica con `docker ps` que ambos estén activos.

## 3. Inicializar datos de ejemplo
- Para pgvector:
  ```bash
  psql -h localhost -U postgres -d vectordb -f scripts/seed_pgvector.sql
  ```
- Para Milvus:
  ```bash
  python scripts/milvus_test.py
  ```

## 4. Correr la API
- Ejecuta:
  ```bash
  uvicorn app.main:app --reload
  ```
- Abre [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 5. Probar endpoints en Swagger
- POST /pgvector/documentos
- GET /pgvector/documentos
- POST /pgvector/search
- POST /milvus/documentos
- GET /milvus/documentos
- POST /milvus/search

## 6. Consultas directas en psql (pgvector)
- Ver todos los registros:
  ```sql
  SELECT * FROM documentos;
  ```
- Buscar por similitud:
  ```sql
  SELECT *, embedding <-> '[0.8,0.2,0.9,0.1]' AS distancia FROM documentos ORDER BY distancia LIMIT 2;
  ```

## 7. Script de Milvus en vivo
- Ejecuta:
  ```bash
  python scripts/milvus_test.py
  ```
- Observa la salida en consola: inserción, consulta, búsqueda vectorial y eliminación.

## 8. Checklist final
- [ ] Docker corriendo
- [ ] Motores activos
- [ ] Datos cargados
- [ ] API y Swagger funcionando
- [ ] Pruebas ejecutadas sin error
