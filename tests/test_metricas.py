import os
from importlib.util import spec_from_file_location, module_from_spec

from src.metricas.medidor import (
    generar_eventos,
    medir_tiempo,
    medir_memoria,
    benchmark_busquedas,
    benchmark_ordenamientos,
    benchmark_memoria,
)


def test_generar_eventos_genera_cantidad_y_ids_unicos():
    eventos = generar_eventos(10)
    assert len(eventos) == 10
    assert len({evento.event_id for evento in eventos}) == 10


def test_medir_tiempo_retorna_numero_positivo():
    tiempo = medir_tiempo(lambda: 1 + 1, repeticiones=10)
    assert isinstance(tiempo, float)
    assert tiempo >= 0


def test_medir_memoria_retorna_kbytes():
    memoria = medir_memoria(lambda: [0] * 1000)
    assert isinstance(memoria, float)
    assert memoria >= 0


def test_benchmark_busquedas_retorna_estructura_correcta():
    resultados = benchmark_busquedas([5])
    assert isinstance(resultados, list)
    assert len(resultados) == 1
    assert set(resultados[0].keys()) == {"n", "secuencial", "binaria", "bst", "hashing"}


def test_benchmark_ordenamientos_retorna_estructura_correcta():
    resultados = benchmark_ordenamientos([5])
    assert isinstance(resultados, list)
    assert len(resultados) == 1
    assert set(resultados[0].keys()) == {"n", "burbuja", "mergesort", "sorted"}


def test_benchmark_memoria_retorna_estructura_correcta():
    resultados = benchmark_memoria([5])
    assert isinstance(resultados, list)
    assert len(resultados) == 1
    assert set(resultados[0].keys()) == {"n", "burbuja", "mergesort", "sorted"}


def test_benchmark_script_importable():
    path = os.path.join(os.path.dirname(__file__), os.pardir, "benchmarks", "benchmark.py")
    path = os.path.abspath(path)
    spec = spec_from_file_location("benchmark_script", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "TAMANIOS")
    assert module.TAMANIOS == [100, 500, 1000, 2000, 5000]
