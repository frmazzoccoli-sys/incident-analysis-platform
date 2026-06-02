# tests/test_estructuras.py

import pytest
from datetime import datetime
from src.modelos.event import Event
from src.estructuras.queue_eventos import QueueEventos
from src.estructuras.priority_queue import PriorityQueueEventos


# ---------------------------------------------------------------------------
# Fixtures: eventos reutilizables en todos los tests
# ---------------------------------------------------------------------------

@pytest.fixture
def evento_alto():
    """Evento de prioridad alta (1 = más crítico)."""
    return Event(
        event_id="E001",
        timestamp=datetime(2024, 1, 1, 10, 0, 0),
        categoria="seguridad",
        prioridad=1,
        texto="Acceso no autorizado detectado",
        origen="servidor-A",
        destino="base-datos"
    )

@pytest.fixture
def evento_medio():
    """Evento de prioridad media."""
    return Event(
        event_id="E002",
        timestamp=datetime(2024, 1, 1, 10, 5, 0),
        categoria="red",
        prioridad=3,
        texto="Latencia elevada en nodo",
        origen="router-B",
        destino="servidor-C"
    )

@pytest.fixture
def evento_bajo():
    """Evento de prioridad baja."""
    return Event(
        event_id="E003",
        timestamp=datetime(2024, 1, 1, 10, 10, 0),
        categoria="mantenimiento",
        prioridad=5,
        texto="Actualización de firmware pendiente",
        origen="nodo-D",
        destino="nodo-E"
    )


# ---------------------------------------------------------------------------
# Tests de QueueEventos (FIFO)
# ---------------------------------------------------------------------------

class TestQueueEventos:

    def test_cola_inicia_vacia(self):
        """Una cola recién creada debe estar vacía."""
        cola = QueueEventos()
        assert cola.esta_vacia() is True
        assert cola.tamanio() == 0

    def test_enqueue_aumenta_tamanio(self, evento_alto):
        """Agregar un evento debe incrementar el tamaño en 1."""
        cola = QueueEventos()
        cola.enqueue(evento_alto)
        assert cola.tamanio() == 1
        assert cola.esta_vacia() is False

    def test_orden_fifo(self, evento_alto, evento_medio, evento_bajo):
        """Los eventos deben salir en el mismo orden en que entraron."""
        cola = QueueEventos()
        cola.enqueue(evento_alto)
        cola.enqueue(evento_medio)
        cola.enqueue(evento_bajo)

        assert cola.dequeue().event_id == "E001"
        assert cola.dequeue().event_id == "E002"
        assert cola.dequeue().event_id == "E003"

    def test_peek_no_elimina(self, evento_alto, evento_medio):
        """peek() debe retornar el frente sin eliminarlo."""
        cola = QueueEventos()
        cola.enqueue(evento_alto)
        cola.enqueue(evento_medio)

        primero = cola.peek()
        assert primero.event_id == "E001"
        assert cola.tamanio() == 2

    def test_dequeue_vacia_la_cola(self, evento_alto):
        """Después de sacar el único elemento, la cola debe quedar vacía."""
        cola = QueueEventos()
        cola.enqueue(evento_alto)
        cola.dequeue()
        assert cola.esta_vacia() is True

    def test_dequeue_cola_vacia_lanza_error(self):
        """dequeue() en cola vacía debe lanzar IndexError."""
        cola = QueueEventos()
        with pytest.raises(IndexError):
            cola.dequeue()

    def test_peek_cola_vacia_lanza_error(self):
        """peek() en cola vacía debe lanzar IndexError."""
        cola = QueueEventos()
        with pytest.raises(IndexError):
            cola.peek()


# ---------------------------------------------------------------------------
# Tests de PriorityQueueEventos (min-heap por prioridad)
# ---------------------------------------------------------------------------

class TestPriorityQueueEventos:

    def test_pq_inicia_vacia(self):
        """Una PQ recién creada debe estar vacía."""
        pq = PriorityQueueEventos()
        assert pq.esta_vacia() is True
        assert pq.tamanio() == 0

    def test_push_aumenta_tamanio(self, evento_alto):
        """Insertar un evento debe incrementar el tamaño."""
        pq = PriorityQueueEventos()
        pq.push(evento_alto)
        assert pq.tamanio() == 1

    def test_pop_retorna_mas_prioritario(self, evento_alto, evento_medio, evento_bajo):
        """pop() debe retornar siempre el evento con menor número de prioridad."""
        pq = PriorityQueueEventos()
        pq.push(evento_bajo)
        pq.push(evento_alto)
        pq.push(evento_medio)

        assert pq.pop().event_id == "E001"
        assert pq.pop().event_id == "E002"
        assert pq.pop().event_id == "E003"

    def test_peek_no_elimina(self, evento_alto, evento_medio):
        """peek() debe retornar el más prioritario sin eliminarlo."""
        pq = PriorityQueueEventos()
        pq.push(evento_medio)
        pq.push(evento_alto)

        tope = pq.peek()
        assert tope.event_id == "E001"
        assert pq.tamanio() == 2

    def test_desempate_por_timestamp(self):
        """Ante igual prioridad, debe salir primero el evento más antiguo."""
        e_antiguo = Event("E010", datetime(2024, 1, 1, 8, 0), "red", 2, "txt", "A", "B")
        e_reciente = Event("E011", datetime(2024, 1, 1, 9, 0), "red", 2, "txt", "A", "B")

        pq = PriorityQueueEventos()
        pq.push(e_reciente)
        pq.push(e_antiguo)

        assert pq.pop().event_id == "E010"

    def test_desempate_mismo_timestamp(self):
        """Con igual prioridad y timestamp, no debe lanzar error (usa contador)."""
        e1 = Event("E020", datetime(2024, 1, 1, 8, 0), "red", 2, "txt", "A", "B")
        e2 = Event("E021", datetime(2024, 1, 1, 8, 0), "red", 2, "txt", "A", "B")

        pq = PriorityQueueEventos()
        pq.push(e1)
        pq.push(e2)

        primero = pq.pop()
        segundo = pq.pop()
        assert primero.event_id in ["E020", "E021"]
        assert segundo.event_id in ["E020", "E021"]
        assert primero.event_id != segundo.event_id

    def test_pop_vacia_lanza_error(self):
        """pop() en PQ vacía debe lanzar IndexError."""
        pq = PriorityQueueEventos()
        with pytest.raises(IndexError):
            pq.pop()

    def test_peek_vacia_lanza_error(self):
        """peek() en PQ vacía debe lanzar IndexError."""
        pq = PriorityQueueEventos()
        with pytest.raises(IndexError):
            pq.peek()

# ---------------------------------------------------------------------------
# Tests de BST
# ---------------------------------------------------------------------------
"""
El BST implementado organiza los eventos por event_id, permitiendo
inserción, búsqueda y eliminación en O(log n) promedio. Se eligió
event_id como clave de ordenamiento por ser el identificador único
del sistema, complementando la PriorityQueueEventos que ya cubre
el ordenamiento por prioridad. La eliminación maneja los tres casos
posibles (nodo hoja, un hijo y dos hijos), usando el sucesor inorden
para el caso más complejo, lo que garantiza que la propiedad BST se
preserve en todo momento. El recorrido inorden produce los eventos
ordenados alfabéticamente sin costo adicional, útil para reportes
y búsquedas por rango. Como limitación, en el peor caso (inserciones
en orden secuencial) el árbol puede degenerarse en una lista enlazada
con complejidad O(n); para producción se recomendaría un árbol
auto-balanceado como AVL o Red-Black.
"""

from src.estructuras.bst import BST

class TestBST:

    @pytest.fixture
    def arbol_con_eventos(self):
        """BST con cinco eventos insertados en orden no secuencial."""
        arbol = BST()
        arbol.insertar(Event("E004", datetime(2024, 1, 1, 10, 0), "red", 2, "txt", "A", "B"))
        arbol.insertar(Event("E002", datetime(2024, 1, 1, 11, 0), "red", 3, "txt", "A", "B"))
        arbol.insertar(Event("E006", datetime(2024, 1, 1, 12, 0), "red", 1, "txt", "A", "B"))
        arbol.insertar(Event("E001", datetime(2024, 1, 1, 13, 0), "red", 5, "txt", "A", "B"))
        arbol.insertar(Event("E005", datetime(2024, 1, 1, 14, 0), "red", 4, "txt", "A", "B"))
        return arbol

    def test_arbol_inicia_vacio(self):
        """Un BST recién creado debe estar vacío."""
        arbol = BST()
        assert arbol.esta_vacio() is True
        assert arbol.tamanio() == 0

    def test_insertar_aumenta_tamanio(self):
        """Insertar un evento debe incrementar el tamaño."""
        arbol = BST()
        arbol.insertar(Event("E001", datetime(2024, 1, 1), "red", 1, "txt", "A", "B"))
        assert arbol.tamanio() == 1
        assert arbol.esta_vacio() is False

    def test_insertar_duplicado_no_aumenta_tamanio(self, arbol_con_eventos):
        """Insertar un event_id duplicado reemplaza el evento sin aumentar tamaño."""
        tamanio_antes = arbol_con_eventos.tamanio()
        arbol_con_eventos.insertar(Event("E002", datetime(2024, 1, 1), "seguridad", 1, "nuevo", "X", "Y"))
        assert arbol_con_eventos.tamanio() == tamanio_antes

    def test_insertar_duplicado_reemplaza_evento(self, arbol_con_eventos):
        """Insertar un event_id duplicado debe actualizar el evento."""
        nuevo = Event("E002", datetime(2024, 1, 1), "seguridad", 1, "nuevo", "X", "Y")
        arbol_con_eventos.insertar(nuevo)
        encontrado = arbol_con_eventos.buscar("E002")
        assert encontrado.categoria == "seguridad"
        assert encontrado.texto == "nuevo"

    def test_buscar_evento_existente(self, arbol_con_eventos):
        """Buscar un event_id existente debe retornar el evento correcto."""
        evento = arbol_con_eventos.buscar("E004")
        assert evento is not None
        assert evento.event_id == "E004"

    def test_buscar_evento_inexistente(self, arbol_con_eventos):
        """Buscar un event_id que no existe debe retornar None."""
        evento = arbol_con_eventos.buscar("E999")
        assert evento is None

    def test_inorden_retorna_eventos_ordenados(self, arbol_con_eventos):
        """inorden() debe retornar los eventos ordenados por event_id."""
        eventos = arbol_con_eventos.inorden()
        ids = [e.event_id for e in eventos]
        assert ids == sorted(ids)

    def test_inorden_contiene_todos_los_eventos(self, arbol_con_eventos):
        """inorden() debe retornar todos los eventos insertados."""
        eventos = arbol_con_eventos.inorden()
        assert len(eventos) == arbol_con_eventos.tamanio()

    def test_minimo(self, arbol_con_eventos):
        """minimo() debe retornar el evento con el event_id más pequeño."""
        assert arbol_con_eventos.minimo().event_id == "E001"

    def test_maximo(self, arbol_con_eventos):
        """maximo() debe retornar el evento con el event_id más grande."""
        assert arbol_con_eventos.maximo().event_id == "E006"

    def test_eliminar_hoja(self, arbol_con_eventos):
        """Eliminar un nodo hoja no debe afectar el resto del árbol."""
        arbol_con_eventos.eliminar("E001")
        assert arbol_con_eventos.buscar("E001") is None
        assert arbol_con_eventos.tamanio() == 4

    def test_eliminar_nodo_con_un_hijo(self, arbol_con_eventos):
        """Eliminar un nodo con un solo hijo debe reemplazarlo por ese hijo."""
        arbol_con_eventos.eliminar("E002")
        assert arbol_con_eventos.buscar("E002") is None
        assert arbol_con_eventos.buscar("E001") is not None
        assert arbol_con_eventos.tamanio() == 4

    def test_eliminar_nodo_con_dos_hijos(self, arbol_con_eventos):
        """Eliminar un nodo con dos hijos debe mantener la propiedad BST."""
        arbol_con_eventos.eliminar("E004")
        assert arbol_con_eventos.buscar("E004") is None
        assert arbol_con_eventos.tamanio() == 4
        # verificar que el árbol sigue ordenado
        ids = [e.event_id for e in arbol_con_eventos.inorden()]
        assert ids == sorted(ids)

    def test_eliminar_inexistente_no_cambia_tamanio(self, arbol_con_eventos):
        """Eliminar un event_id que no existe no debe cambiar el tamaño."""
        tamanio_antes = arbol_con_eventos.tamanio()
        arbol_con_eventos.eliminar("E999")
        assert arbol_con_eventos.tamanio() == tamanio_antes

    def test_minimo_arbol_vacio(self):
        """minimo() en árbol vacío debe retornar None."""
        arbol = BST()
        assert arbol.minimo() is None

    def test_maximo_arbol_vacio(self):
        """maximo() en árbol vacío debe retornar None."""
        arbol = BST()
        assert arbol.maximo() is None

from src.algoritmos.busqueda import busqueda_secuencial, busqueda_binaria
from src.algoritmos.ordenamiento import burbuja, mergesort


class TestBusqueda:

    @pytest.fixture
    def lista_eventos(self):
        """Lista de eventos en orden no secuencial."""
        return [
            Event("E003", datetime(2024, 1, 1, 10, 0), "red", 2, "txt", "A", "B"),
            Event("E001", datetime(2024, 1, 1, 11, 0), "red", 1, "txt", "A", "B"),
            Event("E005", datetime(2024, 1, 1, 12, 0), "red", 3, "txt", "A", "B"),
            Event("E002", datetime(2024, 1, 1, 13, 0), "red", 4, "txt", "A", "B"),
            Event("E004", datetime(2024, 1, 1, 14, 0), "red", 5, "txt", "A", "B"),
        ]

    @pytest.fixture
    def lista_ordenada(self, lista_eventos):
        """Lista de eventos ordenada por event_id para búsqueda binaria."""
        return sorted(lista_eventos, key=lambda e: e.event_id)

    def test_secuencial_encuentra_evento(self, lista_eventos):
        """La búsqueda secuencial debe encontrar un evento existente."""
        resultado = busqueda_secuencial(lista_eventos, "E003")
        assert resultado is not None
        assert resultado.event_id == "E003"

    def test_secuencial_retorna_none_si_no_existe(self, lista_eventos):
        """La búsqueda secuencial debe retornar None si no existe el evento."""
        resultado = busqueda_secuencial(lista_eventos, "E999")
        assert resultado is None

    def test_secuencial_encuentra_primero(self, lista_eventos):
        """La búsqueda secuencial debe encontrar el primer elemento."""
        resultado = busqueda_secuencial(lista_eventos, "E003")
        assert resultado.event_id == "E003"

    def test_secuencial_encuentra_ultimo(self, lista_eventos):
        """La búsqueda secuencial debe encontrar el último elemento."""
        resultado = busqueda_secuencial(lista_eventos, "E004")
        assert resultado.event_id == "E004"

    def test_binaria_encuentra_evento(self, lista_ordenada):
        """La búsqueda binaria debe encontrar un evento existente."""
        resultado = busqueda_binaria(lista_ordenada, "E003")
        assert resultado is not None
        assert resultado.event_id == "E003"

    def test_binaria_retorna_none_si_no_existe(self, lista_ordenada):
        """La búsqueda binaria debe retornar None si no existe el evento."""
        resultado = busqueda_binaria(lista_ordenada, "E999")
        assert resultado is None

    def test_binaria_encuentra_primero(self, lista_ordenada):
        """La búsqueda binaria debe encontrar el primer elemento."""
        resultado = busqueda_binaria(lista_ordenada, "E001")
        assert resultado.event_id == "E001"

    def test_binaria_encuentra_ultimo(self, lista_ordenada):
        """La búsqueda binaria debe encontrar el último elemento."""
        resultado = busqueda_binaria(lista_ordenada, "E005")
        assert resultado.event_id == "E005"

    def test_ambas_busquedas_mismo_resultado(self, lista_eventos, lista_ordenada):
        """Ambas búsquedas deben retornar el mismo evento para el mismo event_id."""
        event_id = "E003"
        resultado_sec = busqueda_secuencial(lista_eventos, event_id)
        resultado_bin = busqueda_binaria(lista_ordenada, event_id)
        assert resultado_sec.event_id == resultado_bin.event_id


# ---------------------------------------------------------------------------
# Tests de Ordenamiento
# ---------------------------------------------------------------------------

class TestOrdenamiento:

    @pytest.fixture
    def eventos_desordenados(self):
        """Lista de eventos con timestamps en orden no secuencial."""
        return [
            Event("E003", datetime(2024, 1, 1, 12, 0), "red", 2, "txt", "A", "B"),
            Event("E001", datetime(2024, 1, 1, 10, 0), "red", 1, "txt", "A", "B"),
            Event("E005", datetime(2024, 1, 1, 14, 0), "red", 3, "txt", "A", "B"),
            Event("E002", datetime(2024, 1, 1, 11, 0), "red", 4, "txt", "A", "B"),
            Event("E004", datetime(2024, 1, 1, 13, 0), "red", 5, "txt", "A", "B"),
        ]

    @pytest.fixture
    def timestamps_esperados(self):
        """Timestamps en orden ascendente esperado."""
        return [
            datetime(2024, 1, 1, 10, 0),
            datetime(2024, 1, 1, 11, 0),
            datetime(2024, 1, 1, 12, 0),
            datetime(2024, 1, 1, 13, 0),
            datetime(2024, 1, 1, 14, 0),
        ]

    def test_burbuja_ordena_correctamente(self, eventos_desordenados, timestamps_esperados):
        """Burbuja debe ordenar los eventos por timestamp ascendente."""
        resultado = burbuja(eventos_desordenados)
        timestamps = [e.timestamp for e in resultado]
        assert timestamps == timestamps_esperados

    def test_burbuja_no_modifica_original(self, eventos_desordenados):
        """Burbuja no debe modificar la lista original."""
        original = [e.timestamp for e in eventos_desordenados]
        burbuja(eventos_desordenados)
        assert [e.timestamp for e in eventos_desordenados] == original

    def test_burbuja_lista_vacia(self):
        """Burbuja debe manejar una lista vacía sin error."""
        assert burbuja([]) == []

    def test_burbuja_un_elemento(self):
        """Burbuja debe manejar una lista de un solo elemento."""
        evento = Event("E001", datetime(2024, 1, 1), "red", 1, "txt", "A", "B")
        assert burbuja([evento])[0].event_id == "E001"

    def test_mergesort_ordena_correctamente(self, eventos_desordenados, timestamps_esperados):
        """Mergesort debe ordenar los eventos por timestamp ascendente."""
        resultado = mergesort(eventos_desordenados)
        timestamps = [e.timestamp for e in resultado]
        assert timestamps == timestamps_esperados

    def test_mergesort_no_modifica_original(self, eventos_desordenados):
        """Mergesort no debe modificar la lista original."""
        original = [e.timestamp for e in eventos_desordenados]
        mergesort(eventos_desordenados)
        assert [e.timestamp for e in eventos_desordenados] == original

    def test_mergesort_lista_vacia(self):
        """Mergesort debe manejar una lista vacía sin error."""
        assert mergesort([]) == []

    def test_mergesort_un_elemento(self):
        """Mergesort debe manejar una lista de un solo elemento."""
        evento = Event("E001", datetime(2024, 1, 1), "red", 1, "txt", "A", "B")
        assert mergesort([evento])[0].event_id == "E001"

    def test_burbuja_y_mergesort_mismo_resultado(self, eventos_desordenados):
        """Burbuja y mergesort deben producir el mismo orden."""
        resultado_burbuja = [e.timestamp for e in burbuja(eventos_desordenados)]
        resultado_mergesort = [e.timestamp for e in mergesort(eventos_desordenados)]
        assert resultado_burbuja == resultado_mergesort

    def test_ambos_coinciden_con_sorted(self, eventos_desordenados):
        """Ambos algoritmos deben coincidir con sorted() de Python."""
        esperado = [e.timestamp for e in sorted(eventos_desordenados, key=lambda e: e.timestamp)]
        resultado_burbuja = [e.timestamp for e in burbuja(eventos_desordenados)]
        resultado_mergesort = [e.timestamp for e in mergesort(eventos_desordenados)]
        assert resultado_burbuja == esperado
        assert resultado_mergesort == esperado