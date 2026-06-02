import pytest
from datetime import datetime

from src.modelos.event import Event
from src.algoritmos.busqueda import busqueda_secuencial, busqueda_binaria
from src.algoritmos.ordenamiento import burbuja, mergesort


def test_busqueda_secuencial_encuentra_evento():
    eventos = [
        Event("E002", datetime(2024, 1, 1, 10, 0), "seguridad", 2, "txt", "A", "B"),
        Event("E001", datetime(2024, 1, 1, 11, 0), "seguridad", 2, "txt", "A", "B"),
    ]

    resultado = busqueda_secuencial(eventos, "E001")
    assert resultado is not None
    assert resultado.event_id == "E001"


def test_busqueda_secuencial_no_encuentra_evento():
    eventos = [
        Event("E002", datetime(2024, 1, 1, 10, 0), "seguridad", 2, "txt", "A", "B"),
        Event("E001", datetime(2024, 1, 1, 11, 0), "seguridad", 2, "txt", "A", "B"),
    ]

    assert busqueda_secuencial(eventos, "E999") is None


def test_busqueda_binaria_encuentra_evento():
    eventos_ordenados = [
        Event("E001", datetime(2024, 1, 1, 10, 0), "seguridad", 2, "txt", "A", "B"),
        Event("E002", datetime(2024, 1, 1, 11, 0), "seguridad", 2, "txt", "A", "B"),
        Event("E003", datetime(2024, 1, 1, 12, 0), "seguridad", 2, "txt", "A", "B"),
    ]

    resultado = busqueda_binaria(eventos_ordenados, "E002")
    assert resultado is not None
    assert resultado.event_id == "E002"


def test_busqueda_binaria_no_encuentra_evento():
    eventos_ordenados = [
        Event("E001", datetime(2024, 1, 1, 10, 0), "seguridad", 2, "txt", "A", "B"),
        Event("E002", datetime(2024, 1, 1, 11, 0), "seguridad", 2, "txt", "A", "B"),
    ]

    assert busqueda_binaria(eventos_ordenados, "E999") is None


def test_burbuja_ordenamiento_preserva_lista_original():
    eventos = [
        Event("E003", datetime(2024, 1, 1, 12, 0), "red", 3, "txt", "A", "B"),
        Event("E001", datetime(2024, 1, 1, 10, 0), "red", 3, "txt", "A", "B"),
        Event("E002", datetime(2024, 1, 1, 11, 0), "red", 3, "txt", "A", "B"),
    ]

    resultado = burbuja(eventos)
    assert [e.event_id for e in resultado] == ["E001", "E002", "E003"]
    assert [e.event_id for e in eventos] == ["E003", "E001", "E002"]


def test_mergesort_ordenamiento():
    eventos = [
        Event("E003", datetime(2024, 1, 1, 12, 0), "red", 3, "txt", "A", "B"),
        Event("E001", datetime(2024, 1, 1, 10, 0), "red", 3, "txt", "A", "B"),
        Event("E002", datetime(2024, 1, 1, 11, 0), "red", 3, "txt", "A", "B"),
    ]

    resultado = mergesort(eventos)
    assert [e.event_id for e in resultado] == ["E001", "E002", "E003"]
    assert [e.event_id for e in eventos] == ["E003", "E001", "E002"]
