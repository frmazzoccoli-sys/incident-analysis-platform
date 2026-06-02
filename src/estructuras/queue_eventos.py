# src/estructuras/queue_eventos.py

from collections import deque


class QueueEventos:
    """
    Cola FIFO para gestión de eventos en orden de llegada.

    Utiliza collections.deque como estructura interna por su eficiencia
    O(1) en operaciones de enqueue y dequeue, a diferencia de list
    que tiene O(n) al eliminar del frente con pop(0).

    Operaciones principales:
        enqueue → O(1)
        dequeue → O(1)
        peek    → O(1)
        size    → O(1)
    """

    def __init__(self):
        """Inicializa una cola vacía."""
        self._cola = deque()

    def enqueue(self, evento):
        """
        Agrega un evento al final de la cola.

        Args:
            evento (Event): El incidente a encolar.

        Complejidad: O(1)
        """
        self._cola.append(evento)

    def dequeue(self):
        """
        Elimina y retorna el evento del frente de la cola.

        Returns:
            Event: El incidente más antiguo en la cola.

        Raises:
            IndexError: Si la cola está vacía.

        Complejidad: O(1)
        """
        if self.esta_vacia():
            raise IndexError("No se puede hacer dequeue: la cola está vacía.")
        return self._cola.popleft()

    def peek(self):
        """
        Retorna el evento del frente sin eliminarlo.

        Returns:
            Event: El próximo evento a procesar.

        Raises:
            IndexError: Si la cola está vacía.

        Complejidad: O(1)
        """
        if self.esta_vacia():
            raise IndexError("No se puede hacer peek: la cola está vacía.")
        return self._cola[0]

    def esta_vacia(self):
        """
        Indica si la cola no tiene elementos.

        Returns:
            bool: True si está vacía, False si tiene elementos.

        Complejidad: O(1)
        """
        return len(self._cola) == 0

    def tamanio(self):
        """
        Retorna la cantidad de eventos en la cola.

        Returns:
            int: Número de eventos encolados.

        Complejidad: O(1)
        """
        return len(self._cola)

    def __repr__(self):
        return f"QueueEventos(tamanio={self.tamanio()})"