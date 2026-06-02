# src/algoritmos/busqueda.py

import bisect

# BUSQUEDA SECUENCIAL

def busqueda_secuencial(eventos, event_id):

    """
    Busca un evento por event_id recorriendo la lista elemento por elemento.

    No requiere que la lista esté ordenada. Compara cada evento hasta
    encontrar el buscado o agotar la lista.

    Args:
        eventos (list[Event]): Lista de eventos donde buscar.
        event_id (str): Identificador del evento a buscar.

    Returns:
        Event: El evento encontrado, o None si no existe.

    Complejidad:
        Mejor caso:  O(1) → el evento está en la primera posición.
        Peor caso:   O(n) → el evento está al final o no existe.
        Promedio:    O(n/2) → simplificado como O(n).
    """

    for evento in eventos:
        if evento.event_id == event_id:
            return evento
    return None

# BUSQUEDA BINARIA

def busqueda_binaria(eventos_ordenados, event_id):

    """
    Busca un evento por event_id usando bisect sobre una lista ordenada.

    Requiere que la lista esté previamente ordenada por event_id.
    Divide la lista por la mitad en cada paso, descartando la mitad
    que no puede contener el elemento buscado.

    Usa bisect_left para encontrar la posición de inserción del event_id
    y luego verifica si el elemento en esa posición coincide.

    Args:
        eventos_ordenados (list[Event]): Lista de eventos ordenada por event_id.
        event_id (str): Identificador del evento a buscar.

    Returns:
        Event: El evento encontrado, o None si no existe.

    Complejidad:
        Mejor caso:  O(1) → el evento está en el medio exacto.
        Peor caso:   O(log n) → divide la lista log n veces.
        Promedio:    O(log n).
    """

    # Extraemos solo los ids para que bisect pueda comparar
    
    ids = [e.event_id for e in eventos_ordenados]
    indice = bisect.bisect_left(ids, event_id)

    if indice < len(eventos_ordenados) and eventos_ordenados[indice].event_id == event_id:
        return eventos_ordenados[indice]
    return None