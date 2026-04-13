-- Crear extensión vector
CREATE EXTENSION IF NOT EXISTS vector;

-- Crear tabla documentos
CREATE TABLE IF NOT EXISTS documentos (
    id VARCHAR PRIMARY KEY,
    titulo VARCHAR NOT NULL,
    contenido TEXT NOT NULL,
    categoria VARCHAR NOT NULL,
    embedding VECTOR(4) NOT NULL
);

-- Insertar datos de ejemplo
INSERT INTO documentos (id, titulo, contenido, categoria, embedding) VALUES
('1', 'Introducción a PostgreSQL', 'PostgreSQL es una base de datos relacional avanzada.', 'PostgreSQL', '[0.9,0.1,0.1,0.2]'),
('2', '¿Qué es Milvus?', 'Milvus es un motor vectorial open source.', 'Milvus', '[0.8,0.2,0.9,0.1]'),
('3', 'FastAPI para APIs REST', 'FastAPI permite crear APIs rápidas y documentadas.', 'FastAPI', '[0.1,0.9,0.2,0.8]'),
('4', 'Swagger y documentación', 'Swagger genera documentación interactiva.', 'Swagger', '[0.2,0.8,0.1,0.9]');
