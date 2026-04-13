# Guion de exposición: Comparativa de Motores Vectoriales

## Introducción
- Buenas tardes, hoy vamos a exponer un proyecto académico sobre motores vectoriales.
- El objetivo es comparar dos tecnologías: **pgvector** (PostgreSQL) y **Milvus**.

## ¿Qué es pgvector?
- Es una extensión para PostgreSQL que permite almacenar y buscar vectores en una base de datos relacional.
- Ideal para añadir capacidades de IA y búsquedas vectoriales a sistemas tradicionales.

## ¿Qué es Milvus?
- Es un motor vectorial open source, diseñado específicamente para búsquedas vectoriales a gran escala.
- Muy usado en aplicaciones de IA, recomendadores y sistemas de búsqueda semántica.

## ¿Por qué usamos FastAPI?
- FastAPI es un framework moderno para crear APIs en Python, rápido y con documentación automática (Swagger).
- Permite exponer fácilmente operaciones CRUD y búsquedas vectoriales.

## Arquitectura del proyecto
- El backend está hecho en Python con FastAPI.
- Hay endpoints separados para pgvector y Milvus.
- Cada motor tiene su propio CRUD y búsqueda vectorial.
- Todo está documentado y listo para probar en Swagger.

## CRUD y búsqueda vectorial
- Se puede crear, leer, actualizar y borrar documentos en ambos motores.
- Además, se puede buscar por similitud vectorial usando embeddings de dimensión 4.
- Los endpoints están organizados y son fáciles de probar.

## Diferencias entre ambos motores
- pgvector es ideal para proyectos que ya usan PostgreSQL y quieren añadir IA.
- Milvus es más escalable y rápido para grandes volúmenes de datos vectoriales.
- Ambos tienen ventajas y desventajas según el caso de uso.

## Cierre y conclusiones
- El proyecto demuestra cómo integrar y comparar dos tecnologías de vanguardia.
- Está pensado para ser estable, fácil de exponer y reproducir en clase.
- ¡Gracias por su atención!
