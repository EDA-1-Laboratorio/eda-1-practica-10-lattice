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

from greedy_cambio import cambio_greedy, cambio_optimo_dp


def comparar_estrategias(monto_max: int, monedas: list) -> dict:
    """
    Para cada monto de 1 a monto_max, compara greedy vs DP.

    Retorna:
        - montos_optimos
        - montos_greedy_falla
        - montos_greedy_suboptimo
        - max_diferencia
    """

    montos_optimos = []
    montos_greedy_falla = []
    montos_greedy_suboptimo = []

    max_diferencia = 0

    for monto in range(1, monto_max + 1):
        g = cambio_greedy(monto, monedas)
        d = cambio_optimo_dp(monto, monedas)

        # Caso: greedy falla pero DP sí encuentra solución
        if g is None and d is not None:
            montos_greedy_falla.append(monto)

        # Ambos tienen solución → comparar número de monedas
        elif g is not None and d is not None:
            monedas_g = len(g[0])
            monedas_d = len(d[0])

            if monedas_g == monedas_d:
                montos_optimos.append(monto)

            elif monedas_g > monedas_d:
                diferencia = monedas_g - monedas_d

                montos_greedy_suboptimo.append(
                    (monto, monedas_g, monedas_d)
                )

                # actualizar máxima diferencia
                if diferencia > max_diferencia:
                    max_diferencia = diferencia

    return {
        "montos_optimos": montos_optimos,
        "montos_greedy_falla": montos_greedy_falla,
        "montos_greedy_suboptimo": montos_greedy_suboptimo,
        "max_diferencia": max_diferencia
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # -------------------------------
    # Sistema canónico
    # -------------------------------
    canonicas = [1, 2, 5, 10, 20, 50]

    print("=== Sistema canónico [1,2,5,10,20,50] ===")
    for monto in [11, 30, 63]:
        g = cambio_greedy(monto, canonicas)
        d = cambio_optimo_dp(monto, canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    res_c = comparar_estrategias(60, canonicas)

    print("\n--- Resultados sistema canónico ---")
    print(f"Casos óptimos      : {len(res_c['montos_optimos'])}")
    print(f"Casos subóptimos   : {len(res_c['montos_greedy_suboptimo'])}")
    print(f"Casos con fallo    : {len(res_c['montos_greedy_falla'])}")
    print(f"Máxima diferencia  : {res_c['max_diferencia']}")

    # -------------------------------
    # Sistema NO canónico
    # -------------------------------
    no_canonicas = [1, 3, 4]

    print("\n=== Sistema no canónico [1,3,4] ===")
    for monto in [6, 12, 15]:
        g = cambio_greedy(monto, no_canonicas)
        d = cambio_optimo_dp(monto, no_canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    res_nc = comparar_estrategias(60, no_canonicas)

    print("\n--- Resultados sistema no canónico ---")
    print(f"Casos óptimos      : {len(res_nc['montos_optimos'])}")
    print(f"Casos subóptimos   : {len(res_nc['montos_greedy_suboptimo'])}")
    print(f"Casos con fallo    : {len(res_nc['montos_greedy_falla'])}")
    print(f"Máxima diferencia  : {res_nc['max_diferencia']}")

    # Mostrar ejemplos de subóptimos
    if res_nc["montos_greedy_suboptimo"]:
        print("\nPrimeros 5 casos subóptimos:")
        for caso in res_nc["montos_greedy_suboptimo"][:5]:
            m, g, d = caso
            print(f"  Monto {m}: greedy={g} monedas, óptimo={d} monedas")
