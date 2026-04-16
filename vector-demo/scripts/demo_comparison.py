"""
DEMO COMPARACIÓN EN VIVO: PGVector vs Milvus
Ejecuta: python scripts/demo_comparison.py
"""
import os
import sys
import time
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

API_BASE = "http://127.0.0.1:8000"

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}{Colors.ENDC}\n")

def print_section(text):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}► {text}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def check_api():
    """Verifica que la API esté corriendo"""
    print_section("Verificando conexión a la API...")
    try:
        response = requests.get(f"{API_BASE}/docs", timeout=2)
        print_success("API en línea en http://127.0.0.1:8000")
        return True
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar a la API. ¿La iniciaste con: uvicorn app.main:app --reload?")
        return False

def create_test_documents():
    """Crea documentos de prueba"""
    print_section("Creando documentos de prueba...")
    
    test_data = [
        {
            "id": "doc_001",
            "titulo": "Introducción a Machine Learning",
            "contenido": "Machine Learning es una rama de la inteligencia artificial que permite a las máquinas aprender de datos.",
            "categoria": "AI",
            "embedding": [0.9, 0.1, 0.2, 0.3]
        },
        {
            "id": "doc_002",
            "titulo": "Redes Neuronales Profundas",
            "contenido": "Las redes neuronales profundas son modelos inspirados en el cerebro humano.",
            "categoria": "AI",
            "embedding": [0.85, 0.15, 0.25, 0.35]
        },
        {
            "id": "doc_003",
            "titulo": "Procesamiento de Lenguaje Natural",
            "contenido": "NLP es una técnica para procesar y entender texto en lenguaje humano.",
            "categoria": "AI",
            "embedding": [0.8, 0.2, 0.3, 0.4]
        },
        {
            "id": "doc_004",
            "titulo": "Visión por Computadora",
            "contenido": "Computer Vision permite a las máquinas interpretar imágenes y videos.",
            "categoria": "AI",
            "embedding": [0.75, 0.25, 0.35, 0.45]
        },
        {
            "id": "doc_005",
            "titulo": "Bases de Datos Vectoriales",
            "contenido": "Las bases de datos vectoriales almacenan embeddings para búsqueda por similitud.",
            "categoria": "Databases",
            "embedding": [0.2, 0.8, 0.7, 0.1]
        },
    ]
    
    for mottor in ["pgvector", "milvus"]:
        print_info(f"Creando documentos en {mottor.upper()}...")
        for doc in test_data:
            try:
                response = requests.post(
                    f"{API_BASE}/{mottor}/documentos",
                    json=doc,
                    timeout=5
                )
                if response.status_code == 200:
                    print_success(f"  {mottor}: {doc['id']} creado")
                else:
                    print_error(f"  {mottor}: Error creando {doc['id']}")
            except Exception as e:
                print_error(f"  {mottor}: {str(e)}")
    
    print_success("Documentos de prueba creados en ambos motores")

def list_documents():
    """Lista todos los documentos"""
    print_section("Listando documentos en ambos motores...")
    
    for motor in ["pgvector", "milvus"]:
        print_info(f"\n{Colors.BOLD}{motor.upper()}{Colors.ENDC}")
        try:
            response = requests.get(f"{API_BASE}/{motor}/documentos", timeout=5)
            if response.status_code == 200:
                docs = response.json()
                print_success(f"Total: {len(docs)} documentos")
                for doc in docs:
                    print(f"  • {doc['id']}: {doc['titulo']}")
            else:
                print_error(f"Error obteniendo documentos: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")

def search_comparison(query_embedding: List[float], category: str = None, top_k: int = 3):
    """Busca en ambos motores y compara resultados"""
    print_section(f"Búsqueda vectorial - Categoria: {category or 'Todas'}, Top-k: {top_k}")
    
    search_payload = {
        "embedding": query_embedding,
        "top_k": top_k
    }
    if category:
        search_payload["categoria"] = category
    
    results = {}
    
    for motor in ["pgvector", "milvus"]:
        print_info(f"\nBuscando en {motor.upper()}...")
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_BASE}/{motor}/search",
                json=search_payload,
                timeout=5
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                docs = response.json()
                results[motor] = {"docs": docs, "time": elapsed, "success": True}
                print_success(f"Encontrados {len(docs)} documentos en {elapsed:.4f}s")
                for i, doc in enumerate(docs, 1):
                    print(f"  {i}. {doc['titulo']}")
                    print(f"     ID: {doc['id']} | Categoría: {doc['categoria']}")
            else:
                print_error(f"Error: {response.status_code}")
                results[motor] = {"success": False, "error": response.status_code}
        except Exception as e:
            print_error(f"Error: {str(e)}")
            results[motor] = {"success": False, "error": str(e)}
    
    # Comparación
    print_section("Comparación de resultados")
    if results["pgvector"].get("success") and results["milvus"].get("success"):
        pgvector_time = results["pgvector"]["time"]
        milvus_time = results["milvus"]["time"]
        
        print_info(f"Tiempo PGVector: {pgvector_time:.4f}s")
        print_info(f"Tiempo Milvus: {milvus_time:.4f}s")
        
        if pgvector_time < milvus_time:
            diff = ((milvus_time - pgvector_time) / pgvector_time) * 100
            print_success(f"PGVector fue {diff:.1f}% más rápido")
        else:
            diff = ((pgvector_time - milvus_time) / milvus_time) * 100
            print_success(f"Milvus fue {diff:.1f}% más rápido")
        
        # Comparar IDs de documentos encontrados
        pgvector_ids = [doc['id'] for doc in results["pgvector"]["docs"]]
        milvus_ids = [doc['id'] for doc in results["milvus"]["docs"]]
        
        if pgvector_ids == milvus_ids:
            print_success("✓ Ambos motores encontraron los mismos documentos")
        else:
            print_info("Los motores encontraron documentos distintos (esperado con embeddings pequeños)")

def update_document(motor: str, doc_id: str):
    """Actualiza un documento"""
    print_section(f"Actualizando documento {doc_id} en {motor.upper()}...")
    
    update_data = {
        "titulo": f"[ACTUALIZADO] {doc_id}",
        "contenido": "Este documento ha sido actualizado para la demo"
    }
    
    try:
        response = requests.put(
            f"{API_BASE}/{motor}/documentos/{doc_id}",
            json=update_data,
            timeout=5
        )
        if response.status_code == 200:
            print_success("Documento actualizado")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def delete_document(motor: str, doc_id: str):
    """Elimina un documento"""
    print_section(f"Eliminando documento {doc_id} de {motor.upper()}...")
    
    try:
        response = requests.delete(
            f"{API_BASE}/{motor}/documentos/{doc_id}",
            timeout=5
        )
        if response.status_code == 200:
            print_success("Documento eliminado")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def run_demo():
    """Ejecuta la demostración completa"""
    print_header("🚀 DEMO: Comparación PGVector vs Milvus")
    
    # Verificar API
    if not check_api():
        print_error("\nNo se puede continuar sin la API en línea")
        sys.exit(1)
    
    # Menú interactivo
    while True:
        print_header("Menú de Demostración")
        print(f"{Colors.OKBLUE}1{Colors.ENDC} - Crear documentos de prueba")
        print(f"{Colors.OKBLUE}2{Colors.ENDC} - Listar documentos")
        print(f"{Colors.OKBLUE}3{Colors.ENDC} - Búsqueda en categoría 'AI'")
        print(f"{Colors.OKBLUE}4{Colors.ENDC} - Búsqueda en categoría 'Databases'")
        print(f"{Colors.OKBLUE}5{Colors.ENDC} - Búsqueda personalizada")
        print(f"{Colors.OKBLUE}6{Colors.ENDC} - Actualizar documento")
        print(f"{Colors.OKBLUE}7{Colors.ENDC} - Eliminar documento")
        print(f"{Colors.OKBLUE}0{Colors.ENDC} - Salir")
        
        choice = input(f"\n{Colors.BOLD}Selecciona opción: {Colors.ENDC}").strip()
        
        if choice == "1":
            create_test_documents()
        elif choice == "2":
            list_documents()
        elif choice == "3":
            search_comparison([0.9, 0.1, 0.2, 0.3], category="AI", top_k=3)
        elif choice == "4":
            search_comparison([0.2, 0.8, 0.7, 0.1], category="Databases", top_k=3)
        elif choice == "5":
            print_section("Búsqueda personalizada")
            try:
                emb = input("Ingresa embedding (4 números separados por comas): ").strip()
                embedding = list(map(float, emb.split(",")))
                if len(embedding) != 4:
                    print_error("El embedding debe tener exactamente 4 valores")
                    continue
                top_k = int(input("Top-k (default 3): ") or "3")
                search_comparison(embedding, top_k=top_k)
            except ValueError:
                print_error("Entrada inválida")
        elif choice == "6":
            motor = input("Motor (pgvector/milvus): ").strip()
            doc_id = input("ID del documento: ").strip()
            update_document(motor, doc_id)
        elif choice == "7":
            motor = input("Motor (pgvector/milvus): ").strip()
            doc_id = input("ID del documento: ").strip()
            delete_document(motor, doc_id)
        elif choice == "0":
            print_success("¡Hasta luego!")
            break
        else:
            print_error("Opción inválida")

if __name__ == "__main__":
    run_demo()
