¿Sobre qué campo buscamos y ordenamos?

Tenemos estos candidatos:
Campo               ¿Tiene sentido buscar/ordenar?
event_id            identificación directa
prioridad           ordenar por urgencia
timestamp           ordenar cronológicamente
categoria           agrupar por tipo

La decisión más útil para demostrar los algoritmos es trabajar con prioridad para ordenamiento (valores numéricos simples, fácil de visualizar) y event_id para búsqueda (strings ordenables, complementa el BST).

Búsqueda secuencial vs binaria
Búsqueda secuencial
Recorre la lista elemento por elemento hasta encontrar el que buscamos.
Lista: [E003, E001, E005, E002, E004]
Busco: E004
→ comparo E003 → E001 → E005 → E002 → E004 

No requiere que la lista esté ordenada
Complejidad: O(n)

Búsqueda binaria
Divide la lista por la mitad en cada paso. Requiere lista ordenada.
Lista ordenada: [E001, E002, E003, E004, E005]
Busco: E004
→ medio = E003 → E004 > E003 → busco en mitad derecha
→ medio = E004 

Requiere lista ordenada
Complejidad: O(log n)
Usaremos bisect de Python que es la implementación estándar

Algoritmo           Complejidad promedio            Complejidad peor caso       Estable
Burbuja             O(n²)                           O(n²)                       Si
InserciónO          (n²)                            O(n²)                       Si
Selección           O(n²)                           O(n²)                       No
Mergesort           O(n log n)                      O(n log n)                  Si
Quicksort           O(n log n)                      O(n²)                       No

La elección más interesante para el informe es Mergesort vs Quicksort porque:

Ambos son O(n log n) promedio pero con diferencias reales en práctica
Tienen estrategias distintas (divide y vencerás vs partición)
El contraste con sorted() es más revelador que comparar dos O(n²)

ComparaciónLo que demuestra
Mergesort vs Quicksort              Dos O(n log n): diferencia sutil, difícil de ver en timeit
Burbuja vs Mergesort                O(n²) vs O(n log n): diferencia brutal y visible en gráficos

Ordenar por prioridad, pero tiene un problema: la prioridad tiene pocos valores posibles (por ejemplo 1 a 5), lo que genera muchos empates y no refleja bien el comportamiento de los algoritmos.
Mejor opción: ordenar por timestamp, porque:

Es un valor numérico continuo (datetime)
Casi no hay empates en datasets realistas
Tiene sentido de negocio: ordenar incidentes cronológicamente
Permite búsqueda binaria por rango de fechas


Decisión                Propuesta original          Propuesta revisada          Razón
Algoritmos              Mergesort + Quicksort       Burbuja + Mergesort         Contraste O(n²) vs O(n log n) más visible y didáctico
Campo ordenamiento      prioridad                   timestamp                   Valores continuos, sin empates, más realista
Campo búsqueda          event_id                    event_id                    Se mantiene, es correcto
Búsqueda binaria        bisect                      bisect                      Se mantiene, es lo que pide la consigna

Orden de implementación
1. busqueda.py     → secuencial + binaria sobre event_id
2. ordenamiento.py → burbuja + mergesort sobre timestamp
3. metricas/       → timeit comparando ambos ordenamientos + sorted()


