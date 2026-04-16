"""
PRUEBAS DE RENDIMIENTO Y ESCALABILIDAD
Compara PGVector vs Milvus con diferentes casos de uso
Ejecuta: python scripts/performance_test.py
"""

import os
import sys
import time
import requests
import statistics
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

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

def print_table(headers: List[str], rows: List[List]):
    """Imprime una tabla formateada"""
    # Calcular anchos de columna
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Imprimir header
    header_line = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
    print(f"\n{Colors.BOLD}{header_line}{Colors.ENDC}")
    print("-" * len(header_line))
    
    # Imprimir rows
    for row in rows:
        print(" | ".join(f"{str(r):<{w}}" for r, w in zip(row, col_widths)))

class PerformanceTest:
    def __init__(self):
        self.results = {"pgvector": {}, "milvus": {}}
    
    def test_api_connection(self):
        """Verifica conexión a la API"""
        print_section("Verificando conexión a API...")
        try:
            response = requests.get(f"{API_BASE}/docs", timeout=2)
            print_success("API disponible")
            return True
        except:
            print_error("API no disponible. ¿La iniciaste con: uvicorn app.main:app --reload?")
            return False
    
    def create_bulk_documents(self, motor: str, count: int = 50):
        """Crea múltiples documentos"""
        print_section(f"Creando {count} documentos en {motor.upper()}...")
        
        start_time = time.time()
        successful = 0
        
        for i in range(count):
            doc = {
                "id": f"{motor}_bulk_{i:04d}",
                "titulo": f"Documento {i}",
                "contenido": f"Este es el documento número {i} para pruebas de rendimiento.",
                "categoria": ["AI", "Databases", "API"][i % 3],
                "embedding": [
                    0.1 + (i % 10) * 0.08,
                    0.2 + (i % 7) * 0.1,
                    0.3 + (i % 5) * 0.12,
                    0.4 + (i % 3) * 0.15
                ]
            }
            
            try:
                response = requests.post(f"{API_BASE}/{motor}/documentos", json=doc, timeout=5)
                if response.status_code == 200:
                    successful += 1
            except:
                pass
            
            if (i + 1) % 10 == 0:
                print_info(f"  {i + 1}/{count} documentos creados")
        
        elapsed = time.time() - start_time
        rate = successful / elapsed if elapsed > 0 else 0
        
        print_success(f"Completado: {successful}/{count} en {elapsed:.2f}s ({rate:.1f} docs/s)")
        
        return {"count": successful, "time": elapsed, "rate": rate}
    
    def test_search_performance(self, motor: str, iterations: int = 10, top_k: int = 5):
        """Prueba rendimiento de búsqueda"""
        print_section(f"Prueba de búsqueda - {motor.upper()} ({iterations} iteraciones, top-k={top_k})")
        
        times = []
        
        for i in range(iterations):
            embedding = [
                0.1 + (i % 10) * 0.08,
                0.2 + (i % 7) * 0.1,
                0.3 + (i % 5) * 0.12,
                0.4 + (i % 3) * 0.15
            ]
            
            payload = {"embedding": embedding, "top_k": top_k}
            
            try:
                start_time = time.time()
                response = requests.post(f"{API_BASE}/{motor}/search", json=payload, timeout=10)
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    times.append(elapsed)
                    print_info(f"  Búsqueda {i+1}: {elapsed*1000:.2f}ms")
            except Exception as e:
                print_error(f"  Búsqueda {i+1}: Error - {str(e)}")
        
        if times:
            avg = statistics.mean(times)
            min_time = min(times)
            max_time = max(times)
            std_dev = statistics.stdev(times) if len(times) > 1 else 0
            
            print_success(f"Resultados:")
            print_info(f"  Promedio: {avg*1000:.2f}ms")
            print_info(f"  Mínimo: {min_time*1000:.2f}ms")
            print_info(f"  Máximo: {max_time*1000:.2f}ms")
            print_info(f"  Desv. Est: {std_dev*1000:.2f}ms")
            
            return {
                "average": avg,
                "min": min_time,
                "max": max_time,
                "stddev": std_dev,
                "count": len(times)
            }
        
        return None
    
    def test_search_with_category(self, motor: str, category: str = "AI"):
        """Prueba búsqueda con filtro de categoría"""
        print_section(f"Búsqueda con filtro (categoría={category}) en {motor.upper()}...")
        
        times = []
        
        for i in range(5):
            embedding = [0.5, 0.5, 0.5, 0.5]
            payload = {
                "embedding": embedding,
                "categoria": category,
                "top_k": 5
            }
            
            try:
                start_time = time.time()
                response = requests.post(f"{API_BASE}/{motor}/search", json=payload, timeout=10)
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    results = response.json()
                    times.append(elapsed)
                    print_info(f"  Búsqueda {i+1}: {elapsed*1000:.2f}ms ({len(results)} resultados)")
            except Exception as e:
                print_error(f"  Búsqueda {i+1}: {str(e)}")
        
        if times:
            avg = statistics.mean(times)
            print_success(f"Promedio con filtro: {avg*1000:.2f}ms")
            return avg
        
        return None
    
    def compare_results(self):
        """Compara resultados entre motores"""
        print_section("Comparación de rendimiento")
        
        # Buscar con el mismo embedding en ambos motores
        embedding = [0.5, 0.5, 0.5, 0.5]
        payload = {"embedding": embedding, "top_k": 5}
        
        results = {}
        
        for motor in ["pgvector", "milvus"]:
            try:
                start_time = time.time()
                response = requests.post(f"{API_BASE}/{motor}/search", json=payload, timeout=10)
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    docs = response.json()
                    results[motor] = {
                        "time": elapsed,
                        "count": len(docs),
                        "ids": [d["id"] for d in docs]
                    }
            except Exception as e:
                print_error(f"{motor}: {str(e)}")
        
        # Mostrar tabla comparativa
        if "pgvector" in results and "milvus" in results:
            pgvector_time = results["pgvector"]["time"]
            milvus_time = results["milvus"]["time"]
            
            print_table(
                ["Motor", "Tiempo (ms)", "Documentos"],
                [
                    ["PGVector", f"{pgvector_time*1000:.2f}", results["pgvector"]["count"]],
                    ["Milvus", f"{milvus_time*1000:.2f}", results["milvus"]["count"]]
                ]
            )
            
            if pgvector_time < milvus_time:
                ratio = milvus_time / pgvector_time
                print_success(f"PGVector fue {ratio:.2f}x más rápido")
            else:
                ratio = pgvector_time / milvus_time
                print_success(f"Milvus fue {ratio:.2f}x más rápido")
            
            # Comparar IDs
            if results["pgvector"]["ids"] == results["milvus"]["ids"]:
                print_success("Ambos motores retornaron los mismos documentos")
            else:
                print_info("Los motores retornaron diferentes documentos (esperado)")

def main():
    print_header("🧪 PRUEBAS DE RENDIMIENTO: PGVector vs Milvus")
    
    tester = PerformanceTest()
    
    if not tester.test_api_connection():
        sys.exit(1)
    
    print_info("Nota: Estas pruebas crean documentos con el prefijo '*_bulk_'")
    print_info("Se pueden limpiar después de las pruebas")
    
    # Menú de pruebas
    while True:
        print_header("Menú de Pruebas")
        print(f"{Colors.OKBLUE}1{Colors.ENDC} - Crear documentos en bulk (50)")
        print(f"{Colors.OKBLUE}2{Colors.ENDC} - Prueba de búsqueda (10 iteraciones)")
        print(f"{Colors.OKBLUE}3{Colors.ENDC} - Búsqueda con filtro (categoría)")
        print(f"{Colors.OKBLUE}4{Colors.ENDC} - Comparar resultados finales")
        print(f"{Colors.OKBLUE}5{Colors.ENDC} - Ejecutar todas las pruebas")
        print(f"{Colors.OKBLUE}0{Colors.ENDC} - Salir")
        
        choice = input(f"\n{Colors.BOLD}Selecciona: {Colors.ENDC}").strip()
        
        if choice == "1":
            for motor in ["pgvector", "milvus"]:
                tester.create_bulk_documents(motor, 50)
        elif choice == "2":
            for motor in ["pgvector", "milvus"]:
                tester.test_search_performance(motor, 10, 5)
        elif choice == "3":
            for motor in ["pgvector", "milvus"]:
                tester.test_search_with_category(motor, "AI")
        elif choice == "4":
            tester.compare_results()
        elif choice == "5":
            for motor in ["pgvector", "milvus"]:
                tester.create_bulk_documents(motor, 50)
            print()
            for motor in ["pgvector", "milvus"]:
                tester.test_search_performance(motor, 10, 5)
            print()
            tester.compare_results()
        elif choice == "0":
            print_success("¡Hasta luego!")
            break
        else:
            print_error("Opción inválida")

if __name__ == "__main__":
    main()
