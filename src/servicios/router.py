# src/servicios/router.py


class Router:
    """
    Maneja consultas de rutas entre nodos origen y destino.

    Almacena pares origen-destino de los eventos procesados,
    permitiendo consultar qué rutas existen en el sistema y
    cuántos eventos transitaron por cada una.

    Utiliza un diccionario donde la clave es una tupla (origen, destino)
    y el valor es la lista de eventos que transitaron esa ruta.

    Operaciones principales:
        registrar        → O(1)
        consultar        → O(1)
        listar_rutas     → O(r) donde r es el número de rutas únicas
        ruta_mas_activa  → O(r)
    """

    def __init__(self):
        """Inicializa el router sin rutas registradas."""
        self._rutas = {}

    def registrar(self, evento):
        """
        Registra la ruta origen-destino de un evento.

        Args:
            evento (Event): El incidente cuya ruta se registra.

        Complejidad: O(1)
        """
        clave = (evento.origen, evento.destino)
        if clave not in self._rutas:
            self._rutas[clave] = []
        self._rutas[clave].append(evento)

    def consultar(self, origen, destino):
        """
        Retorna todos los eventos que transitaron una ruta dada.

        Args:
            origen (str): Nodo de origen.
            destino (str): Nodo de destino.

        Returns:
            list[Event]: Lista de eventos en esa ruta,
                         o lista vacía si no existe.

        Complejidad: O(1)
        """
        return self._rutas.get((origen, destino), [])

    def listar_rutas(self):
        """
        Retorna todas las rutas registradas con su cantidad de eventos.

        Returns:
            list[tuple]: Lista de ((origen, destino), cantidad).

        Complejidad: O(r) donde r es el número de rutas únicas.
        """
        return [
            (ruta, len(eventos))
            for ruta, eventos in self._rutas.items()
        ]

    def ruta_mas_activa(self):
        """
        Retorna la ruta con mayor cantidad de eventos registrados.

        Returns:
            tuple: ((origen, destino), cantidad), o None si no hay rutas.

        Complejidad: O(r)
        """
        if not self._rutas:
            return None
        ruta = max(self._rutas, key=lambda r: len(self._rutas[r]))
        return (ruta, len(self._rutas[ruta]))

    def tamanio(self):
        """
        Retorna la cantidad de rutas únicas registradas.

        Returns:
            int: Número de rutas únicas.

        Complejidad: O(1)
        """
        return len(self._rutas)

    def __repr__(self):
        return f"Router(rutas={self.tamanio()})"