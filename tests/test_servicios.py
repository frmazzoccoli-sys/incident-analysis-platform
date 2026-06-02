# tests/test_servicios.py

import pytest
from datetime import datetime
from src.modelos.event import Event
from src.servicios.event_store import EventStore
from src.servicios.index import Index
from src.servicios.router import Router
from src.servicios.text_analyzer import TextAnalyzer
from src.estructuras.priority_queue import PriorityQueueEventos


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def e1():
    return Event("E001", datetime(2024, 1, 1, 10, 0), "seguridad", 1,
                 "Acceso no autorizado detectado", "servidor-A", "base-datos")

@pytest.fixture
def e2():
    return Event("E002", datetime(2024, 1, 1, 11, 0), "red", 3,
                 "Latencia elevada en nodo", "router-B", "servidor-C")

@pytest.fixture
def e3():
    return Event("E003", datetime(2024, 1, 1, 12, 0), "seguridad", 2,
                 "Intento de acceso fallido", "servidor-A", "servidor-C")

@pytest.fixture
def tres_eventos(e1, e2, e3):
    return [e1, e2, e3]


# ---------------------------------------------------------------------------
# Tests de EventStore
# ---------------------------------------------------------------------------

class TestEventStore:

    def test_store_inicia_vacio(self):
        store = EventStore()
        assert store.esta_vacio() is True
        assert store.tamanio() == 0

    def test_agregar_aumenta_tamanio(self, e1):
        store = EventStore()
        store.agregar(e1)
        assert store.tamanio() == 1
        assert store.esta_vacio() is False

    def test_obtener_evento_existente(self, e1):
        store = EventStore()
        store.agregar(e1)
        resultado = store.obtener("E001")
        assert resultado is not None
        assert resultado.event_id == "E001"

    def test_obtener_evento_inexistente(self, e1):
        store = EventStore()
        store.agregar(e1)
        assert store.obtener("E999") is None

    def test_eliminar_evento_existente(self, e1):
        store = EventStore()
        store.agregar(e1)
        eliminado = store.eliminar("E001")
        assert eliminado is True
        assert store.tamanio() == 0

    def test_eliminar_evento_inexistente(self, e1):
        store = EventStore()
        store.agregar(e1)
        eliminado = store.eliminar("E999")
        assert eliminado is False
        assert store.tamanio() == 1

    def test_listar_retorna_todos(self, tres_eventos):
        store = EventStore()
        for e in tres_eventos:
            store.agregar(e)
        lista = store.listar()
        assert len(lista) == 3

    def test_listar_no_modifica_store(self, e1):
        store = EventStore()
        store.agregar(e1)
        lista = store.listar()
        lista.clear()
        assert store.tamanio() == 1

    def test_eventstore_actualiza_indice_automaticamente(self, e1):
        store = EventStore()
        store.agregar(e1)

        assert store.obtener("E001") is e1
        assert store.buscar_por_categoria("seguridad") == [e1]
        assert store.buscar_por_origen("servidor-A") == [e1]

    def test_flow_crear_almacenar_indexar_analizar_priorizar(self, e1, e2):
        store = EventStore()
        analyzer = TextAnalyzer()
        queue = PriorityQueueEventos()

        store.agregar(e1)
        store.agregar(e2)

        eventos_seguridad = store.buscar_por_categoria("seguridad")
        eventos_latencia = analyzer.buscar_por_palabra(store.listar(), "latencia")

        assert eventos_seguridad == [e1]
        assert eventos_latencia == [e2]

        queue.push(e1)
        queue.push(e2)

        primero = queue.pop()
        assert primero.event_id == "E001"
        assert queue.tamanio() == 1


# ---------------------------------------------------------------------------
# Tests de Index
# ---------------------------------------------------------------------------

class TestIndex:

    def test_index_inicia_vacio(self):
        index = Index()
        assert index.tamanio() == 0

    def test_agregar_indexa_por_id(self, e1):
        index = Index()
        index.agregar(e1)
        assert index.buscar_por_id("E001") is not None
        assert index.buscar_por_id("E001").event_id == "E001"

    def test_agregar_indexa_por_categoria(self, e1, e3):
        index = Index()
        index.agregar(e1)
        index.agregar(e3)
        resultados = index.buscar_por_categoria("seguridad")
        assert len(resultados) == 2

    def test_agregar_indexa_por_origen(self, e1, e3):
        index = Index()
        index.agregar(e1)
        index.agregar(e3)
        resultados = index.buscar_por_origen("servidor-A")
        assert len(resultados) == 2

    def test_buscar_id_inexistente(self, e1):
        index = Index()
        index.agregar(e1)
        assert index.buscar_por_id("E999") is None

    def test_buscar_categoria_inexistente(self, e1):
        index = Index()
        index.agregar(e1)
        assert index.buscar_por_categoria("inexistente") == []

    def test_buscar_origen_inexistente(self, e1):
        index = Index()
        index.agregar(e1)
        assert index.buscar_por_origen("inexistente") == []

    def test_eliminar_evento(self, e1):
        index = Index()
        index.agregar(e1)
        eliminado = index.eliminar("E001")
        assert eliminado is True
        assert index.buscar_por_id("E001") is None
        assert index.tamanio() == 0

    def test_eliminar_limpia_categoria(self, e1):
        index = Index()
        index.agregar(e1)
        index.eliminar("E001")
        assert index.buscar_por_categoria("seguridad") == []

    def test_eliminar_limpia_origen(self, e1):
        index = Index()
        index.agregar(e1)
        index.eliminar("E001")
        assert index.buscar_por_origen("servidor-A") == []

    def test_eliminar_inexistente(self, e1):
        index = Index()
        index.agregar(e1)
        assert index.eliminar("E999") is False
        assert index.tamanio() == 1


# ---------------------------------------------------------------------------
# Tests de Router
# ---------------------------------------------------------------------------

class TestRouter:

    def test_router_inicia_vacio(self):
        router = Router()
        assert router.tamanio() == 0

    def test_registrar_ruta(self, e1):
        router = Router()
        router.registrar(e1)
        assert router.tamanio() == 1

    def test_consultar_ruta_existente(self, e1):
        router = Router()
        router.registrar(e1)
        resultados = router.consultar("servidor-A", "base-datos")
        assert len(resultados) == 1
        assert resultados[0].event_id == "E001"

    def test_consultar_ruta_inexistente(self, e1):
        router = Router()
        router.registrar(e1)
        assert router.consultar("X", "Y") == []

    def test_ruta_mas_activa(self, e1, e3):
        router = Router()
        router.registrar(e1)
        router.registrar(e3)
        ruta, cantidad = router.ruta_mas_activa()
        assert cantidad >= 1

    def test_ruta_mas_activa_sin_rutas(self):
        router = Router()
        assert router.ruta_mas_activa() is None

    def test_listar_rutas(self, tres_eventos):
        router = Router()
        for e in tres_eventos:
            router.registrar(e)
        rutas = router.listar_rutas()
        assert len(rutas) > 0


# ---------------------------------------------------------------------------
# Tests de TextAnalyzer
# ---------------------------------------------------------------------------

class TestTextAnalyzer:

    def test_buscar_por_palabra_encuentra(self, tres_eventos):
        analyzer = TextAnalyzer()
        resultados = analyzer.buscar_por_palabra(tres_eventos, "acceso")
        assert len(resultados) == 2

    def test_buscar_por_palabra_case_insensitive(self, tres_eventos):
        analyzer = TextAnalyzer()
        resultados = analyzer.buscar_por_palabra(tres_eventos, "ACCESO")
        assert len(resultados) == 2

    def test_buscar_por_palabra_sin_resultados(self, tres_eventos):
        analyzer = TextAnalyzer()
        resultados = analyzer.buscar_por_palabra(tres_eventos, "xyz")
        assert resultados == []

    def test_buscar_por_patron(self, tres_eventos):
        analyzer = TextAnalyzer()
        resultados = analyzer.buscar_por_patron(tres_eventos, "latencia elevada")
        assert len(resultados) == 1
        assert resultados[0].event_id == "E002"

    def test_palabras_frecuentes(self, tres_eventos):
        analyzer = TextAnalyzer()
        frecuentes = analyzer.palabras_frecuentes(tres_eventos, top=5)
        assert len(frecuentes) <= 5
        assert isinstance(frecuentes[0], tuple)
        # la palabra más frecuente debe tener mayor o igual frecuencia que la segunda
        if len(frecuentes) > 1:
            assert frecuentes[0][1] >= frecuentes[1][1]