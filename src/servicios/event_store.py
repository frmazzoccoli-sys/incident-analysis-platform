from src.servicios.index import Index


class EventStore:
    """
    Almacena y gestiona la colección principal de eventos.

    Actúa como repositorio central del sistema. Todos los eventos
    ingresados al sistema pasan primero por EventStore antes de
    ser indexados o procesados por otros servicios.

    Atributos:
        _eventos (list): Lista interna de eventos almacenados.
        index (Index): Índice integrado para búsquedas rápidas.

    Operaciones principales:
        agregar   → O(1)
        obtener   → O(1) con índice
        eliminar  → O(n)
        listar    → O(1)
        buscar_por_categoria → O(1)
        buscar_por_origen   → O(1)
    """

    def __init__(self):
        """Inicializa un store e índice vacíos."""
        self._eventos = []
        self.index = Index()

    def agregar(self, evento):
        """
        Agrega un evento al store e indexa automáticamente sus claves.

        Si ya existe un evento con el mismo ID, reemplaza el registro
        anterior para mantener el store consistente.

        Args:
            evento (Event): El incidente a almacenar.

        Complejidad: O(1)
        """
        if self.index.buscar_por_id(evento.event_id) is not None:
            self.eliminar(evento.event_id)

        self._eventos.append(evento)
        self.index.agregar(evento)

    def obtener(self, event_id):
        """
        Busca y retorna un evento por su event_id.

        Args:
            event_id (str): Identificador del evento a buscar.

        Returns:
            Event: El evento encontrado, o None si no existe.

        Complejidad: O(1) a través del índice.
        """
        return self.index.buscar_por_id(event_id)

    def eliminar(self, event_id):
        """
        Elimina un evento del store y del índice por su event_id.

        Args:
            event_id (str): Identificador del evento a eliminar.

        Returns:
            bool: True si fue eliminado, False si no existía.

        Complejidad: O(n) para búsqueda en la lista + O(1) para eliminación en el índice.
        """
        for i, evento in enumerate(self._eventos):
            if evento.event_id == event_id:
                self._eventos.pop(i)
                self.index.eliminar(event_id)
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

    def buscar_por_categoria(self, categoria):
        """
        Retorna todos los eventos indexados por categoría.

        Args:
            categoria (str): La categoría a consultar.

        Returns:
            list[Event]: Lista de eventos de esa categoría.

        Complejidad: O(1)
        """
        return self.index.buscar_por_categoria(categoria)

    def buscar_por_origen(self, origen):
        """
        Retorna todos los eventos indexados por origen.

        Args:
            origen (str): El origen a consultar.

        Returns:
            list[Event]: Lista de eventos de ese origen.

        Complejidad: O(1)
        """
        return self.index.buscar_por_origen(origen)

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
        return f"EventStore(tamanio={self.tamanio()}, index={self.index})"
