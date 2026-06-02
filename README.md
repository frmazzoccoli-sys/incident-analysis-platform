# incident-analysis-platform

Proyecto AyED sobre análisis de incidentes.

## Estructura del proyecto

```
incident-analysis-platform/
│
├── benchmarks/                      # scripts de evaluación de performance
│       └── benchmark.py             # script que genera y mide datasets de tamaños crecientes
├── data/                            # datasets, pruebas, ejemplos, archivos de entrada/salida
├── tests/                           # pruebas unitarias y validaciones
│
├── src/                             # código fuente del proyecto
│   ├── main.py                      # punto de entrada
│   │
│   ├── modelos/                     # clase Event
│   ├── estructuras/                 # árboles, heaps, grafos, colas, queue, heap, BST
|   │       ├── __init__.py
│   │       ├── queue_eventos.py     # Queue FIFO
│   │       ├── priority_queue.py    # PriorityQueue con heapq
│   │       └── bst.py               # Binary Search Tree y NodoBST
│   ├── algoritmos/                  # búsquedas, ordenamientos
|   │       ├── __init__.py
│   │       ├── busqueda.py          # secuencial + binaria
│   │       └── ordenamiento.py      # burbuja + mergesort
│   ├── metricas/                    # timeit, complejidad, benchmarking
│   │       ├── __init__.py
│   │       ├── medidor.py           # funciones de medición con timeit y tracemalloc
│   │       └── reporte.py           # funciones para mostrar resultados en consola
│   ├── servicios/                   # EventStore, Index, Router, TextAnalyzer
│   │       ├── __init__.py
│   │       ├── event_store.py       # EventStore
│   │       ├── index.py             # Index (hashing)
│   │       ├── router.py            # Router
│   │       └── text_analyzer.py     # TextAnalyzer
│   └── utils/                       # funciones auxiliares reutilizables
│
├── requirements.txt      # dependencias del proyecto
└── README.md             # descripción, uso e instrucciones
```
```
data/ → datasets, ejemplos, archivos de entrada/salida
tests/ → pruebas unitarias y validaciones
src/ → código fuente del proyecto
main.py → punto de entrada del programa
modelos/ → Event
estructuras/ → queue, heap, NodoBST, BST
algoritmos/ → búsquedas, ordenamientos
metricas/ → timeit, complejidad, benchmarking
servicios/ → EventStore, Index, Router, TextAnalyzer
utils/ → funciones auxiliares reutilizables
requirements.txt → dependencias del proyecto
README.md → descripción, uso e instrucciones
__init__.py → marca carpetas como paquetes Python importables.
```