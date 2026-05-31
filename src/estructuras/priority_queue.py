import heapq
import itertools


class PriorityQueueEventos:
    """
    Cola de prioridad para gestión de eventos por severidad.

    Utiliza heapq (min-heap) internamente. Los eventos con menor número
    de prioridad son atendidos primero (prioridad 1 = más crítico).
    Ante igualdad de prioridad, se atiende primero el evento más antiguo
    (menor timestamp).

    La tupla almacenada es: (prioridad, timestamp, contador, evento)
    El contador garantiza desempate sin comparar objetos Event directamente,
    evitando TypeError si dos eventos tienen igual prioridad y timestamp.

    Operaciones principales:
        push  → O(log n)
        pop   → O(log n)
        peek  → O(1)
        size  → O(1)
    """

    def __init__(self):
        """Inicializa una cola de prioridad vacía."""
        self._heap = []
        self._contador = itertools.count()

    def push(self, evento):
        """
        Inserta un evento en la cola respetando su prioridad.

        Args:
            evento (Event): El incidente a insertar.

        Complejidad: O(log n)
        """
        tupla = (evento.prioridad, evento.timestamp, next(self._contador), evento)
        heapq.heappush(self._heap, tupla)

    def pop(self):
        """
        Extrae y retorna el evento más prioritario.

        Returns:
            Event: El incidente más crítico (menor prioridad numérica).

        Raises:
            IndexError: Si la cola está vacía.

        Complejidad: O(log n)
        """
        if self.esta_vacia():
            raise IndexError("No se puede hacer pop: la cola está vacía.")
        _, _, _, evento = heapq.heappop(self._heap)
        return evento

    def peek(self):
        """
        Retorna el evento más prioritario sin extraerlo.

        Returns:
            Event: El incidente más crítico en espera.

        Raises:
            IndexError: Si la cola está vacía.

        Complejidad: O(1)
        """
        if self.esta_vacia():
            raise IndexError("No se puede hacer peek: la cola está vacía.")
        _, _, _, evento = self._heap[0]
        return evento

    def esta_vacia(self):
        """
        Indica si la cola no tiene elementos.

        Returns:
            bool: True si está vacía, False si tiene elementos.

        Complejidad: O(1)
        """
        return len(self._heap) == 0

    def tamanio(self):
        """
        Retorna la cantidad de eventos en la cola.

        Returns:
            int: Número de eventos en espera.

        Complejidad: O(1)
        """
        return len(self._heap)

    def __repr__(self):
        return f"PriorityQueueEventos(tamanio={self.tamanio()})"