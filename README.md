# incident-analysis-platform

Proyecto AyED sobre análisis de incidentes.

## Estructura del proyecto

```
incident-analysis-platform/
│
├── data/                 # datasets, pruebas, ejemplos, archivos de entrada/salida
├── docs/                 # documentación
├── tests/                # pruebas unitarias y validaciones
│
├── src/                             # código fuente del proyecto
│   ├── main.py                      # punto de entrada
│   │
│   ├── modelos/                     # clase Event
│   ├── estructuras/                 # árboles, heaps, grafos, colas, queue, heap, BST
|   |       ├── __init__.py
│   |       ├──queue_eventos.py      # Queue FIFO
│   |       └── priority_queue.py    # PriorityQueue con heapq
│   ├── algoritmos/                  # búsquedas, ordenamientos
│   ├── seguridad/                   # RSA, cifrado, hashing
│   ├── metricas/                    # tiempos, complejidad, benchmarking
│   ├── servicios/                   # EventStore, Index, Router, TextAnalyzer
│   └── utils/                       # funciones auxiliares reutilizables
│
├── requirements.txt      # dependencias del proyecto
└── README.md             # descripción, uso e instrucciones
```
```
data/ → datasets, ejemplos, archivos de entrada/salida
docs/ → documentación del proyecto
tests/ → pruebas unitarias y validaciones
src/ → código fuente del proyecto
main.py → punto de entrada del programa
modelos/ → Event
estructuras/ → queue, heap, BST, etc.
algoritmos/ → búsquedas, ordenamientos
seguridad/ → RSA, cifrado, hashing
metricas/ → timeit, complejidad, benchmarking
servicios/ → EventStore, Index, Router, TextAnalyzer
utils/ → funciones auxiliares reutilizables
requirements.txt → dependencias del proyecto
README.md → descripción, uso e instrucciones
__init__.py → marca carpetas como paquetes Python importables.
```