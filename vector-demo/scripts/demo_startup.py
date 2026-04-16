"""
VERIFICACIÓN DE STARTUP
Ejecuta: python scripts/demo_startup.py
Verifica que todo esté listo para la exposición
"""
import os
import time
import docker
import requests
from dotenv import load_dotenv
from pymilvus import connections
from sqlalchemy import create_engine, text
import sys

load_dotenv()

class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check_docker():
    """Verifica que Docker esté corriendo"""
    print(f"\n{Colors.BOLD}1. Verificando Docker...{Colors.ENDC}")
    try:
        client = docker.from_env()
        client.ping()
        print(f"{Colors.OKGREEN}✓ Docker en línea{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ Docker no disponible: {str(e)}{Colors.ENDC}")
        return False

def check_containers():
    """Verifica que los contenedores estén corriendo"""
    print(f"\n{Colors.BOLD}2. Verificando contenedores...{Colors.ENDC}")
    try:
        client = docker.from_env()
        containers = client.containers.list()
        
        pgvector_running = any(cont.name == "pgvector" for cont in containers)
        milvus_running = any(cont.name == "milvus" for cont in containers)
        
        if pgvector_running:
            print(f"{Colors.OKGREEN}✓ Contenedor pgvector en línea{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ Contenedor pgvector NO está corriendo{Colors.ENDC}")
            print(f"   Inicia con: docker-compose -f docker-compose.pgvector.yml up -d")
        
        if milvus_running:
            print(f"{Colors.OKGREEN}✓ Contenedor milvus en línea{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ Contenedor milvus NO está corriendo{Colors.ENDC}")
            print(f"   Inicia con: docker-compose -f docker-compose.milvus.yml up -d")
        
        return pgvector_running and milvus_running
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error verificando contenedores: {str(e)}{Colors.ENDC}")
        return False

def check_postgres():
    """Verifica conexión a PostgreSQL"""
    print(f"\n{Colors.BOLD}3. Verificando PostgreSQL...{Colors.ENDC}")
    try:
        db_url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"{Colors.OKGREEN}✓ PostgreSQL conectado{Colors.ENDC}")
            
            # Verificar tabla de documentos
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM documentos"))
                count = result.scalar()
                print(f"{Colors.OKBLUE}  → Tabla 'documentos': {count} registros{Colors.ENDC}")
            except:
                print(f"{Colors.FAIL}  ✗ Tabla 'documentos' no existe o está vacía{Colors.ENDC}")
                return False
        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error conectando a PostgreSQL: {str(e)}{Colors.ENDC}")
        return False

def check_milvus():
    """Verifica conexión a Milvus"""
    print(f"\n{Colors.BOLD}4. Verificando Milvus...{Colors.ENDC}")
    try:
        host = os.getenv("MILVUS_HOST", "localhost")
        port = int(os.getenv("MILVUS_PORT", "19530"))
        
        connections.connect(host=host, port=port, pool_size=1)
        print(f"{Colors.OKGREEN}✓ Milvus conectado{Colors.ENDC}")
        
        from pymilvus import utility
        collections = utility.list_collections()
        print(f"{Colors.OKBLUE}  → Colecciones: {len(collections)}{Colors.ENDC}")
        for col in collections:
            print(f"    • {col}")
        
        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error conectando a Milvus: {str(e)}{Colors.ENDC}")
        return False

def check_api():
    """Verifica que la API esté corriendo"""
    print(f"\n{Colors.BOLD}5. Verificando API FastAPI...{Colors.ENDC}")
    try:
        response = requests.get("http://127.0.0.1:8000/docs", timeout=2)
        if response.status_code == 200:
            print(f"{Colors.OKGREEN}✓ API en línea (http://127.0.0.1:8000){Colors.ENDC}")
            return True
        else:
            print(f"{Colors.FAIL}✗ API responde con error: {response.status_code}{Colors.ENDC}")
            return False
    except Exception as e:
        print(f"{Colors.FAIL}✗ API no disponible: {str(e)}{Colors.ENDC}")
        print(f"   Inicia con: uvicorn app.main:app --reload")
        return False

def check_dependencies():
    """Verifica dependencias Python"""
    print(f"\n{Colors.BOLD}6. Verificando dependencias Python...{Colors.ENDC}")
    required = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2",
        "pgvector",
        "pymilvus",
        "dotenv",
        "requests"
    ]
    
    all_ok = True
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
            print(f"{Colors.OKGREEN}✓ {pkg}{Colors.ENDC}")
        except ImportError:
            print(f"{Colors.FAIL}✗ {pkg} no instalado{Colors.ENDC}")
            all_ok = False
    
    return all_ok

def main():
    """Ejecuta todas las verificaciones"""
    print(f"\n{Colors.BOLD}{'='*60}")
    print("VERIFICACIÓN DE STARTUP - EXPOSICIÓN UNIVERSITARIA")
    print(f"{'='*60}{Colors.ENDC}")
    
    checks = [
        ("Docker", check_docker),
        ("Contenedores", check_containers),
        ("PostgreSQL+pgvector", check_postgres),
        ("Milvus", check_milvus),
        ("API FastAPI", check_api),
        ("Dependencias Python", check_dependencies),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
            time.sleep(0.5)
        except Exception as e:
            print(f"{Colors.FAIL}✗ Error en {name}: {str(e)}{Colors.ENDC}")
            results[name] = False
    
    # Resumen
    print(f"\n{Colors.BOLD}{'='*60}")
    print("RESUMEN")
    print(f"{'='*60}{Colors.ENDC}")
    
    all_ok = all(results.values())
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, result in results.items():
        status = f"{Colors.OKGREEN}✓{Colors.ENDC}" if result else f"{Colors.FAIL}✗{Colors.ENDC}"
        print(f"{status} {name}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} verificaciones pasadas{Colors.ENDC}")
    
    if all_ok:
        print(f"\n{Colors.OKGREEN}{'='*60}")
        print("¡LISTO PARA LA EXPOSICIÓN!")
        print(f"{'='*60}{Colors.ENDC}")
        print(f"\nPara iniciar la demostración:")
        print(f"  1. API: uvicorn app.main:app --reload")
        print(f"  2. Demo: python scripts/demo_comparison.py")
        print(f"\nAccede a Swagger: http://127.0.0.1:8000/docs")
        return 0
    else:
        print(f"\n{Colors.FAIL}{'='*60}")
        print("FALTAN AJUSTES ANTES DE LA EXPOSICIÓN")
        print(f"{'='*60}{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
