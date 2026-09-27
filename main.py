import os
import random
import sys
from enum import Enum
from random import randint
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
UTILS_DIR = os.path.join(ROOT, "utils")
AGENTES_DIR = os.path.join(ROOT, "agentes")
for directory in (UTILS_DIR, AGENTES_DIR):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from agentes import (
    Agente,
    AgenteBFS,
    AgenteDFS,
    AgenteDijkstra,
    AgenteGenetico,
    AgenteRandom,
)
from juego import Juego
from mapas import *

x_size = 15
y_size = 15


def genPos():
    return (randint(0, x_size - 1), randint(0, y_size - 1))


class TipoAgentes(Enum):
    DFS = 1
    BFS = 2
    DIJKSTRA = 3
    GENETICO = 5


def genFuego(mapa: np.ndarray, num: int):
    nuevo = np.array(mapa)
    posiciones_libres = list(
        zip(
            *np.where(
                (nuevo != TipoCuadricula.SALIDA.value)
                & (nuevo != TipoCuadricula.FUEGO.value)
            )
        )
    )
    if num > len(posiciones_libres):
        raise ValueError("No hay suficientes casillas libres para generar el fuego")

    for i, j in random.sample(posiciones_libres, num):
        nuevo[i, j] = TipoCuadricula.FUEGO.value
    return nuevo


def func(tipos: list[TipoAgentes], mapa: np.ndarray):
    juego = Juego.fromMap(genFuego(mapa, 2), 4)
    salida = np.where(mapa == TipoCuadricula.SALIDA.value)  # pyright: ignore[reportAny]
    muertosTotales = 0
    for i in tipos:
        x, y = genPos()
        while (x, y) == salida:
            x, y = genPos()
        match i:
            case TipoAgentes.DFS:
                juego.agentes.append(Agente(x, y, AgenteDFS()))
            case TipoAgentes.BFS:
                juego.agentes.append(Agente(x, y, AgenteBFS()))
            case TipoAgentes.DIJKSTRA:
                juego.agentes.append(Agente(x, y, AgenteDijkstra()))
            case TipoAgentes.GENETICO:
                juego.agentes.append(Agente(x, y, AgenteGenetico()))
    i = 0
    while True:
        i += 1
        tup: tuple[int, int] = juego.step(False)
        restantes, muertos = tup
        if restantes == 0:
            muertosTotales += muertos
            break
    return i, muertosTotales


a = 0
if len(sys.argv) != 3:
    print(
        "uso: python main.py <numero de agentes> <numero de iteraciones por tipo de agente>"
    )
    sys.exit(-1)
numAgentes = int(sys.argv[1])
iteraciones = int(sys.argv[2])
mapa = mapa_2
for tipo in [TipoAgentes.GENETICO]:
    start = time.time()
    res = np.zeros(iteraciones, dtype=np.int_)
    muertos = np.zeros(iteraciones, dtype=np.int_)
    for k in range(iteraciones):
        res[k], muertos[k] = func([tipo for _ in range(numAgentes)], mapa)
        print(f"iteracion{k} terminada en {time.time() - start}")
        start = time.time()
    print(
        f"En promedio el agente de este tipo ({tipo.name}) demoró {sum(res) / iteraciones} turnos en encontrar la salida, con una tasa de supervivencia del {(1 - sum(muertos) / (iteraciones * numAgentes)) * 100}%, con una desviacion estandar de {res.std()} y un rango entre {res.min()} y {res.max()}"
    )
