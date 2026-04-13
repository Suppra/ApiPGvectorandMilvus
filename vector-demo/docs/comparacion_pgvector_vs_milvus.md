# Comparación: pgvector vs Milvus

## ¿Qué es cada uno?
- **pgvector**: extensión para PostgreSQL que permite almacenar y buscar vectores en una base relacional.
- **Milvus**: motor vectorial especializado, diseñado para búsquedas vectoriales a gran escala.

## Ventajas de pgvector
- Fácil de integrar en proyectos que ya usan PostgreSQL.
- Permite combinar SQL tradicional con búsquedas vectoriales.
- Menor curva de aprendizaje si ya conoces SQL.

## Ventajas de Milvus
- Altamente escalable y rápido para grandes volúmenes de datos vectoriales.
- Soporta índices avanzados y optimizados para IA.
- Arquitectura distribuida y orientada a big data.

## Diferencias de arquitectura
- pgvector es una extensión, Milvus es un motor independiente.
- Milvus requiere servicios adicionales (etcd, minio), pgvector solo PostgreSQL.
- Milvus está optimizado para búsquedas vectoriales, pgvector es más generalista.

## ¿Cuándo conviene uno u otro?
- Usa pgvector si ya tienes PostgreSQL y buscas añadir IA de forma sencilla.
- Usa Milvus si necesitas rendimiento, escalabilidad y buscas trabajar con millones de vectores.

## ¿Qué se demuestra en este proyecto?
- Cómo exponer y comparar ambos motores en un entorno real.
- Ventajas y limitaciones de cada uno.
- Ejemplos prácticos y pruebas en vivo para exposición académica.
