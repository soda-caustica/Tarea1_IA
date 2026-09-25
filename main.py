import sys
from enum import Enum
from random import randint

from agentes import Agente, AgenteBFS, AgenteDFS, AgenteDijkstra, AgenteRandom
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
    RANDOM = 4


def func(tipos: list[TipoAgentes], mapa: np.ndarray):
    juego = Juego.fromMap(mapa)
    salida = np.where(mapa == TipoCuadricula.SALIDA.value)  # pyright: ignore[reportAny]
    for i in tipos:
        x, y = genPos()
        while (x, y) == salida:
            x, y = genPos()
        match i:
            case TipoAgentes.RANDOM:
                juego.agentes.append(Agente(x, y, AgenteRandom()))
            case TipoAgentes.DFS:
                juego.agentes.append(Agente(x, y, AgenteDFS()))
            case TipoAgentes.BFS:
                juego.agentes.append(Agente(x, y, AgenteBFS()))
            case TipoAgentes.DIJKSTRA:
                juego.agentes.append(Agente(x, y, AgenteDijkstra()))
    i = 0
    while True:
        i += 1
        restantes: int = juego.step(False)
        if restantes == 0:
            break
    return i


a = 0
if len(sys.argv) != 3:
    print(
        "uso: python main.py <numero de agentes> <numero de iteraciones por tipo de agente>"
    )
    sys.exit(-1)
numAgentes = int(sys.argv[1])
iteraciones = int(sys.argv[2])
mapa = mapa_2
for tipo in TipoAgentes:
    res = np.zeros(iteraciones, dtype=np.int_)
    for k in range(iteraciones):
        res[k] = func([tipo for _ in range(numAgentes)], mapa)
    print(
        f"En promedio el agente de este tipo ({tipo.name}) demoró {sum(res) / iteraciones} turnos en encontrar la salida, con una desviacion estandar de {res.std()} y un rango entre {res.min()} y {res.max()}"
    )
