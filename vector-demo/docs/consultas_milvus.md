# Consultas manuales en Milvus (Python)

Milvus no tiene consola SQL, pero puedes interactuar directamente con el motor usando scripts en Python con pymilvus.

---

## Script de ejemplo para pruebas en vivo

El archivo `scripts/milvus_test.py` contiene ejemplos de:
- Creación de colección
- Inserción de datos
- Consulta por id
- Búsqueda vectorial
- Eliminación de un registro
- Listado de datos

Puedes ejecutar y modificar el script para probar otros casos o mostrarlo en vivo durante la exposición:

```bash
python scripts/milvus_test.py
```

---

## ¿Qué muestra este script?
- Inserta documentos de ejemplo
- Consulta por id
- Realiza una búsqueda vectorial por similitud
- Elimina un documento
- Lista todos los documentos
