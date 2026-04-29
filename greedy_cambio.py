"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Algoritmo ávido (greedy) – Cambio de monedas

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""


# ---------------------------------------------------------------------------
# Problema A – Solución greedy
# ---------------------------------------------------------------------------

def cambio_greedy(monto: int, monedas: list) -> tuple | None:
    """
    Resuelve el problema de cambio con la estrategia ávida:
    en cada paso usa la moneda de mayor valor que quepa.

    Parámetros:
        monto   – Cantidad (entero positivo) a devolver.
        monedas – Lista de denominaciones disponibles (enteros positivos).

    Retorna:
        (usadas: list, total: int)  si hay solución exacta.
        None                        si el monto no se puede completar.
    """

    if monto < 0 or not isinstance(monedas, list) or len(monedas) == 0:
        return None
    if any(type(m) != int or m <= 0 for m in monedas):
        return None

    monedas = sorted(monedas, reverse=True)

    usadas = []
    restante = monto

    for moneda in monedas:
        cantidad = restante // moneda
        if cantidad > 0:
            usadas.extend([moneda] * cantidad)
            restante = restante % moneda

    if restante == 0:
        return usadas, sum(usadas)

    return None
# ---------------------------------------------------------------------------
# Problema B – Solución óptima por programación dinámica
# ---------------------------------------------------------------------------
def cambio_optimo_dp(monto: int, monedas: list) -> tuple | None:

    """
    Resuelve el problema de cambio de manera óptima usando
    programación dinámica (número mínimo de monedas).

    Retorna:
        (usadas: list, total: int)  con mínimo de monedas.
        None                        si no hay solución exacta.

    Pistas (bottom-up DP):
        dp[i] = mínimo de monedas para devolver exactamente i.
        Inicializa: dp[0] = 0,  dp[i] = float('inf') para i > 0.
        Transición: dp[i] = min(dp[i], dp[i - m] + 1) para cada moneda m <= i.
        Guarda padre[i] = m que produjo dp[i] para reconstruir la solución.
    """
    if monto < 0 or not monedas:
        return None
    if any(type(m) != int or m <= 0 for m in monedas):
        return None

    # Inicialización
    dp = [float('inf')] * (monto + 1)
    dp[0] = 0

    # Para reconstruir la solución
    prev = [-1] * (monto + 1)

    # Llenado de la tabla
    for i in range(1, monto + 1):
        for moneda in monedas:
            if i - moneda >= 0 and dp[i - moneda] + 1 < dp[i]:
                dp[i] = dp[i - moneda] + 1
                prev[i] = moneda

    # Si no hay solución
    if dp[monto] == float('inf'):
        return None

    # Reconstrucción de la solución
    resultado = []
    actual = monto

    while actual > 0:
        moneda = prev[actual]
        resultado.append(moneda)
        actual -= moneda

    return resultado, sum(resultado)

# ---------------------------------------------------------------------------
# Problema C – Comparación: contraejemplos
# ---------------------------------------------------------------------------
def comparar_estrategias(monto_max: int, monedas: list) -> dict:
    """
    Para cada monto de 1 a monto_max, compara greedy vs DP.

    Retorna un diccionario con:
        'montos_greedy_falla'     : lista de montos donde greedy devuelve None
                                    pero DP sí tiene solución.
        'montos_greedy_suboptimo' : lista de (monto, total_greedy, total_dp)
                                    donde greedy usa más monedas que DP.
    """
    montos_greedy_falla = []
    montos_greedy_suboptimo = []

    for m in range(1, monto_max + 1):
        g = cambio_greedy(m, monedas)
        d = cambio_optimo_dp(m, monedas)

        if g is None and d is not None:
            montos_greedy_falla.append(m)

        elif g is not None and d is not None:
            if len(g[0]) > len(d[0]):
                montos_greedy_suboptimo.append((m, len(g[0]), len(d[0])))

    return {
        "montos_greedy_falla": montos_greedy_falla,
        "montos_greedy_suboptimo": montos_greedy_suboptimo
    }

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Sistema canónico
    canonicas = [1, 2, 5, 10, 20, 50]
    print("=== Sistema canónico [1,2,5,10,20,50] ===")
    for monto in [11, 30, 63]:
        g = cambio_greedy(monto, canonicas)
        d = cambio_optimo_dp(monto, canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    # Sistema no canónico – aquí greedy falla
    no_canonicas = [1, 3, 4]
    print("\n=== Sistema no canónico [1,3,4] ===")
    for monto in [6, 12, 15]:
        g = cambio_greedy(monto, no_canonicas)
        d = cambio_optimo_dp(monto, no_canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    print("\n=== Análisis completo montos 1-60, sistema [1,3,4] ===")
    resultado = comparar_estrategias(60, no_canonicas)
    if resultado is not None:
        sub = resultado.get("montos_greedy_suboptimo", [])
        fal = resultado.get("montos_greedy_falla", [])
        print(f"  Casos subóptimos : {len(sub)}")
        print(f"  Casos con fallo  : {len(fal)}")
        if sub:
            print(f"  Primeros 5 subóptimos: {sub[:5]}")
    else:
        print("  comparar_estrategias aún no implementada")
