# src/metricas/medidor.py

import timeit
import tracemalloc
import random
from datetime import datetime, timedelta

from src.modelos.event import Event
from src.algoritmos.busqueda import busqueda_secuencial, busqueda_binaria
from src.algoritmos.ordenamiento import burbuja, mergesort
from src.estructuras.bst import BST
from src.servicios.index import Index


# ---------------------------------------------------------------------------
# Generador de datos de prueba
# ---------------------------------------------------------------------------

def generar_eventos(n):
    """
    Genera una lista de n eventos con datos aleatorios y únicos.

    Usa random.sample para garantizar event_ids únicos y timedelta
    para distribuir los timestamps a lo largo de un día completo.

    Args:
        n (int): Cantidad de eventos a generar.

    Returns:
        list[Event]: Lista de n eventos con datos aleatorios.
    """
    base = datetime(2024, 1, 1)
    ids = random.sample(range(n * 10), n)
    categorias = ["seguridad", "red", "mantenimiento"]

    return [
        Event(
            event_id=f"E{str(i).zfill(6)}",
            timestamp=base + timedelta(seconds=random.randint(0, 86400)),
            categoria=random.choice(categorias),
            prioridad=random.randint(1, 5),
            texto="Evento de prueba generado",
            origen=f"nodo-{random.randint(1, 10)}",
            destino=f"nodo-{random.randint(1, 10)}"
        )
        for i in ids
    ]


# ---------------------------------------------------------------------------
# Medición de tiempo
# ---------------------------------------------------------------------------

def medir_tiempo(funcion, repeticiones=100):
    """
    Mide el tiempo promedio de ejecución de una función sin argumentos.

    Usa timeit para ejecutar la función múltiples veces y retorna
    el tiempo promedio por ejecución, eliminando el ruido del sistema.

    Args:
        funcion (callable): Función sin argumentos a medir.
                            Usar lambda para funciones con argumentos.
        repeticiones (int): Cantidad de veces que se ejecuta la función.
                            Por defecto 100.

    Returns:
        float: Tiempo promedio de ejecución en segundos.
    """
    tiempo_total = timeit.timeit(funcion, number=repeticiones)
    return tiempo_total / repeticiones


# ---------------------------------------------------------------------------
# Medición de memoria
# ---------------------------------------------------------------------------

def medir_memoria(funcion):
    """
    Mide el pico de memoria utilizado durante la ejecución de una función.

    Usa tracemalloc para rastrear las asignaciones de memoria en tiempo
    real y retorna el pico máximo alcanzado durante la ejecución.

    Args:
        funcion (callable): Función sin argumentos a medir.

    Returns:
        float: Pico de memoria en kilobytes.
    """
    tracemalloc.start()
    funcion()
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico / 1024


# ---------------------------------------------------------------------------
# Benchmark de búsquedas
# ---------------------------------------------------------------------------

def benchmark_busquedas(tamanios):
    """
    Mide y compara los cuatro métodos de búsqueda sobre tamaños crecientes.

    Para cada tamaño genera un dataset, prepara las estructuras necesarias
    y mide el tiempo promedio de cada método buscando un event_id que
    no existe (peor caso para secuencial y binaria).

    Args:
        tamanios (list[int]): Lista de tamaños de dataset a evaluar.

    Returns:
        list[dict]: Lista de resultados por tamaño, cada uno con:
                    n, secuencial, binaria, bst, hashing (tiempos en segundos)
    """
    resultados = []

    for n in tamanios:
        eventos = generar_eventos(n)
        eventos_ordenados = sorted(eventos, key=lambda e: e.event_id)
        objetivo = "E999999"    # ID que no existe → peor caso

        # Preparar BST
        arbol = BST()
        for e in eventos:
            arbol.insertar(e)

        # Preparar índice hash
        index = Index()
        for e in eventos:
            index.agregar(e)

        # Medir cada método
        t_secuencial = medir_tiempo(
            lambda: busqueda_secuencial(eventos, objetivo)
        )
        t_binaria = medir_tiempo(
            lambda: busqueda_binaria(eventos_ordenados, objetivo)
        )
        t_bst = medir_tiempo(
            lambda: arbol.buscar(objetivo)
        )
        t_hashing = medir_tiempo(
            lambda: index.buscar_por_id(objetivo)
        )

        resultados.append({
            "n": n,
            "secuencial": t_secuencial,
            "binaria": t_binaria,
            "bst": t_bst,
            "hashing": t_hashing
        })

    return resultados


# ---------------------------------------------------------------------------
# Benchmark de ordenamientos
# ---------------------------------------------------------------------------

def benchmark_ordenamientos(tamanios):
    """
    Mide y compara los tres métodos de ordenamiento sobre tamaños crecientes.

    Para burbuja con n grande se reduce el número de repeticiones para
    evitar tiempos de ejecución excesivos, dado su complejidad O(n²).

    Args:
        tamanios (list[int]): Lista de tamaños de dataset a evaluar.

    Returns:
        list[dict]: Lista de resultados por tamaño, cada uno con:
                    n, burbuja, mergesort, sorted (tiempos en segundos)
    """
    resultados = []

    for n in tamanios:
        eventos = generar_eventos(n)

        # Reducir repeticiones para burbuja con n grande
        reps_burbuja = 10 if n >= 1000 else 100

        t_burbuja = medir_tiempo(
            lambda: burbuja(eventos),
            repeticiones=reps_burbuja
        )
        t_mergesort = medir_tiempo(
            lambda: mergesort(eventos)
        )
        t_sorted = medir_tiempo(
            lambda: sorted(eventos, key=lambda e: e.timestamp)
        )

        resultados.append({
            "n": n,
            "burbuja": t_burbuja,
            "mergesort": t_mergesort,
            "sorted": t_sorted
        })

    return resultados


# ---------------------------------------------------------------------------
# Benchmark de memoria
# ---------------------------------------------------------------------------

def benchmark_memoria(tamanios):
    """
    Mide el pico de memoria de cada algoritmo de ordenamiento.

    Args:
        tamanios (list[int]): Lista de tamaños de dataset a evaluar.

    Returns:
        list[dict]: Lista de resultados por tamaño, cada uno con:
                    n, burbuja, mergesort, sorted (memoria en KB)
    """
    resultados = []

    for n in tamanios:
        eventos = generar_eventos(n)

        m_burbuja = medir_memoria(lambda: burbuja(eventos))
        m_mergesort = medir_memoria(lambda: mergesort(eventos))
        m_sorted = medir_memoria(
            lambda: sorted(eventos, key=lambda e: e.timestamp)
        )

        resultados.append({
            "n": n,
            "burbuja": m_burbuja,
            "mergesort": m_mergesort,
            "sorted": m_sorted
        })

    return resultados