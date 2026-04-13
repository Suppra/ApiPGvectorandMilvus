# Exposición Completa: Comparativa pgvector vs Milvus

## 1. Introducción

Este proyecto académico compara dos motores vectoriales de última generación:
- **pgvector**: extensión para PostgreSQL que permite búsquedas vectoriales en bases relacionales.
- **Milvus**: motor especializado, escalable y rápido para búsquedas vectoriales a gran escala.

Incluye backend FastAPI, API REST CRUD, documentación Swagger, scripts de prueba y todo listo para exposición y demo en clase.

---

## 2. Instalación y levantamiento rápido (Docker)

### Requisitos previos
- Docker Desktop instalado y corriendo ([descargar](https://www.docker.com/products/docker-desktop))
- Python 3.11 ([descargar](https://www.python.org/downloads/release/python-3110/))

### Clonar el proyecto
```bash
git clone https://github.com/Suppra/ApiPGvectorandMilvus.git
cd ApiPGvectorandMilvus/vector-demo
```

### Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env si necesitas cambiar puertos o credenciales
```

### Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### Levantar PostgreSQL + pgvector
```bash
docker-compose -f docker-compose.pgvector.yml up -d
docker ps  # Verifica que el contenedor 'pgvector' esté corriendo
```

### Levantar Milvus
```bash
docker-compose -f docker-compose.milvus.yml up -d
docker ps  # Verifica que el contenedor 'milvus' esté corriendo
```

---

## 3. Carga de datos de ejemplo

### PostgreSQL (pgvector)
```bash
psql -h localhost -U postgres -d vectordb -f scripts/seed_pgvector.sql
```

### Milvus
```bash
cd vector-demo
python scripts/milvus_test.py
```

---

## 4. Levantar la API y abrir Swagger

### Iniciar la API FastAPI
```bash
uvicorn app.main:app --reload
```

### Abrir la documentación interactiva
Abre [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) en tu navegador.

- Prueba los endpoints CRUD y de búsqueda vectorial para ambos motores:
  - `/pgvector/documentos`, `/pgvector/search`
  - `/milvus/documentos`, `/milvus/search`

---

## 5. Pruebas en vivo y consultas directas

### Consultas SQL en pgvector
- Ver todos los registros:
  ```sql
  SELECT * FROM documentos;
  ```
- Buscar por similitud:
  ```sql
  SELECT *, embedding <-> '[0.8,0.2,0.9,0.1]' AS distancia FROM documentos ORDER BY distancia LIMIT 2;
  ```
- Insertar manualmente:
  ```sql
  INSERT INTO documentos (id, titulo, contenido, categoria, embedding) VALUES ('5', 'API REST con FastAPI', 'FastAPI permite crear APIs rápidas.', 'FastAPI', '[0.5,0.5,0.5,0.5]');
  ```

### Pruebas en Milvus (Python)


#### Pruebas manuales con Milvus paso a paso

Puedes interactuar con Milvus desde Python de forma manual, ideal para la exposición. Sigue estos pasos exactamente:

1. **Abre una terminal y entra a la carpeta del proyecto:**
   ```bash
   cd vector-demo
   ```

2. **Inicia el intérprete interactivo de Python:**
   ```bash
   python
   ```

3. **(¡IMPORTANTE!) Antes de cualquier consulta, debes importar y conectar:**
   ```python
   from pymilvus import connections, Collection
   connections.connect(host="localhost", port="19530")
   col = Collection("documentos_milvus_api")
   ```
   - Si olvidas esto, cualquier comando que use `col` dará error "name 'col' is not defined".

4. **Listar todos los documentos:**
   ```python
   docs = col.query("id != ''", output_fields=["id", "titulo", "contenido", "categoria", "embedding"])
   for d in docs:
     print(d)
   ```

5. **Buscar por similitud vectorial:**
   ```python
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
   ```

6. **Insertar un documento nuevo:**
   ```python
   col.insert([
     ["5"],
     ["API REST con FastAPI"],
     ["FastAPI permite crear APIs rápidas."],
     ["FastAPI"],
     [[0.5,0.5,0.5,0.5]]
   ])
   col.flush()
   ```

7. **Eliminar un documento:**
   ```python
   col.delete("id == '5'")
   col.flush()
   ```

---
**Tips y advertencias:**
- Siempre ejecuta primero la conexión y la creación de la colección (`col = Collection(...)`).
- Si cierras el intérprete o abres uno nuevo, repite el paso 3 antes de cualquier consulta.
- Si ves errores como `name 'col' is not defined`, es porque olvidaste definir la colección.
- Puedes repetir los pasos 4-7 cuantas veces quieras para mostrar búsquedas, inserciones y eliminaciones en vivo.

Esto te permite demostrar el uso de Milvus de forma clara y sin errores en la exposición.

---

## 6. Comparativa rápida: ¿cuándo usar cada motor?

| Característica         | pgvector (PostgreSQL)         | Milvus                      |
|-----------------------|-------------------------------|-----------------------------|
| Integración           | Muy fácil si ya usas Postgres | Independiente, requiere más servicios |
| Escalabilidad         | Limitada por Postgres         | Altamente escalable         |
| Rendimiento           | Bueno para volúmenes medianos | Óptimo para millones de vectores |
| Consultas SQL         | Sí                            | No (solo Python API)        |
| Ideal para            | Añadir IA a sistemas existentes| Grandes sistemas de IA      |

---

## 7. Checklist para la demo
- [ ] Docker Desktop corriendo
- [ ] Contenedores de pgvector y Milvus activos
- [ ] Dependencias Python instaladas
- [ ] `.env` configurado
- [ ] Datos de ejemplo cargados
- [ ] API corriendo y Swagger accesible
- [ ] Pruebas ejecutadas sin error

---

## 8. Tips y cierre
- Si algo falla, revisa versiones de Python y dependencias.
- Usa siempre Python 3.11, no 3.13.
- Puedes mostrar consultas directas y resultados en Swagger en vivo.
- El proyecto está listo para clonar, levantar y exponer en minutos.

¡Éxito en tu exposición!
