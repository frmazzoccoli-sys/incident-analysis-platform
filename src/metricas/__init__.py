# src/metricas/__init__.py

from .medidor import (
    generar_eventos,
    medir_tiempo,
    medir_memoria,
    benchmark_busquedas,
    benchmark_ordenamientos,
    benchmark_memoria
)

from .reporte import (
    mostrar_busquedas,
    mostrar_ordenamientos,
    mostrar_memoria,
    mostrar_analisis
)