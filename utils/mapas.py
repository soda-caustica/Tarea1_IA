# Hecho con Gemini

import numpy as np

from grafo import TipoCuadricula

#  Codificación numérica:
#  0: Celda libre
#  1: Pared / obstáculo
#  2: Salida de evacuación (S)

CHAR_MAP = {".": TipoCuadricula.CAMINABLE, "#": TipoCuadricula.MURO, "S": TipoCuadricula.SALIDA, "F": TipoCuadricula.FUEGO}


def parse_map(map_str: str) -> np.ndarray:
    lines = [
        line.strip() for line in map_str.strip().split("\n") if line.strip()
    ]
    rows = []
    for line in lines:
        row = line.split()
        rows.append([CHAR_MAP[char].value for char in row])
    return np.array(rows, dtype=np.int8)


#  -------------------------------------------------------------
#  Mapa 1: Alta Densidad / Cuello de Botella (15x15)
#  -------------------------------------------------------------
mapa_1_str = """
. . . . . . . . # . . . . . .
. . . . . . . . # . . . . . .
# # # . # # # . # . # # # . .
. . . . # . . . # . . . # . .
. . # # # # # . # # # # # . .
. . # . . . . . . . . . # . .
. . # . # # # . # # # . # . .
. . # . # . . . . . # . # . .
. . . . # . # # # . # . . . .
. # # # # . # S # . # # # # #
. . . . . . # . # . . . . . .
. . # # # # # . # # # # # . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
mapa_1 = parse_map(mapa_1_str)

#  -------------------------------------------------------------
#  Mapa 2: Densidad Media / Laberinto Corporativo (15x15)
#  -------------------------------------------------------------
mapa_2_str = """
. . . . . . . . . . . . . . .
. . . . # . . . . . # . . . .
. . # . # . # # # . # . # . .
. . # . . . # . # . . . # . .
. . # # # # # . # # # # # . .
. . . . . . # . . . . . . . .
# # # . # . # # # . # # # . .
. . . . # . . . # . # . . . .
. . # # # # # . # . # . # # #
. . # . . . # . # . . . # . .
. . # . # . # . # # # . # . .
. . . . # . . . # . . . . . .
. . # . # . # . # . # # # . .
. . . . # . . . . . . . # S .
. . . . . . . . . . . . . . .
"""
mapa_2 = parse_map(mapa_2_str)

#  -------------------------------------------------------------
#  Mapa 3: Baja Densidad / Dispersión Abierta (15x15)
#  -------------------------------------------------------------
mapa_3_str = """
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . # # . . . . . # # . . .
. . . . . . . . . . . . . . .
. . . . . . # # # . . . . . .
. . . . . . . . . . . . . . .
. . . # # . . . . . # # . . .
. . . . . . . . . . . . . . .
. . . . . . # # # . . . . . .
. . . . . . . . . . . . . . .
. . . # # . . . . . # # . . .
. . . . . . . . . . . . . . .
. . . # # . . S . . # # . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
mapa_3 = parse_map(mapa_3_str)
