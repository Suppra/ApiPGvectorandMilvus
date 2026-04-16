# ⚡ INICIO RÁPIDO - 3 MINUTOS

Sigue estos pasos para iniciar demo:

## PASO 1: Verificar Sistema (1 minuto)

```bash
cd c:\Users\Crist\BDpgMilvus\vector-demo
python scripts/demo_startup.py
```

Espera a que todos los checks muestren ✓ verde

## PASO 2: Iniciar Contenedores (20 segundos)

**Opción A - Automático:**
```powershell
.\scripts\start_demo.ps1 -Containers
```

**Opción B - Manual:**
```bash
docker-compose -f docker-compose.pgvector.yml up -d
docker-compose -f docker-compose.milvus.yml up -d
# Espera 15-20 segundos
```

## PASO 3: Iniciar API (10 segundos)

```bash
uvicorn app.main:app --reload
```

Verifica que esté en: http://127.0.0.1:8000/docs

## PASO 4: DEMO EN VIVO (elige una)

### Opción A: Demo Interactiva (Recomendado)
```bash
python scripts/demo_comparison.py
```

### Opción B: Swagger UI (Más profesional)
Abre en navegador: http://127.0.0.1:8000/docs

### Opción C: Pruebas de Rendimiento
```bash
python scripts/performance_test.py
```

---

## 🎯 WHAT TO SHOW

### En Demo Interactiva:
1. Opción 1: Crear documentos
2. Opción 2: Listar documentos
3. Opción 3: Búsqueda en AI (compara tiempos)
4. Observa: "✓ Milvus fue X% más rápido"

### En Swagger:
1. POST /pgvector/documentos - Crear
2. POST /pgvector/search - Buscar
3. POST /milvus/documentos - Crear
4. POST /milvus/search - Buscar
5. Compara tiempos en "Response"

---

## 📞 Si Algo Falla

### PostgreSQL no responde
```bash
docker-compose -f docker-compose.pgvector.yml restart
```

### Milvus no responde
```bash
docker-compose -f docker-compose.milvus.yml restart
# Espera 20+ segundos
```

### API no funciona
```bash
# Termina proceso anterior (Ctrl+C)
uvicorn app.main:app --reload
```

---

## 📖 Para Más Detalles

- [Guía Completa](docs/GUIA_EXPOSICION.md)
- [Resumen Ejecutivo](docs/RESUMEN_EXPOSICION.md)

---

**¡Listo para la exposición!** 🚀
