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

-----------------------------

BST
Un Binary Search Tree es un árbol binario donde cada nodo cumple esta propiedad:
        E004
       /    \
    E002    E006
    /  \    /  \
 E001  E003 E005 E007

Todo lo que está a la izquierda de un nodo tiene un valor menor
Todo lo que está a la derecha tiene un valor mayor

Esto permite buscar en O(log n) en lugar de O(n) de una lista, porque en cada paso descartamos la mitad del árbol.

En nuestro sistema tenemos eventos con event_id. Sin un BST, buscar un evento por ID requiere recorrer toda la lista: O(n). Con un BST ordenado por event_id:
Operación                       Lista               BST
Insertar                        O(1)                O(log n)
Buscar                          O(n)                O(log n)
Eliminar                        O(n)                O(log n)
Recorrer ordenado               O(n log n)          O(n)
El recorrido ordenado es gratis en un BST usando inorden (izquierda → raíz → derecha).

¿Por qué no usar un diccionario directamente?
Un diccionario también busca en O(1). La razón de implementar BST es:

El TP lo requiere explícitamente
Un BST permite recorrer eventos ordenados sin costo extra
Permite búsquedas por rango (todos los eventos entre E010 y E050)
Demuestra comprensión de estructuras jerárquicas para el informe

¿Por qué campo ordenamos?
Tenemos estas opciones:
Campo               Ventaja
event_id            Búsqueda directa por identificador
timestamp           Consultas cronológicas y por rango de tiempo
prioridad           Ya lo cubre la PriorityQueue

La opción más útil y complementaria a lo que ya tenemos es event_id, porque la PriorityQueue ya cubre prioridad y la búsqueda por ID es la consulta más común en cualquier sistema de incidentes.

-------------------------

Diseño de la clase Nodo
Cada nodo del árbol necesita guardar:

class NodoBST:
    evento        # el objeto Event
    izquierda     # referencia al hijo izquierdo
    derecha       # referencia al hijo derecho

Es una clase simple, sin lógica propia. Toda la lógica vive en el BST.

Operaciones que vamos a implementar
insertar            Agregar un evento al árbol                      O(log n)
buscar              Encontrar un evento por event_id                O(log n)
eliminar            Quitar un evento del árbol                      O(log n)
inorden             Listar todos los eventos ordenados por event_id O(n)
minimo              Evento con el event_id más pequeño              O(log n)
maximo              Evento con el event_id más grande               O(log n)

--------------------------

Eliminar un nodo

Eliminar tiene tres casos:
Caso 1 — El nodo no tiene hijos (es una hoja): simplemente se elimina.
Antes:         Después:
   E004           E004
   /              /
 E002           (vacío)

Caso 2 — El nodo tiene un solo hijo: se reemplaza por su hijo.
Antes:         Después:
   E004           E004
   /              /
 E002           E001
 /
E001

Caso 3 — El nodo tiene dos hijos: se reemplaza por su sucesor inorden (el menor de los mayores), que es el nodo más a la izquierda del subárbol derecho.
Antes:         Después:
   E004           E005
   /  \           /  \
 E002  E006     E002  E006
       /
     E005