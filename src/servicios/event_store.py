# src/servicios/event_store.py


class EventStore:
    """
    Almacena y gestiona la colección principal de eventos.

    Actúa como repositorio central del sistema. Todos los eventos
    ingresados al sistema pasan primero por EventStore antes de
    ser indexados o procesados por otros servicios.

    Atributos:
        _eventos (list): Lista interna de eventos almacenados.

    Operaciones principales:
        agregar   → O(1)
        obtener   → O(n)
        eliminar  → O(n)
        listar    → O(1)
        tamanio   → O(1)
    """

    def __init__(self):
        """Inicializa un store vacío."""
        self._eventos = []

    def agregar(self, evento):
        """
        Agrega un evento al store.

        Args:
            evento (Event): El incidente a almacenar.

        Complejidad: O(1)
        """
        self._eventos.append(evento)

    def obtener(self, event_id):
        """
        Busca y retorna un evento por su event_id.

        Args:
            event_id (str): Identificador del evento a buscar.

        Returns:
            Event: El evento encontrado, o None si no existe.

        Complejidad: O(n) — búsqueda secuencial sobre la lista.
        """
        for evento in self._eventos:
            if evento.event_id == event_id:
                return evento
        return None

    def eliminar(self, event_id):
        """
        Elimina un evento del store por su event_id.

        Args:
            event_id (str): Identificador del evento a eliminar.

        Returns:
            bool: True si fue eliminado, False si no existía.

        Complejidad: O(n)
        """
        for i, evento in enumerate(self._eventos):
            if evento.event_id == event_id:
                self._eventos.pop(i)
                return True
        return False

    def listar(self):
        """
        Retorna todos los eventos almacenados.

        Returns:
            list[Event]: Copia de la lista de eventos.

        Complejidad: O(n)
        """
        return self._eventos[:]

    def tamanio(self):
        """
        Retorna la cantidad de eventos almacenados.

        Returns:
            int: Número de eventos en el store.

        Complejidad: O(1)
        """
        return len(self._eventos)

    def esta_vacio(self):
        """
        Indica si el store no tiene eventos.

        Returns:
            bool: True si está vacío, False si tiene eventos.

        Complejidad: O(1)
        """
        return len(self._eventos) == 0

    def __repr__(self):
        return f"EventStore(tamanio={self.tamanio()})"