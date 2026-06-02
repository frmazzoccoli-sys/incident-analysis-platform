from src.metricas.reporte import (
    mostrar_busquedas,
    mostrar_ordenamientos,
    mostrar_memoria,
    mostrar_analisis,
)


def test_mostrar_busquedas_formatea_salida(capsys):
    resultados = [{
        "n": 10,
        "secuencial": 0.001234,
        "binaria": 0.000123,
        "bst": 0.000234,
        "hashing": 0.000012,
    }]
    mostrar_busquedas(resultados)
    salida = capsys.readouterr().out

    assert "BENCHMARK DE ALGORITMOS - BÚSQUEDA" in salida
    assert "10" in salida
    assert "0.001234s" in salida


def test_mostrar_ordenamientos_formatea_salida(capsys):
    resultados = [{
        "n": 10,
        "burbuja": 0.012345,
        "mergesort": 0.001234,
        "sorted": 0.000123,
    }]
    mostrar_ordenamientos(resultados)
    salida = capsys.readouterr().out

    assert "BENCHMARK DE ALGORITMOS - ORDENAMIENTO" in salida
    assert "10" in salida
    assert "0.001234s" in salida


def test_mostrar_memoria_formatea_salida(capsys):
    resultados = [{
        "n": 10,
        "burbuja": 1.23,
        "mergesort": 4.56,
        "sorted": 7.89,
    }]
    mostrar_memoria(resultados)
    salida = capsys.readouterr().out

    assert "BENCHMARK DE MEMORIA - ORDENAMIENTO" in salida
    assert "1.23KB" in salida
    assert "7.89KB" in salida


def test_mostrar_analisis_imprime_resumen(capsys):
    mostrar_analisis()
    salida = capsys.readouterr().out

    assert "ANÁLISIS DE RESULTADOS" in salida
    assert "BÚSQUEDA:" in salida
    assert "ORDENAMIENTO:" in salida
