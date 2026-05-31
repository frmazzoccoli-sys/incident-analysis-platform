El sistema maneja incidentes (Events) con estos atributos clave para las estructuras:

prioridad   → decide el orden de atención
timestamp   → desempate cuando dos incidentes tienen igual prioridad
id          → identificación única

Estructura      ¿Para qué?                                      ¿Con qué?
´Queue´          Procesar eventos en orden de llegada (FIFO)    collections.deque
´PriorityQueue´  Atender primero el incidente más crítico       heapq

¿Por qué collections.deque y no una lista?
Una lista de Python puede usarse como cola, pero:
Operación               list                deque
´append()´ al final     O(1)                O(1)
´pop(0)´ del frente     O(n)                O(1) 

´deque´ está optimizada para inserciones y eliminaciones en ambos extremos. Para una cola FIFO, esto es esencial.

¿Por qué heapq y no ordenar una lista?
Para la PriorityQueue necesitamos siempre extraer el elemento más urgente. Podríamos mantener una lista ordenada, pero:
Operación               Lista ordenada          heapq
Insertar                O(n)                    O(log n)
Extraer mínimo          O(1)                    O(log n)
Construir desde lista   O(n log n)              O(n)

heapq implementa un min-heap: el elemento con menor valor siempre está en la raíz. Como queremos atender la mayor prioridad primero, vamos a invertir el valor (multiplicar por -1) para convertirlo en max-heap.

Implementar la Queue
La Queue FIFO modela una línea de espera: el primer incidente en entrar es el primero en atenderse. Útil para procesar eventos en orden cronológico de llegada.

Implementar la PriorityQueue
Acá entra la decisión más importante: ¿cómo le decimos a heapq que prioridad 1 es más urgente que prioridad 5, o al revés?
Definamos la convención: prioridad 1 = más crítico (como en sistemas de tickets). heapq es un min-heap, entonces el número más chico sale primero → nos conviene directamente.
Para desempatar cuando dos eventos tienen la misma prioridad, usamos el timestamp (el más antiguo primero).

Resumen de decisiones tomadas
Decisión                                      Alternativa descartada         Razón
´deque´ para Queue                            list                         popleft() es O(1) vs O(n)
´heapq´ para Priority                         Solo (prioridad, evento)     Desempate determinístico sin comparar objetos
Prioridad 1 = más crítico (min-heap directo)  Invertir con -1                Más legible, no requiere transformación
