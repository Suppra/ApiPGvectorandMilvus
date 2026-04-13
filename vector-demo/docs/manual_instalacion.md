# Manual de instalación paso a paso

## 1. Instalar Docker Desktop
- Descarga Docker Desktop desde https://www.docker.com/products/docker-desktop
- Instálalo y reinicia tu PC si es necesario.
- Abre Docker Desktop y asegúrate de que esté corriendo.

## 2. Verificar Docker
- Abre una terminal y ejecuta:
  ```bash
  docker --version
  docker compose version
  ```
- Debes ver la versión instalada, sin errores.

## 3. Instalar Python 3.11
- Descarga Python 3.11 desde https://www.python.org/downloads/release/python-3110/
- Durante la instalación, marca "Add Python to PATH".
- Verifica en terminal:
  ```bash
  python --version
  ```
- Debe mostrar Python 3.11.x

## 4. Clonar o copiar el proyecto
- Descarga o clona el repositorio en tu carpeta de trabajo.

## 5. Configurar variables de entorno
- Copia `.env.example` a `.env`:
  ```bash
  cp .env.example .env
  ```
- Puedes editar `.env` si necesitas cambiar puertos o credenciales.

## 6. Instalar dependencias Python
- En la terminal, ejecuta:
  ```bash
  pip install -r requirements.txt
  ```

## 7. Levantar PostgreSQL + pgvector
- Ejecuta:
  ```bash
  docker-compose -f docker-compose.pgvector.yml up -d
  ```
- Espera unos segundos y verifica con:
  ```bash
  docker ps
  ```
- Debes ver el contenedor `pgvector` corriendo.

## 8. Levantar Milvus
- Ejecuta:
  ```bash
  docker-compose -f docker-compose.milvus.yml up -d
  ```
- Verifica con:
  ```bash
  docker ps
  ```
- Debes ver el contenedor `milvus` corriendo.

## 9. Inicializar datos de ejemplo
- Para pgvector:
  ```bash
  psql -h localhost -U postgres -d vectordb -f scripts/seed_pgvector.sql
  ```
  (La contraseña es `postgres` por defecto)
- Para Milvus:
  ```bash
  python scripts/milvus_test.py
  ```

## 10. Correr la API
- Ejecuta:
  ```bash
  uvicorn app.main:app --reload
  ```
- Abre [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) en tu navegador para ver Swagger.

## 11. Probar funcionamiento
- Usa Swagger o Postman para probar los endpoints.
- Consulta los archivos en `docs/` para ejemplos y pruebas en vivo.
