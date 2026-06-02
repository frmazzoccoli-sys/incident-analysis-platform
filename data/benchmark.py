# data/benchmark.py

import sys
import os

# Agregar la raíz del proyecto al path para poder importar src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.metricas.medidor import (
    benchmark_busquedas,
    benchmark_ordenamientos,
    benchmark_memoria
)
from src.metricas.reporte import (
    mostrar_busquedas,
    mostrar_ordenamientos,
    mostrar_memoria,
    mostrar_analisis
)

# ---------------------------------------------------------------------------
# Tamaños crecientes para el benchmark
# ---------------------------------------------------------------------------

TAMANIOS = [100, 500, 1000, 2000, 5000]

# ---------------------------------------------------------------------------
# Ejecución principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("   PLATAFORMA DE ANÁLISIS DE INCIDENTES")
    print("   Benchmark de algoritmos y estructuras de datos")
    print("=" * 65)
    print(f"\n  Tamaños evaluados: {TAMANIOS}")
    print("  Por favor esperá, esto puede tardar unos segundos...\n")

    # Benchmark de búsquedas
    print("  Midiendo búsquedas...")
    resultados_busqueda = benchmark_busquedas(TAMANIOS)
    mostrar_busquedas(resultados_busqueda)

    # Benchmark de ordenamientos
    print("\n  Midiendo ordenamientos...")
    resultados_orden = benchmark_ordenamientos(TAMANIOS)
    mostrar_ordenamientos(resultados_orden)

    # Benchmark de memoria
    print("\n  Midiendo memoria...")
    resultados_memoria = benchmark_memoria(TAMANIOS)
    mostrar_memoria(resultados_memoria)

    # Análisis textual
    mostrar_analisis()