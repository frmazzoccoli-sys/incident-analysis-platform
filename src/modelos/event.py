class Event:
    """
    Clase que representa un incidente, atributos: id, timestamp, categoria, prioridad, texto, origen, destino
    """
    def __init__(
        self,
        event_id,
        timestamp,
        categoria,
        prioridad,
        texto,
        origen,
        destino
    ):
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
    
print(Event)