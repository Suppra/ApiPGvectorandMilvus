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

Puedes interactuar con Milvus desde Python de forma manual, ideal para la exposición. **No necesitas saber nada previo de Milvus ni de Python avanzado.**

Sigue estos pasos exactamente y lee las explicaciones de cada comando:

1. **Abre una terminal y entra a la carpeta del proyecto:**
  ```bash
  cd vector-demo
  ```
  Esto te asegura que estás en la carpeta donde está el código y los scripts.

2. **Inicia el intérprete interactivo de Python:**
  ```bash
  python
  ```
  Verás que el prompt cambia a `>>>`, lo que indica que puedes escribir código Python línea por línea.

3. **Conéctate a Milvus y accede a la colección:**
  ```python
  from pymilvus import connections, Collection  # Importa las funciones necesarias
  connections.connect(host="localhost", port="19530")  # Conecta con el servidor Milvus local
  col = Collection("documentos_milvus_api")  # Accede a la colección de documentos (como una tabla)
  ```
  - **¿Qué es `col`?** Es el objeto que representa tu colección de documentos en Milvus. Todas las operaciones (buscar, insertar, borrar) se hacen a través de él.
  - **IMPORTANTE:** Si olvidas este paso, cualquier comando que use `col` dará error "name 'col' is not defined".

4. **Listar todos los documentos (mostrar todo lo que hay en la colección):**
  ```python
  docs = col.query("id != ''", output_fields=["id", "titulo", "contenido", "categoria", "embedding"])
  for d in docs:
     print(d)
  ```
  - `col.query(...)` busca todos los documentos cuyo id no está vacío.
  - `output_fields` indica qué campos quieres ver (id, título, contenido, etc).
  - El bucle `for d in docs: print(d)` imprime cada documento encontrado.

5. **Buscar por similitud vectorial (encontrar los documentos más parecidos a un vector):**
  ```python
  search_params = {"metric_type": "L2", "params": {"ef": 32}}  # Configura el tipo de búsqueda
  results = col.search(
     data=[[0.8,0.2,0.9,0.1]],  # El vector de consulta (puedes cambiarlo)
     anns_field="embedding",  # El campo vectorial sobre el que buscar
     param=search_params,
     limit=2,  # Cuántos resultados quieres
     output_fields=["id", "titulo", "contenido", "categoria", "embedding"]
  )
  for hits in results:
     for hit in hits:
        print(hit.entity)  # Muestra cada documento similar encontrado
  ```
  - Esto busca los 2 documentos más parecidos al vector `[0.8,0.2,0.9,0.1]`.

6. **Insertar un documento nuevo (agregar un registro a la colección):**
  ```python
  col.insert([
     ["5"],  # id
     ["API REST con FastAPI"],  # título
     ["FastAPI permite crear APIs rápidas."],  # contenido
     ["FastAPI"],  # categoría
     [[0.5,0.5,0.5,0.5]]  # embedding (vector)
  ])
  col.flush()  # Guarda los cambios en la colección
  ```
  - Cada lista interna representa un campo. El embedding debe ser una lista de 4 números (como en los ejemplos).

7. **Eliminar un documento (borrar por id):**
  ```python
  col.delete("id == '5'")  # Elimina el documento cuyo id es '5'
  col.flush()  # Guarda los cambios
  ```

---
**Tips y advertencias para principiantes:**
- **Nunca pongas espacios al inicio de la línea** en el prompt de Python, excepto dentro de un bucle o función (por ejemplo, dentro de `for d in docs:` sí van 4 espacios antes de `print(d)`).
- Si cierras el intérprete o abres uno nuevo, repite el paso 3 antes de cualquier consulta.
- Si ves errores como `name 'col' is not defined`, es porque olvidaste definir la colección.
- Puedes repetir los pasos 4-7 cuantas veces quieras para mostrar búsquedas, inserciones y eliminaciones en vivo.
- Si tienes dudas, copia y pega los ejemplos tal cual, pero revisa que no haya espacios extra al inicio de las líneas.

Esto te permite demostrar el uso de Milvus de forma clara, didáctica y sin errores en la exposición, incluso si nunca has usado Milvus o Python interactivo antes.

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
