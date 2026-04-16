# vector-demo

Proyecto académico para comparar dos motores vectoriales: **pgvector** (PostgreSQL) y **Milvus**. Incluye instalación, API REST CRUD con FastAPI, documentación Swagger, consultas directas y scripts de prueba para exposición universitaria.

---

## 🚀 INICIO RÁPIDO - EXPOSICIÓN (3 MINUTOS)

```bash
# 1️⃣ Verificar que todo está listo (1 minuto)
python scripts/demo_startup.py

# 2️⃣ Iniciar contenedores (30 segundos)
docker-compose -f docker-compose.pgvector.yml up -d
docker-compose -f docker-compose.milvus.yml up -d

# 3️⃣ Iniciar API (20 segundos)
uvicorn app.main:app --reload

# 4️⃣ Abrir DEMO (elige una)
python scripts/demo_comparison.py      # 🎮 Demo interactiva (RECOMENDADO)
# O
# http://127.0.0.1:8000/docs           # 🌐 Swagger UI profesional
# O
# python scripts/performance_test.py   # 📊 Análisis de rendimiento
```

**Leer primero**: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

---

## 📚 Documentación para Exposición

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
6. Corre la API:
   ```bash
   uvicorn app.main:app --reload
   ```
7. Abre Swagger en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Scripts para la Exposición

### 🚀 Verificación rápida de startup
Antes de empezar la exposición, verifica que todo está listo:
```bash
python scripts/demo_startup.py
```
Muestra estado de Docker, contenedores, bases de datos y API.

### 🎮 Demo interactiva comparativa
Menú interactivo para comparar ambos motores en tiempo real:
```bash
python scripts/demo_comparison.py
```
Opciones:
- Crear documentos de prueba
- Listar documentos en ambos motores
- Realizar búsquedas vectoriales y comparar tiempos
- Actualizar/eliminar documentos
- Hacer búsquedas personalizadas

### 📊 Pruebas de rendimiento
Análisis profundo de rendimiento y escalabilidad:
```bash
python scripts/performance_test.py
```
Opciones:
- Crear 50+ documentos en bulk
- Realizar búsquedas consecutivas con métricas
- Comparar tiempos de respuesta
- Generar gráficos de rendimiento

### 🚀 Script PowerShell de inicio rápido (Windows)
```powershell
.\scripts\start_demo.ps1
```
Menú para iniciar contenedores, API y demo en mismo comando.

## 📋 Guía de Exposición

Para una presentación paso a paso, consulta:
[Guía completa de exposición](docs/GUIA_EXPOSICION.md)

Incluye:
- Checklist pre-exposición
- Instrucciones Swagger
- Guión sugerido (20 minutos)
- Troubleshooting rápido

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
