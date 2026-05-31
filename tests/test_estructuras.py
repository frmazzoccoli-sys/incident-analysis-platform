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
