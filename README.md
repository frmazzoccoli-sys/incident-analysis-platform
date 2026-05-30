# incident-analysis-platform

Proyecto AyED sobre análisis de incidentes.

## Estructura del proyecto

```
incident-analysis-platform/
│
├── data/                 # datasets, pruebas, ejemplos
├── docs/                 # documentación
├── tests/                # tests unitarios
│
├── src/
│   ├── main.py           # punto de entrada
│   ├── modelos/          # clases (Incidente, Nodo, Event, etc.)
│   ├── estructuras/      # árboles, heaps, grafos, colas
│   ├── algoritmos/       # búsquedas, rutas, patrones
│   ├── seguridad/        # RSA, cifrado, hashing
│   ├── metricas/         # tiempos, complejidad, benchmarking
│   ├── servicios/        # lógica de negocio
│   └── utils/            # helpers
│
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
- `estructuras/` → colas, heaps, árboles, grafos, etc.
- `algoritmos/` → búsquedas, ordenamientos, rutas
- `seguridad/` → RSA, cifrado, hashing
- `metricas/` → mediciones, `timeit`, benchmarking
- `servicios/` → EventStore, Index, Router, TextAnalyzer
- `utils/` → funciones auxiliares reutilizables
- `requirements.txt` → dependencias del proyecto

Mantén este README actualizado con instrucciones de instalación y uso.
