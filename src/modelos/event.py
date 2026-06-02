# src/modelos/event.py

class Event:
    """
    Clase que representa un incidente.
    
    Atributos:
        event_id (str): Identificador único del evento.
        timestamp (datetime): Fecha y hora del incidente.
        categoria (str): Tipo de incidente (seguridad, red, etc.).
        prioridad (int): Nivel de urgencia (1 = más crítico).
        texto (str): Descripción del incidente.
        origen (str): Nodo o sistema de origen.
        destino (str): Nodo o sistema de destino.
    """

    def __init__(self, event_id, timestamp, categoria, prioridad, texto, origen, destino):
        self.event_id = event_id
        self.timestamp = timestamp
        self.categoria = categoria
        self.prioridad = prioridad
        self.texto = texto
        self.origen = origen
        self.destino = destino

    def __str__(self):
        return (
            f"Event("
            f"id={self.event_id}, "
            f"categoria={self.categoria}, "
            f"prioridad={self.prioridad})"
        )