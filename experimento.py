import time
from greedy_cambio import cambio_greedy

# -------------------------------
# Medición de tiempo
# -------------------------------
def medir_tiempo(func, *args, repeticiones=5):
    tiempos = []

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        func(*args)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    return min(tiempos)


# -------------------------------
# Experimento (test de doblamiento)
# -------------------------------
def experimento_greedy():
    monedas = [1, 5, 10, 25]
    tamaños = [100, 200, 400, 800]

    resultados = []

    print("\nEjecutando experimento...\n")

    for n in tamaños:
        t = medir_tiempo(cambio_greedy, n, monedas)
        resultados.append((n, t))
        print(f"n={n} -> tiempo={t:.8f} s")

    return resultados


# -------------------------------
# Calcular razón de doblamiento
# -------------------------------
def calcular_ratio(resultados):
    print("\nRazón de doblamiento:\n")

    for i in range(len(resultados) - 1):
        n1, t1 = resultados[i]
        n2, t2 = resultados[i + 1]

        r = t2 / t1 if t1 > 0 else 0

        print(f"r({n1}) = T({n2}) / T({n1}) = {r:.2f}")


# -------------------------------
# Tabla final
# -------------------------------
def mostrar_tabla(resultados):
    print("\nTabla de resultados:\n")
    print("n\tT(n) (s)")

    for n, t in resultados:
        print(f"{n}\t{t:.8f}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    resultados = experimento_greedy()
    mostrar_tabla(resultados)
    calcular_ratio(resultados)
