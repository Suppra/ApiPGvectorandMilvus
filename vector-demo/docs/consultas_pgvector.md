# Consultas manuales en pgvector (PostgreSQL)

## 1. Ver todos los registros
```sql
SELECT * FROM documentos;
```

## 2. Insertar un documento manualmente
```sql
INSERT INTO documentos (id, titulo, contenido, categoria, embedding) VALUES
('5', 'API REST con FastAPI', 'FastAPI permite crear APIs rápidas.', 'FastAPI', '[0.5,0.5,0.5,0.5]');
```

## 3. Buscar similitud con un vector
```sql
SELECT *, embedding <-> '[0.8,0.2,0.9,0.1]' AS distancia FROM documentos ORDER BY distancia LIMIT 2;
```

## 4. Actualizar un embedding
```sql
UPDATE documentos SET embedding = '[0.1,0.1,0.1,0.1]' WHERE id = '5';
```

## 5. Crear un índice HNSW
```sql
CREATE INDEX ON documentos USING hnsw (embedding vector_l2_ops);
```

## 6. Filtrar por categoría y ordenar por similitud
```sql
SELECT *, embedding <-> '[0.8,0.2,0.9,0.1]' AS distancia FROM documentos WHERE categoria = 'Milvus' ORDER BY distancia LIMIT 2;
```
