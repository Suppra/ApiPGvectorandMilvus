# 📋 GUÍA DE EXPOSICIÓN - Comparativa PGVector vs Milvus

**Fecha**: April 15, 2026
**Proyecto**: API REST CRUD y búsqueda vectorial
**Tecnologías**: FastAPI, PostgreSQL+pgvector, Milvus

---

## 🎯 Objetivos de la Exposición

- Demostrar instalación y uso de dos motores vectoriales
- Comparar rendimiento: PGVector vs Milvus en tiempo real
- Exponer operaciones CRUD en ambos motores
- Realizar búsquedas vectoriales interactivas
- Mostrar Swagger UI con documentación en vivo

---

## ✅ CHECKLIST PRE-EXPOSICIÓN

### 1️⃣ Verificación del Sistema (5 minutos antes)

```bash
# En la carpeta vector-demo/
python scripts/demo_startup.py
```

Debería mostrar:
- ✓ Docker en línea
- ✓ Contenedores pgvector y milvus corriendo
- ✓ PostgreSQL conectado
- ✓ Milvus conectado
- ✓ API FastAPI disponible
- ✓ Dependencias Python instaladas

### 2️⃣ Iniciar Contenedores

**Opción 1 (PowerShell):**
```powershell
.\scripts\start_demo.ps1 -Containers
```

**Opción 2 (Manual):**
```bash
# Terminal 1: PostgreSQL + pgvector
docker-compose -f docker-compose.pgvector.yml up -d

# Terminal 2: Milvus
docker-compose -f docker-compose.milvus.yml up -d

# Esperar 15-20 segundos para que Milvus se inicialice
```

### 3️⃣ Iniciar Aplicación

```bash
# Terminal 3: API FastAPI (desde carpeta vector-demo)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Deberías ver:
```
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

### 4️⃣ Verificar Swagger

Abre en navegador:
```
http://127.0.0.1:8000/docs
```

Deberías ver la interfaz Swagger con dos secciones:
- **pgvector**: Documentos
- **milvus**: Documentos

---

## 🚀 DEMOSTRACIÓN INTERACTIVA

### OPCIÓN A: Script de Demo

```bash
python scripts/demo_comparison.py
```

Esto abre un menú interactivo donde puedes:
1. Crear documentos de prueba
2. Listar documentos
3. Realizar búsquedas por categoría
4. Comparar tiempos de respuesta
5. Actualizar/eliminar documentos

### OPCIÓN B: Swagger UI (Recomendado para exposición en vivo)

En Swagger acedes a: http://127.0.0.1:8000/docs

Pasos sugeridos:

#### 1. **Crear documentos** (Demostrar CRUD)

**PGVector:**
- Click en `POST /pgvector/documentos`
- Click en "Try it out"
- Ingresa JSON:
```json
{
  "id": "doc_demo_1",
  "titulo": "Introducción a Machine Learning",
  "contenido": "Machine Learning es una rama de la inteligencia artificial",
  "categoria": "AI",
  "embedding": [0.9, 0.1, 0.2, 0.3]
}
```
- Click "Execute"

**Milvus:**
- Repetir lo anterior pero en `/milvus/documentos`
- Observar que ambos responden exitosamente

#### 2. **Listar documentos**

**PGVector:**
- Click en `GET /pgvector/documentos`
- Click "Execute"

**Milvus:**
- Click en `GET /milvus/documentos`
- Click "Execute"

**Punto de discusión**: Ambos retornan los mismos datos

#### 3. **Búsqueda Vectorial** (Núcleo de la exposición)

Esto es lo más importante para comparar.

**PGVector:**
- Click en `POST /pgvector/search`
- "Try it out"
- Ingresa:
```json
{
  "embedding": [0.9, 0.1, 0.2, 0.3],
  "top_k": 3
}
```
- **Nota el tiempo de respuesta** (en Headers)

**Milvus:**
- Repite lo anterior en `/milvus/search`
- **Compara tiempos**

**Punto de discusión**: 
- Ambos usan métrica L2 (Euclidiana)
- Los tiempos pueden variar por cantidad de datos
- Con más documentos, Milvus tendría ventaja

#### 4. **Búsqueda con Filtro**

Demuestra que ambos permiten filtros por categoría:

```json
{
  "embedding": [0.9, 0.1, 0.2, 0.3],
  "categoria": "AI",
  "top_k": 3
}
```

#### 5. **Actualizar documento**

- Click en `PUT /pgvector/documentos/{id}`
- "Try it out"
- ID: "doc_demo_1"
- Ingresa:
```json
{
  "titulo": "[ACTUALIZADO] Introducción a Machine Learning"
}
```

#### 6. **Eliminar documento**

- Click en `DELETE /pgvector/documentos/{id}`
- ID: "doc_demo_1"
- Execute

---

## 📊 SCRIPT DE PRUEBAS DE RENDIMIENTO

Para mostrar análisis más profundo:

```bash
python scripts/performance_test.py
```

Opciones:
1. Crear 50 documentos en bulk en ambos motores
2. Realizar 10 búsquedas consecutivas y medir tiempos
3. Comparar resultados finales
4. Ejecutar todo automáticamente

**Métricas que se muestran:**
- Tasa de inserción (docs/segundo)
- Tiempo promedio de búsqueda
- Desviación estándar
- Tiempos mínimo y máximo
- Comparativa de rendimiento

---

## 💡 PUNTOS CLAVE PARA PRESENTAR

### PGVector (PostgreSQL)
```
✓ Ventajas:
  • Integración con base de datos relacional
  • ACID completo
  • Índices vectoriales avanzados
  • Consultas SQL complejas mezclando relacional + vectorial
  • Mejor para datos estructurados con búsqueda vectorial

✗ Limitaciones:
  • Menos especializado en búsqueda pura de vectores
  • Rendimiento inferior con millones de dimensiones
```

### Milvus
```
✓ Ventajas:
  • Especializado exclusivamente en búsqueda vectorial
  • Mejor rendimiento a escala
  • Soporte para índices avanzados (HNSW, IVF, etc.)
  • Escalable horizontalmente
  • Mejor para millones de vectores

✗ Limitaciones:
  • No es una base de datos relacional completa
  • Menos funcionalidades SQL
  • Requiere infraestructura adicional (etcd, MinIO)
```

---

## 🐛 TROUBLESHOOTING RÁPIDO

### "API no disponible"
```bash
# Terminal 3 - Reinicia API
uvicorn app.main:app --reload
```

### "No se puede conectar a PostgreSQL"
```bash
# Verifica contenedor
docker ps | grep pgvector

# Reinicia
docker-compose -f docker-compose.pgvector.yml restart
```

### "No se puede conectar a Milvus"
```bash
# Verifica contenedores
docker ps | grep milvus
docker ps | grep etcd
docker ps | grep minio

# Reinicia todos
docker-compose -f docker-compose.milvus.yml restart
```

### "timeout ejecutetd"
- Espera más tiempo (Milvus necesita 15-20s para inicializarse)
- Verifica que Milvus esté saludable: `docker logs milvus`

---

## 📑 ESTRUCTURA DE CARPETAS

```
vector-demo/
├── app/
│   ├── main.py                 # Aplicación FastAPI
│   ├── database.py             # Conexión a PostgreSQL
│   ├── schemas.py              # Modelos Pydantic
│   ├── routers/
│   │   ├── pgvector_router.py  # Endpoints PGVector
│   │   └── milvus_router.py    # Endpoints Milvus
│   └── services/
│       ├── pgvector_service.py # Lógica PGVector
│       └── milvus_service.py   # Lógica Milvus
├── scripts/
│   ├── demo_startup.py         # Verificación de startup ✨
│   ├── demo_comparison.py      # Demo interactiva ✨
│   ├── performance_test.py     # Pruebas de rendimiento ✨
│   ├── start_demo.ps1          # Script PowerShell ✨
│   ├── milvus_test.py          # Pruebas directas Milvus
│   └── seed_pgvector.sql       # Datos iniciales
├── docker-compose.pgvector.yml # PostgreSQL + pgvector
├── docker-compose.milvus.yml   # Milvus
├── .env                        # Variables de entorno
└── README.md                   # Este archivo

✨ = Scripts nuevos para la exposición
```

---

## 🎬 GUIÓN DE EXPOSICIÓN SUGERIDO

### MINUTO 0-2: Introducción
- Presentar el problema: búsqueda vectorial en bases de datos
- Mostrar dos soluciones: PGVector y Milvus

### MINUTO 2-5: Arquitectura
- Mostrar diagrama de arquitectura
- APIs separadas pero compatibles
- Stack: FastAPI, SQLAlchemy, Docker

### MINUTO 5-15: DEMO EN VIVO
1. **Swagger UI** - Mostrar documentación interactiva (2 min)
2. **Crear documentos** - CRUD en ambos (1 min)
3. **Búsqueda vectorial** - Comparar tiempos (2-3 min)
4. **Análisis de resultados** - Mostrar similitud (1 min)

### MINUTO 15-20: Análisis Técnico
- Diferencias en implementación
- Ventajas/desventajas de cada motor
- Casos de uso

### MINUTO 20-25: Q&A / Conclusiones

---

## 📞 CONTACTO & DOCUMENTACIÓN

Para más detalles:
- Proyecto: https://github.com/Suppra/ApiPGvectorandMilvus.git
- Documentación técnica en: `docs/`

---

## ✅ CHECKLIST FINAL

ANTES de iniciar la exposición:

- [ ] Docker Desktop está corriendo
- [ ] Contenedores inicializados (`docker ps` muestra pgvector y milvus)
- [ ] API FastAPI en línea (`http://127.0.0.1:8000/docs` accesible)
- [ ] Swagger carga correctamente
- [ ] He probado crear un documento
- [ ] He probado hacer una búsqueda
- [ ] He verificado tiempos de respuesta
- [ ] Tengo datos de prueba listos
- [ ] His reviewed demo_comparison.py
- [ ] Terminal lista para mostrar logs
- [ ] Navegador con Swagger abierto

---

**¡Buena suerte en tu exposición! 🚀**
