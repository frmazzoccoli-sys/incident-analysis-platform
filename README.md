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
├── src/                  # código fuente del proyecto
│   ├── main.py           # punto de entrada
│   ├── modelos/          # clases (Event, Incidente, Nodo, etc.)
│   ├── estructuras/      # colas, heaps, árboles, grafos
│   │   ├── __init__.py
│   │   ├── queue_eventos.py      # Queue FIFO
│   │   └── priority_queue.py    # PriorityQueue con heapq
│   ├── algoritmos/       # búsquedas, ordenamientos, rutas
│   ├── seguridad/        # RSA, cifrado, hashing
│   ├── metricas/         # tiempos, complejidad, benchmarking
│   ├── servicios/        # EventStore, Index, Router, TextAnalyzer
	└── utils/            # helpers

├── requirements.txt
└── README.md
```

Breve descripción de carpetas:

- `data/` → datasets, ejemplos, archivos de entrada/salida
- `docs/` → documentación del proyecto
- `tests/` → pruebas unitarias y validaciones
- `src/` → código fuente del proyecto
- `main.py` → punto de entrada del programa
- `modelos/` → clases como `Event`
- `estructuras/` → `queue_eventos.py`, `priority_queue.py`, colas y heaps
- `algoritmos/` → búsquedas, ordenamientos, rutas
- `seguridad/` → RSA, cifrado, hashing
- `metricas/` → mediciones y benchmarking
- `servicios/` → implementación de la lógica de negocio
- `utils/` → funciones auxiliares reutilizables
- `requirements.txt` → dependencias del proyecto

Mantén este README actualizado con instrucciones de instalación y uso.
