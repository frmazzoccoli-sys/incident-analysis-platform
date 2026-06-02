# src/metricas/reporte.py


def mostrar_busquedas(resultados):
    """
    Muestra en consola los resultados del benchmark de búsquedas.

    Args:
        resultados (list[dict]): Salida de benchmark_busquedas().
    """
    print("\n" + "=" * 65)
    print("   BENCHMARK DE ALGORITMOS - BÚSQUEDA")
    print("=" * 65)
    print(f"{'n':<8} {'secuencial':>12} {'binaria':>12} {'bst':>12} {'hashing':>12}")
    print("-" * 65)

    for r in resultados:
        print(
            f"{r['n']:<8} "
            f"{r['secuencial']:>12.6f}s "
            f"{r['binaria']:>12.6f}s "
            f"{r['bst']:>12.6f}s "
            f"{r['hashing']:>12.6f}s"
        )

    print("=" * 65)


def mostrar_ordenamientos(resultados):
    """
    Muestra en consola los resultados del benchmark de ordenamientos.

    Args:
        resultados (list[dict]): Salida de benchmark_ordenamientos().
    """
    print("\n" + "=" * 65)
    print("   BENCHMARK DE ALGORITMOS - ORDENAMIENTO")
    print("=" * 65)
    print(f"{'n':<8} {'burbuja':>12} {'mergesort':>12} {'sorted()':>12}")
    print("-" * 65)

    for r in resultados:
        print(
            f"{r['n']:<8} "
            f"{r['burbuja']:>12.6f}s "
            f"{r['mergesort']:>12.6f}s "
            f"{r['sorted']:>12.6f}s"
        )

    print("=" * 65)


def mostrar_memoria(resultados):
    """
    Muestra en consola los resultados del benchmark de memoria.

    Args:
        resultados (list[dict]): Salida de benchmark_memoria().
    """
    print("\n" + "=" * 65)
    print("   BENCHMARK DE MEMORIA - ORDENAMIENTO")
    print("=" * 65)
    print(f"{'n':<8} {'burbuja':>12} {'mergesort':>12} {'sorted()':>12}")
    print("-" * 65)

    for r in resultados:
        print(
            f"{r['n']:<8} "
            f"{r['burbuja']:>12.2f}KB "
            f"{r['mergesort']:>12.2f}KB "
            f"{r['sorted']:>12.2f}KB"
        )

    print("=" * 65)


def mostrar_analisis():
    """
    Muestra un análisis textual de los resultados observados.
    Útil para incluir en el informe y como cierre del benchmark.
    """
    print("\n" + "=" * 65)
    print("   ANÁLISIS DE RESULTADOS")
    print("=" * 65)
    print("""
BÚSQUEDA:
  - Secuencial O(n): el tiempo crece linealmente con n.
    Con n=5000 es significativamente más lento que los demás.
  - Binaria O(log n): crece muy lento. Requiere lista ordenada.
  - BST O(log n): similar a binaria pero sin necesidad de
    reordenar la lista ante cada inserción.
  - Hashing O(1): el más rápido. El tiempo es prácticamente
    constante independientemente de n.

ORDENAMIENTO:
  - Burbuja O(n²): el tiempo explota con n grande.
    La diferencia con mergesort es dramática en n=5000.
  - Mergesort O(n log n): crece moderadamente. Garantiza
    O(n log n) en todos los casos.
  - sorted() O(n log n): el más rápido por estar implementado
    en C nativo. Es la referencia de rendimiento óptimo.

MEMORIA:
  - Burbuja y mergesort crean copias de la lista → O(n).
  - sorted() también usa O(n) pero con menor overhead.
  - El trade-off tiempo/memoria favorece mergesort sobre
    burbuja: mismo uso de memoria, mucho mejor tiempo.
""")
    print("=" * 65)