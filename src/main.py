# src/main.py

"""
Punto de entrada principal de la plataforma de análisis de incidentes.

Este módulo es el punto de inicio del programa. Coordina la carga de eventos,
su procesamiento a través de los distintos servicios y la presentación de resultados.
"""

import sys
import os

# Agregar la raíz del proyecto al path para poder importar src/
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.servicios.event_store import EventStore
from src.servicios.index import Index
from src.servicios.router import Router
from src.servicios.text_analyzer import TextAnalyzer
from src.estructuras.queue_eventos import QueueEventos
from src.estructuras.priority_queue import PriorityQueueEventos


def main():
    """
    Función principal que ejecuta la plataforma.
    
    Inicializa los servicios principales y demuestra sus funcionalidades.
    """
    print("=" * 65)
    print("   PLATAFORMA DE ANÁLISIS DE INCIDENTES")
    print("=" * 65)
    
    # Inicializar servicios
    event_store = EventStore()
    index = Index()
    router = Router()
    text_analyzer = TextAnalyzer()
    
    # Estructuras de datos
    queue = QueueEventos()
    priority_queue = PriorityQueueEventos()
    
    print("\n✓ Servicios inicializados correctamente")
    print("  - EventStore: almacenamiento de eventos")
    print("  - Index: búsqueda por ID, categoría, origen")
    print("  - Router: gestión de rutas origen-destino")
    print("  - TextAnalyzer: análisis de texto")
    print("  - QueueEventos: procesamiento FIFO")
    print("  - PriorityQueueEventos: procesamiento por prioridad")
    
    print("\n" + "=" * 65)
    print("   Para ejecutar benchmarks, usar: python benchmarks/benchmark.py")
    print("=" * 65)


if __name__ == "__main__":
    main()
