# src/servicios/text_analyzer.py


class TextAnalyzer:
    """
    Realiza búsquedas y análisis sobre el campo texto de los eventos.

    Permite buscar patrones simples (palabras clave) en las descripciones
    de los incidentes, útil para detección de alertas y clasificación
    automática de eventos por contenido.

    Operaciones principales:
        buscar_por_palabra  → O(n * m) donde n es eventos y m longitud del texto
        buscar_por_patron   → O(n * m)
        palabras_frecuentes → O(n * m + p log p) donde p es palabras únicas
    """

    def __init__(self):
        """Inicializa el analizador sin configuración adicional."""
        pass

    def buscar_por_palabra(self, eventos, palabra):
        """
        Retorna todos los eventos cuyo texto contiene una palabra dada.

        La búsqueda es case-insensitive: busca la palabra en minúsculas
        dentro del texto también convertido a minúsculas.

        Args:
            eventos (list[Event]): Lista de eventos donde buscar.
            palabra (str): Palabra clave a buscar en el texto.

        Returns:
            list[Event]: Lista de eventos que contienen la palabra.

        Complejidad: O(n * m) donde n es la cantidad de eventos
                     y m la longitud promedio del texto.
        """
        palabra = palabra.lower()
        return [
            evento for evento in eventos
            if palabra in evento.texto.lower()
        ]

    def buscar_por_patron(self, eventos, patron):
        """
        Retorna todos los eventos cuyo texto contiene un patrón dado.

        Similar a buscar_por_palabra pero permite patrones más amplios,
        como frases completas o subcadenas.

        Args:
            eventos (list[Event]): Lista de eventos donde buscar.
            patron (str): Patrón o frase a buscar en el texto.

        Returns:
            list[Event]: Lista de eventos que contienen el patrón.

        Complejidad: O(n * m)
        """
        patron = patron.lower()
        return [
            evento for evento in eventos
            if patron in evento.texto.lower()
        ]

    def palabras_frecuentes(self, eventos, top=10):
        """
        Retorna las palabras más frecuentes en los textos de los eventos.

        Útil para identificar patrones recurrentes en las descripciones
        de incidentes y apoyar la toma de decisiones.

        Ignora palabras cortas (menos de 3 caracteres) para filtrar
        artículos, preposiciones y conectores poco informativos.

        Args:
            eventos (list[Event]): Lista de eventos a analizar.
            top (int): Cantidad de palabras más frecuentes a retornar.
                       Por defecto 10.

        Returns:
            list[tuple]: Lista de (palabra, frecuencia) ordenada
                         de mayor a menor frecuencia.

        Complejidad: O(n * m + p log p) donde p es la cantidad
                     de palabras únicas encontradas.
        """
        frecuencias = {}

        for evento in eventos:
            palabras = evento.texto.lower().split()
            for palabra in palabras:
                # Filtrar palabras cortas y limpiar puntuación
                palabra = palabra.strip(".,;:!?()[]")
                if len(palabra) >= 3:
                    frecuencias[palabra] = frecuencias.get(palabra, 0) + 1

        ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
        return ordenadas[:top]

    def __repr__(self):
        return "TextAnalyzer()"