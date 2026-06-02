# src/estructuras/bst.py

class NodoBST:
    """
    Nodo interno del árbol BST.

    Contiene un evento y referencias a sus hijos izquierdo y derecho.
    No tiene lógica propia: toda la lógica de ordenamiento y búsqueda
    vive en la clase BST.

    Atributos:
        evento (Event): El incidente almacenado en este nodo.
        izquierda (NodoBST): Hijo izquierdo (event_id menor).
        derecha (NodoBST): Hijo derecho (event_id mayor).
    """

    def __init__(self, evento):
        """
        Inicializa un nodo con un evento y sin hijos.

        Args:
            evento (Event): El incidente a almacenar.
        """
        self.evento = evento
        self.izquierda = None
        self.derecha = None


class BST:
    """
    Árbol Binario de Búsqueda (Binary Search Tree) ordenado por event_id.

    Permite insertar, buscar y eliminar eventos en O(log n) promedio,
    y recorrerlos en orden alfabético/numérico de event_id en O(n).

    A diferencia de un diccionario (O(1) búsqueda pero sin orden),
    el BST permite recorridos ordenados y búsquedas por rango sin
    costo adicional.

    Complejidades:
        insertar  → O(log n) promedio, O(n) peor caso (árbol degenerado)
        buscar    → O(log n) promedio, O(n) peor caso
        eliminar  → O(log n) promedio, O(n) peor caso
        inorden   → O(n)
        minimo    → O(log n)
        maximo    → O(log n)
    """

    def __init__(self):
        """Inicializa un árbol vacío."""
        self._raiz = None
        self._tamanio = 0

    # -----------------------------------------------------------------------
    # Insertar
    # -----------------------------------------------------------------------

    def insertar(self, evento):
        """
        Inserta un evento en el árbol respetando el orden por event_id.

        Si el event_id ya existe, reemplaza el evento existente.

        Args:
            evento (Event): El incidente a insertar.

        Complejidad: O(log n) promedio.
        """
        self._raiz, insertado = self._insertar_rec(self._raiz, evento)
        if insertado:
            self._tamanio += 1

    def _insertar_rec(self, nodo, evento):
        """
        Inserción recursiva. Retorna el nodo actualizado y si fue insertado.

        Args:
            nodo (NodoBST): Nodo actual en la recursión.
            evento (Event): El incidente a insertar.

        Returns:
            tuple: (nodo actualizado, bool indicando si fue nuevo)
        """
        if nodo is None:
            return NodoBST(evento), True

        if evento.event_id < nodo.evento.event_id:
            nodo.izquierda, insertado = self._insertar_rec(nodo.izquierda, evento)
        elif evento.event_id > nodo.evento.event_id:
            nodo.derecha, insertado = self._insertar_rec(nodo.derecha, evento)
        else:
            # event_id duplicado: reemplazar
            nodo.evento = evento
            insertado = False

        return nodo, insertado

    # -----------------------------------------------------------------------
    # Buscar
    # -----------------------------------------------------------------------

    def buscar(self, event_id):
        """
        Busca un evento por su event_id.

        Args:
            event_id (str): El identificador del incidente a buscar.

        Returns:
            Event: El evento encontrado, o None si no existe.

        Complejidad: O(log n) promedio.
        """
        nodo = self._buscar_rec(self._raiz, event_id)
        return nodo.evento if nodo else None

    def _buscar_rec(self, nodo, event_id):
        """
        Búsqueda recursiva por event_id.

        Args:
            nodo (NodoBST): Nodo actual en la recursión.
            event_id (str): El identificador a buscar.

        Returns:
            NodoBST: El nodo encontrado, o None si no existe.
        """
        if nodo is None or nodo.evento.event_id == event_id:
            return nodo

        if event_id < nodo.evento.event_id:
            return self._buscar_rec(nodo.izquierda, event_id)
        return self._buscar_rec(nodo.derecha, event_id)

    # -----------------------------------------------------------------------
    # Eliminar
    # -----------------------------------------------------------------------

    def eliminar(self, event_id):
        """
        Elimina el evento con el event_id dado.

        Maneja tres casos:
        - Nodo hoja: se elimina directamente.
        - Nodo con un hijo: se reemplaza por su hijo.
        - Nodo con dos hijos: se reemplaza por su sucesor inorden
          (el menor del subárbol derecho).

        Args:
            event_id (str): El identificador del incidente a eliminar.

        Complejidad: O(log n) promedio.
        """
        self._raiz, eliminado = self._eliminar_rec(self._raiz, event_id)
        if eliminado:
            self._tamanio -= 1

    def _eliminar_rec(self, nodo, event_id):
        """
        Eliminación recursiva. Retorna el nodo actualizado y si fue eliminado.

        Args:
            nodo (NodoBST): Nodo actual en la recursión.
            event_id (str): El identificador a eliminar.

        Returns:
            tuple: (nodo actualizado, bool indicando si fue eliminado)
        """
        if nodo is None:
            return None, False

        eliminado = False

        if event_id < nodo.evento.event_id:
            nodo.izquierda, eliminado = self._eliminar_rec(nodo.izquierda, event_id)
        elif event_id > nodo.evento.event_id:
            nodo.derecha, eliminado = self._eliminar_rec(nodo.derecha, event_id)
        else:
            # Nodo encontrado: manejar los tres casos
            eliminado = True

            # Caso 1 y 2: sin hijo izquierdo o sin hijo derecho
            if nodo.izquierda is None:
                return nodo.derecha, eliminado
            if nodo.derecha is None:
                return nodo.izquierda, eliminado

            # Caso 3: dos hijos → buscar sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._minimo_nodo(nodo.derecha)
            nodo.evento = sucesor.evento
            nodo.derecha, _ = self._eliminar_rec(nodo.derecha, sucesor.evento.event_id)

        return nodo, eliminado

    # -----------------------------------------------------------------------
    # Mínimo y máximo
    # -----------------------------------------------------------------------

    def minimo(self):
        """
        Retorna el evento con el event_id más pequeño.

        Returns:
            Event: El evento mínimo, o None si el árbol está vacío.

        Complejidad: O(log n).
        """
        if self._raiz is None:
            return None
        return self._minimo_nodo(self._raiz).evento

    def _minimo_nodo(self, nodo):
        """
        Retorna el nodo con el event_id más pequeño desde un nodo dado.
        Siempre es el nodo más a la izquierda.

        Args:
            nodo (NodoBST): Nodo desde donde buscar.

        Returns:
            NodoBST: El nodo más a la izquierda.
        """
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    def maximo(self):
        """
        Retorna el evento con el event_id más grande.

        Returns:
            Event: El evento máximo, o None si el árbol está vacío.

        Complejidad: O(log n).
        """
        if self._raiz is None:
            return None
        nodo = self._raiz
        while nodo.derecha is not None:
            nodo = nodo.derecha
        return nodo.evento

    # -----------------------------------------------------------------------
    # Recorrido inorden
    # -----------------------------------------------------------------------

    def inorden(self):
        """
        Retorna todos los eventos ordenados por event_id (ascendente).

        Recorre el árbol izquierda → raíz → derecha, lo que produce
        los elementos en orden natural del event_id.

        Returns:
            list[Event]: Lista de eventos ordenados.

        Complejidad: O(n).
        """
        resultado = []
        self._inorden_rec(self._raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        """
        Recorrido inorden recursivo.

        Args:
            nodo (NodoBST): Nodo actual.
            resultado (list): Lista donde se acumulan los eventos.
        """
        if nodo is not None:
            self._inorden_rec(nodo.izquierda, resultado)
            resultado.append(nodo.evento)
            self._inorden_rec(nodo.derecha, resultado)

    # -----------------------------------------------------------------------
    # Utilidades
    # -----------------------------------------------------------------------

    def esta_vacio(self):
        """
        Indica si el árbol no tiene elementos.

        Returns:
            bool: True si está vacío, False si tiene elementos.
        """
        return self._raiz is None

    def tamanio(self):
        """
        Retorna la cantidad de eventos en el árbol.

        Returns:
            int: Número de eventos almacenados.
        """
        return self._tamanio

    def __repr__(self):
        return f"BST(tamanio={self._tamanio})"