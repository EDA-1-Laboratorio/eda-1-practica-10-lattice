"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Estrategia incremental – Insertion sort instrumentado

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""

import time
import random


# ---------------------------------------------------------------------------
# Problema A – Insertion sort con métricas
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list) -> tuple:
 arr = arr.copy()
    n = len(arr)
    comparaciones = 0
    movimientos   = 0
    inicio = time.perf_counter()

    for i in range(1, n):
        llave = arr[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if arr[j] > llave:
                arr[j+1] = arr[j]
                movimientos += 1
                j -= 1
            else:
                break
        arr[j+1] = llave
        movimientos += 1
        
    tiempo = time.perf_counter() - inicio
    return (arr, comparaciones, movimientos, tiempo)

print(insertion_sort_metricas([5, 2, 7, 1, 4]))



# ---------------------------------------------------------------------------
# Problema B – Generación de escenarios
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list[int]) -> tuple:
    arr = arr.copy()
    n = len(arr)
    comparaciones = 0
    movimientos = 0
    inicio = time.perf_counter()

    for i in range(1, n):
        llave = arr[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if arr[j] > llave:
                arr[j+1] = arr[j]
                movimientos += 1
                j -= 1
            else:
                break
        arr[j+1] = llave
        movimientos += 1
        
    tiempo = time.perf_counter() - inicio
    return (arr, comparaciones, movimientos, tiempo)

def generar_arreglo(n: int, escenario: str) -> list:
    if escenario == 'mejor':
        return list(range(n))
    elif escenario == 'peor':
        return list(range(n, 0, -1))
    elif escenario == 'promedio':
        arr = list(range(n))
        random.shuffle(arr)
        return arr
    else:
        raise ValueError("Escenario inválido")

def medir_escenarios(tamanos: list) -> list:
    resultados = []
    for n in tamanos:
        for escenario in ("mejor", "promedio", "peor"):
            arr = generar_arreglo(n, escenario)
            _, comps, movs, t = insertion_sort_metricas(arr)
            
            res = {
                "tamano": n,
                "escenario": escenario,
                "comparaciones": comps,
                "movimientos": movs,
                "tiempo": t
            }
            resultados.append(res)
            
            print(f"n={n:4} | {escenario:8} -> Comps: {comps:10} | Movs: {movs:10} | Tiempo: {t:.5f}s")
    
    return resultados

# ---------------------------------------------------------------------------
# Problema D – Versión híbrida (insertion sort + merge sort)
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list[int]) -> tuple:
    arr = arr.copy()
    n = len(arr)
    comparaciones = 0
    movimientos = 0
    inicio = time.perf_counter()

    for i in range(1, n):
        llave = arr[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if arr[j] > llave:
                arr[j+1] = arr[j]
                movimientos += 1
                j -= 1
            else:
                break
        arr[j+1] = llave
        movimientos += 1
        
    tiempo = time.perf_counter() - inicio
    return (arr, comparaciones, movimientos, tiempo)

def implement_hibrido (arr: list[int], t: int):
    if len(arr) <= t:
        sorted_arr, _, _, _ = insertion_sort_metricas(arr)
        return sorted_arr
    
    mid = len(arr) // 2
    izq = implement_hibrid (arr[:mid], t)
    der = implement_hibrid (arr[mid:], t)
    
    return merge(izq, der)

def merge(izq, der):
    lista_unida = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] < der[j]:
            lista_unida.append(izq[i])
            i += 1
        else:
            lista_unida.append(der[j])
            j += 1
    lista_unida.extend(izq[i:])
    lista_unida.extend(der[j:])
    return lista_unida

n_grande = 10000
umbrales = [8, 16, 32, 64]
arreglo_aleatorio = [random.randint(0, 10000) for _ in range(n_grande)]

for t in umbrales:
    inicio = time.perf_counter()
    resultado = implement_hibrid (arreglo_aleatorio, t)
    fin = time.perf_counter() - inicio
    print(f"Umbral t={t}         Tiempo total: {fin:.6f} segundos")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tamanos = [1000, 2000, 4000, 8000]
    print("Midiendo escenarios... (puede tardar unos segundos)\n")
    resultados = medir_escenarios(tamanos)

    if resultados:
        print(f"{'Tamaño':>8} {'Escenario':>10} {'Comps':>12} "
              f"{'Movs':>12} {'Tiempo (s)':>12}")
        print("-" * 60)
        for r in resultados:
            print(f"{r['tamano']:>8} {r['escenario']:>10} "
                  f"{r['comparaciones']:>12} {r['movimientos']:>12} "
                  f"{r['tiempo']:>12.4f}")
    else:
        print("medir_escenarios aún no implementada.")
