# src/algoritmos/ordenamiento.py


def burbuja(eventos):
    """
    Ordena una lista de eventos por timestamp usando el algoritmo de burbuja.

    Compara pares adyacentes y los intercambia si están en orden incorrecto.
    Repite el proceso hasta que no haya más intercambios necesarios.
    Incluye optimización de corte temprano: si en un pasada completa no hubo
    ningún intercambio, la lista ya está ordenada y se detiene.

    Args:
        eventos (list[Event]): Lista de eventos a ordenar.

    Returns:
        list[Event]: Nueva lista ordenada por timestamp ascendente.
                     La lista original no se modifica.

    Complejidad:
        Mejor caso:  O(n)   → lista ya ordenada (corte temprano).
        Peor caso:   O(n²)  → lista en orden inverso.
        Promedio:    O(n²).
        Memoria:     O(n)   → crea una copia de la lista.
    """
    resultado = eventos[:]         # copia para no modificar la lista original
    n = len(resultado)

    for i in range(n - 1):
        hubo_intercambio = False

        for j in range(n - 1 - i):
            if resultado[j].timestamp > resultado[j + 1].timestamp:
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
                hubo_intercambio = True

        if not hubo_intercambio:   # corte temprano
            break

    return resultado


def mergesort(eventos):
    """
    Ordena una lista de eventos por timestamp usando el algoritmo mergesort.

    Aplica la estrategia divide y vencerás: divide la lista en mitades
    recursivamente hasta tener sublistas de un elemento, luego las fusiona
    en orden. La fusión garantiza que el resultado siempre esté ordenado.

    Args:
        eventos (list[Event]): Lista de eventos a ordenar.

    Returns:
        list[Event]: Nueva lista ordenada por timestamp ascendente.
                     La lista original no se modifica.

    Complejidad:
        Mejor caso:  O(n log n) → siempre divide en mitades iguales.
        Peor caso:   O(n log n) → garantizado en todos los casos.
        Promedio:    O(n log n).
        Memoria:     O(n)       → requiere listas auxiliares en la fusión.
    """
    if len(eventos) <= 1:
        return eventos[:]

    medio = len(eventos) // 2
    izquierda = mergesort(eventos[:medio])
    derecha = mergesort(eventos[medio:])

    return _fusionar(izquierda, derecha)


def _fusionar(izquierda, derecha):
    """
    Fusiona dos listas ordenadas en una sola lista ordenada.

    Compara los elementos del frente de cada lista y toma el menor,
    avanzando en esa lista hasta agotar ambas.

    Args:
        izquierda (list[Event]): Primera mitad ordenada.
        derecha (list[Event]): Segunda mitad ordenada.

    Returns:
        list[Event]: Lista fusionada y ordenada por timestamp.

    Complejidad: O(n) donde n es la suma de ambas listas.
    """
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i].timestamp <= derecha[j].timestamp:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    # Agregar los elementos restantes de la lista que no se agotó
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado