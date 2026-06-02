# incident-analysis-platform

Proyecto AyED para la plataforma de análisis de incidentes.

## Descripción

Esta aplicación implementa un flujo de negocio de gestión de incidentes que incluye:
- almacenamiento y gestión de eventos con `EventStore`
- indexación rápida por `id`, `categoría` y `origen`
- análisis de texto sobre descripciones de incidentes
- procesamiento con colas FIFO y de prioridad
- rutas de origen-destino para registrar y consultar conexiones entre sistemas

## Requisitos

- Python 3.11+ recomendado
- entorno virtual (`venv`) para dependencias
- El archivo `requirements.txt` actualmente contiene solo `pytest>=7.0`
  para ejecutar las pruebas.

## Instalación

Desde la raíz del proyecto:

```powershell
python -m venv .venv
& ".venv\Scripts\Activate.ps1"
pip install -r requirements.txt
```

## Ejecución

### Ejecutar la aplicación principal

```powershell
python src/main.py
```

### Ejecutar benchmarks

```powershell
& ".venv\Scripts\python.exe" benchmarks/benchmark.py
```

o si el entorno virtual está activo:

```powershell
python benchmarks/benchmark.py
```

## Tests

Ejecutar la suite de pruebas con `pytest`:

```powershell
python -m pytest -q
```

## Estructura del proyecto

```
incident-analysis-platform/
├── benchmarks/                  # scripts de benchmarking y medición de performance
│   └── benchmark.py             # generador y medidor de datasets
├── data/                        # archivos de datos, ejemplos y documentación auxiliar
├── tests/                       # pruebas unitarias
├── src/                         # código fuente del proyecto
│   ├── main.py                  # punto de entrada de la aplicación
│   ├── modelos/                 # definición del modelo Event
│   │   └── event.py
│   ├── estructuras/             # estructuras de datos (colas, heaps, BST)
│   │   ├── queue_eventos.py
│   │   ├── priority_queue.py
│   │   └── bst.py
│   ├── algoritmos/              # algoritmos de búsqueda y ordenamiento
│   │   ├── busqueda.py
│   │   └── ordenamiento.py
│   ├── metricas/                # mediciones de tiempo y reporte de resultados
│   │   ├── medidor.py
│   │   └── reporte.py
│   ├── servicios/               # servicios de negocio del sistema
│   │   ├── event_store.py
│   │   ├── index.py
│   │   ├── router.py
   │   └── text_analyzer.py
│   └── utils/                   # funciones auxiliares reutilizables
├── requirements.txt             # dependencias del proyecto
└── README.md                    # documentación del proyecto
```

## Características principales

- `EventStore`: almacena eventos y mantiene un índice integrado para consultas rápidas.
- `Index`: búsqueda por `event_id`, `categoría` y `origen`.
- `TextAnalyzer`: análisis de texto, búsqueda por palabra/patrón y palabras frecuentes.
- `QueueEventos`: cola FIFO para procesamiento en orden de llegada.
- `PriorityQueueEventos`: cola de prioridad por severidad y timestamp.
- `Router`: registro y consulta de rutas origen-destino.

## Flujo de negocio

El flujo típico del proyecto es:
1. crear un evento
2. almacenar el evento en `EventStore`
3. indexar automáticamente por `id`, `categoría` y `origen`
4. analizar texto para buscar incidentes relevantes
5. priorizar eventos con la cola de prioridad

## Consideraciones

- El `EventStore` se usa como fuente de verdad única y mantiene la consistencia entre almacenamiento e índice.
- La aplicación principal (`src/main.py`) debe ejecutarse desde la raíz del proyecto para que las rutas de importación funcionen correctamente.
- Los tests validan la integración entre servicios, el almacenamiento, la indexación y el análisis.
- El README incluye instrucciones claras de instalación, ejecución y pruebas para facilitar el uso.
```