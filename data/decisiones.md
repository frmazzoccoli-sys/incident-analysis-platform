Analisis de los resultados:

n           secuencial          binaria         BST         hashing
100         0.000004s           0.000005s       0.000001s   ~0s
500         0.000037s           0.000020s       0.000002s   ~0s
1000        0.000075s           0.000038s       0.000002s   ~0s
2000        0.000062s           0.000095s       0.000002s   ~0s
5000        0.000215s           0.000281s       0.000003s   ~0s

Hashing es imbatible: tiempo prácticamente cero en todos los tamaños, confirmando O(1)
BST sorprende: más rápido que binaria en todos los casos, porque evita construir la lista de IDs en cada búsqueda
Binaria con anomalía: en n=2000 es más lento que en n=1000, esto se explica porque bisect extrae la lista de IDs cada vez, sumando O(n) al costo real
Secuencial: crece linealmente como se esperaba, confirmando O(n)

Ordenamientos
n           burbuja         mergesort           sorted()
100         0.001297s       0.000246s           0.000020s
500         0.038182s       0.001885s           0.000152s
1000        0.126106s       0.003936s           0.000350s
2000        0.529306s       0.009675s           0.000744s
5000        4.509754s       0.030042s           0.002369s

Burbuja explota: de 0.001s a 4.5s con n=5000, confirmando O(n²) de forma dramática
Mergesort escala bien: de 0.000246s a 0.030s, crecimiento moderado confirmando O(n log n)
sorted() es 13x más rápido que mergesort: implementación en C nativo, misma complejidad pero constante mucho menor
La diferencia burbuja vs mergesort en n=5000: 4.5s vs 0.03s → mergesort es 150 veces más rápido

Memoria
n           burbuja         mergesort           sorted()
100         0.78KB          1.77KB              0.95KB
5000        39.06KB         81.74KB             116.95KB

Burbuja usa menos memoria: solo necesita una copia de la lista
Mergesort usa más memoria: crea sublistas auxiliares en cada nivel de recursión
Trade-off claro: burbuja gana en memoria pero pierde dramáticamente en tiempo
