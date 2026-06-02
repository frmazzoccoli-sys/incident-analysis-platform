# src/main.py

"""
Punto de entrada principal de la plataforma de análisis de incidentes.

Este módulo es el punto de inicio del programa. Coordina la carga de eventos,
su procesamiento a través de los distintos servicios y la presentación de resultados.
"""

import sys
import os
from datetime import datetime

# Agregar la raíz del proyecto al path para poder importar src/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.modelos.event import Event
from src.servicios.event_store import EventStore
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
    router = Router()
    text_analyzer = TextAnalyzer()
    
    # Estructuras de datos
    queue = QueueEventos()
    priority_queue = PriorityQueueEventos()

    # Ejemplo de flujo de negocio: crear, almacenar e indexar un evento
    ejemplo_evento = Event(
        "E001",
        datetime.now(),
        "seguridad",
        1,
        "Acceso no autorizado detectado",
        "servidor-A",
        "base-datos"
    )
    event_store.agregar(ejemplo_evento)
    eventos_seguridad = event_store.buscar_por_categoria("seguridad")

    print("\n✓ Servicios inicializados correctamente")
    print("  - EventStore: almacenamiento de eventos con índice integrado")
    print("  - Router: gestión de rutas origen-destino")
    print("  - TextAnalyzer: análisis de texto")
    print("  - QueueEventos: procesamiento FIFO")
    print("  - PriorityQueueEventos: procesamiento por prioridad")
    print(f"  - Eventos de seguridad indexados: {len(eventos_seguridad)}")
    print(f"  - Evento E001 recuperado desde EventStore: {event_store.obtener('E001')}")
    
    print("\n" + "=" * 65)
    print("   Para ejecutar benchmarks, usar: python benchmarks/benchmark.py")
    print("=" * 65)


if __name__ == "__main__":
    main()
