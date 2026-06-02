# src/servicios/index.py


class Index:
    """
    Índice hash para búsquedas rápidas de eventos por distintas claves.

    Mantiene tres diccionarios internos que actúan como índices invertidos:
    - by_id:       clave única, retorna un solo evento.
    - by_category: clave múltiple, retorna lista de eventos.
    - by_origin:   clave múltiple, retorna lista de eventos.

    Los diccionarios de Python implementan tablas de hash internamente,
    lo que garantiza búsquedas en O(1) promedio. Esto contrasta con la
    búsqueda secuencial O(n) de EventStore y la búsqueda binaria O(log n).

    Sobre colisiones:
        Python maneja colisiones internamente mediante direccionamiento
        abierto (open addressing). Cuando dos claves producen el mismo
        hash, Python busca la siguiente posición disponible en la tabla.
        En la práctica, con un factor de carga bajo, las colisiones son
        raras y el rendimiento se mantiene en O(1) promedio.

    Operaciones principales:
        agregar            → O(1)
        buscar_por_id      → O(1)
        buscar_por_categoria → O(1)
        buscar_por_origen  → O(1)
        eliminar           → O(1) buscar + O(k) eliminar de lista
    """

    def __init__(self):
        """Inicializa los tres índices vacíos."""
        self.by_id = {}
        self.by_category = {}
        self.by_origin = {}

    def agregar(self, evento):
        """
        Indexa un evento en los tres índices simultáneamente.

        Para by_id guarda el evento directamente ya que el ID es único.
        Para by_category y by_origin guarda listas porque múltiples
        eventos pueden compartir la misma categoría u origen.

        Args:
            evento (Event): El incidente a indexar.

        Complejidad: O(1)
        """
        # Índice por ID: clave única
        self.by_id[evento.event_id] = evento

        # Índice por categoría: clave múltiple
        if evento.categoria not in self.by_category:
            self.by_category[evento.categoria] = []
        self.by_category[evento.categoria].append(evento)

        # Índice por origen: clave múltiple
        if evento.origen not in self.by_origin:
            self.by_origin[evento.origen] = []
        self.by_origin[evento.origen].append(evento)

    def buscar_por_id(self, event_id):
        """
        Retorna el evento con el event_id dado.

        Args:
            event_id (str): Identificador del evento a buscar.

        Returns:
            Event: El evento encontrado, o None si no existe.

        Complejidad: O(1)
        """
        return self.by_id.get(event_id, None)

    def buscar_por_categoria(self, categoria):
        """
        Retorna todos los eventos de una categoría dada.

        Args:
            categoria (str): La categoría a consultar.

        Returns:
            list[Event]: Lista de eventos de esa categoría,
                         o lista vacía si no existe.

        Complejidad: O(1)
        """
        return self.by_category.get(categoria, [])

    def buscar_por_origen(self, origen):
        """
        Retorna todos los eventos de un origen dado.

        Args:
            origen (str): El origen a consultar.

        Returns:
            list[Event]: Lista de eventos de ese origen,
                         o lista vacía si no existe.

        Complejidad: O(1)
        """
        return self.by_origin.get(origen, [])

    def eliminar(self, event_id):
        """
        Elimina un evento de los tres índices.

        Busca primero en by_id para obtener el evento completo,
        luego lo elimina de by_category y by_origin.

        Args:
            event_id (str): Identificador del evento a eliminar.

        Returns:
            bool: True si fue eliminado, False si no existía.

        Complejidad: O(1) para by_id + O(k) para listas,
                     donde k es la cantidad de eventos en esa categoría/origen.
        """
        evento = self.by_id.get(event_id)
        if evento is None:
            return False

        # Eliminar de by_id
        del self.by_id[event_id]

        # Eliminar de by_category
        categoria = evento.categoria
        if categoria in self.by_category:
            self.by_category[categoria] = [
                e for e in self.by_category[categoria]
                if e.event_id != event_id
            ]
            if not self.by_category[categoria]:
                del self.by_category[categoria]

        # Eliminar de by_origin
        origen = evento.origen
        if origen in self.by_origin:
            self.by_origin[origen] = [
                e for e in self.by_origin[origen]
                if e.event_id != event_id
            ]
            if not self.by_origin[origen]:
                del self.by_origin[origen]

        return True

    def tamanio(self):
        """
        Retorna la cantidad de eventos indexados.

        Returns:
            int: Número de eventos en el índice.

        Complejidad: O(1)
        """
        return len(self.by_id)

    def __repr__(self):
        return f"Index(tamanio={self.tamanio()})"