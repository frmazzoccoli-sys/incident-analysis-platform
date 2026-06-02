timeit es el módulo estándar de Python para medir tiempos de ejecución. La ventaja sobre medir con time.time() es que:

Característica                  time.time()             timeit
Repeticiones automáticas        No                      Si
Elimina ruido del sistema       No                      Si
Deshabilita garbage collector   No                      Si
Precisión                       Baja                    Alta

timeit ejecuta el código muchas veces y reporta el tiempo mínimo, eliminando variaciones del sistema operativo.

Tenemos estos algoritmos implementados que vale la pena comparar:
Búsquedas
Algoritmo           Complejidad             ¿Qué esperamos ver?
Secuencial          O(n)                    Tiempo crece linealmente con n
Binaria             O(log n)                Tiempo crece muy lento con n

Ordenamientos
Algoritmo           Complejidad             ¿Qué esperamos ver?
Burbuja             O(n²)                   Tiempo explota con n grande
Mergesort           O(n log n)              Tiempo crece moderadamente
sorted()            O(n log n)              Similar a mergesort pero más rápido (C nativo)

Para que la diferencia entre O(n), O(n log n) y O(n²) sea visible, necesitamos tamaños suficientemente grandes: 
tamanios = [100, 500, 1000, 2000, 5000]

Con n=5000, burbuja hace ~25.000.000 comparaciones mientras mergesort hace ~60.000. La diferencia será dramática y útil.

¿Cómo manejamos la memoria?
La consigna dice "si aplica". Para memoria usamos el módulo tracemalloc de Python (estándar, sin dependencias externas):

import tracemalloc
tracemalloc.start()
# ... código a medir ...
_, pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

Esto nos da el pico de memoria en bytes durante la ejecución.

Estructura del modulo:
El módulo de métricas tiene dos responsabilidades distintas:

Medir: funciones que ejecutan timeit y tracemalloc y devuelven números
Reportar: funciones que muestran los resultados de forma legible

Las separamos en dos archivos para mantener la modularidad:
src/
└── metricas/
    ├── __init__.py
    ├── medidor.py      ← funciones de medición con timeit y tracemalloc
    └── reporte.py      ← funciones para mostrar resultados en consola

Y un script separado que ejecuta todas las mediciones:
benchmarks/
└── benchmark.py        ← script que genera y mide datasets de tamaños crecientes

--------------------------

Generamos datos de prueba realistas:
Necesitamos listas de eventos con timestamps y event_ids variados. Usamos random para generar datasets de distintos tamaños sin repetir IDs:
Ejemplo de lo que generará el benchmark
eventos_100  = generar_eventos(100)
eventos_500  = generar_eventos(500)
eventos_1000 = generar_eventos(1000)

Plan de implementación
1. src/metricas/medidor.py   → funciones medir_tiempo() y medir_memoria()
2. src/metricas/reporte.py   → función mostrar_reporte()
3. src/metricas/__init__.py  → exports del módulo
4. benchmarks/benchmark.py   → script principal que corre todo

Lo que vamos a mostrar al ejecutarse:
=============================================
   BENCHMARK DE ALGORITMOS - BÚSQUEDA
=============================================
n=100    secuencial: 0.000012s   binaria: 0.000003s
n=500    secuencial: 0.000058s   binaria: 0.000004s
n=1000   secuencial: 0.000115s   binaria: 0.000005s
n=2000   secuencial: 0.000231s   binaria: 0.000006s
n=5000   secuencial: 0.000578s   binaria: 0.000007s

=============================================
   BENCHMARK DE ALGORITMOS - ORDENAMIENTO
=============================================
n=100    burbuja: 0.000210s   mergesort: 0.000045s   sorted: 0.000008s
n=500    burbuja: 0.005200s   mergesort: 0.000280s   sorted: 0.000035s
n=1000   burbuja: 0.021000s   mergesort: 0.000620s   sorted: 0.000075s
n=2000   burbuja: 0.084000s   mergesort: 0.001400s   sorted: 0.000160s
n=5000   burbuja: 0.520000s   mergesort: 0.003800s   sorted: 0.000430s


