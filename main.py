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
    AgenteGreedy,
    AgenteBeam,
    AgenteRandom,
    AgenteTermino,
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
    GENETICO = 5
    GREEDY = 6
    BEAM = 7


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


def func(tipos: list[TipoAgentes], mapa: np.ndarray) -> tuple[int | None, int]:
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
            case TipoAgentes.GENETICO:
                juego.agentes.append(Agente(x, y, AgenteGenetico()))
            case TipoAgentes.GREEDY:
                juego.agentes.append(Agente(x, y, AgenteGreedy()))
            case TipoAgentes.BEAM:
                juego.agentes.append(Agente(x, y, AgenteBeam()))
    i = 0
    ultimo_escape = 0
    escapes = 0
    while True:
        i += 1
        tup: tuple[int, int] = juego.step(False)
        restantes, muertos = tup
        escapes_actuales = sum(
            isinstance(agente.state, AgenteTermino) for agente in juego.agentes
        )
        if escapes_actuales > escapes:
            ultimo_escape = i
            escapes = escapes_actuales
        if restantes == 0:
            muertosTotales += muertos
            return (ultimo_escape if escapes else None), muertosTotales


def imprimir_tabla(filas: list[tuple[str, ...]]):
    encabezados = (
        "Mapa",
        "Algoritmo",
        "Iteraciones",
        "Supervivencia",
        "Tiempos validos",
        "Media turnos",
        "Desv. estandar",
        "Min. turnos",
        "Max. turnos",
        "T/iter(s)",
    )
    anchos = [
        max(len(encabezado), *(len(fila[indice]) for fila in filas))
        for indice, encabezado in enumerate(encabezados)
    ]

    def borde(caracter="-"):
        return "+" + "+".join(caracter * (ancho + 2) for ancho in anchos) + "+"

    def fila(valores):
        return (
            "| "
            + " | ".join(valor.ljust(ancho) for valor, ancho in zip(valores, anchos))
            + " |"
        )

    print("\nRESUMEN DE SIMULACIONES")
    print(borde("="))
    print(fila(encabezados))
    print(borde("="))
    for valores in filas:
        print(fila(valores))
    print(borde("="))


if len(sys.argv) not in (2, 3):
    print(
        "uso: python main.py <numero de agentes> "
        "[numero de iteraciones por tipo de agente (predeterminado: 200)]"
    )
    sys.exit(-1)

numAgentes = int(sys.argv[1])
iteraciones = int(sys.argv[2]) if len(sys.argv) == 3 else 200
if numAgentes <= 0:
    raise ValueError("El numero de agentes debe ser positivo")
if iteraciones < 80:
    raise ValueError("Cada experimento requiere al menos 80 iteraciones")

mapas = (("Mapa 1", mapa_1), ("Mapa 2", mapa_2), ("Mapa 3", mapa_3))
filas = []
for nombre_mapa, mapa in mapas:
    for tipo in TipoAgentes:
        inicio = time.perf_counter()
        turnos = np.full(iteraciones, np.nan, dtype=np.float64)
        muertos = np.zeros(iteraciones, dtype=np.int_)
        for indice in range(iteraciones):
            tiempo_despeje, muertos[indice] = func(
                [tipo for _ in range(numAgentes)], mapa
            )
            if tiempo_despeje is not None:
                turnos[indice] = tiempo_despeje
            print(
                f"[{nombre_mapa}][{tipo.name}] "
                f"iteracion {indice + 1}/{iteraciones} terminada: "
                f"{tiempo_despeje if tiempo_despeje is not None else 'sin evacuados'} "
                f"turnos, {muertos[indice]} muertos"
            )

        tiempo_promedio = (time.perf_counter() - inicio) / iteraciones
        supervivencia = (1 - sum(muertos) / (iteraciones * numAgentes)) * 100
        tiempos_validos = turnos[~np.isnan(turnos)]
        if tiempos_validos.size:
            media_turnos = f"{tiempos_validos.mean():.2f}"
            desv_estandar = (
                f"{tiempos_validos.std(ddof=1):.2f}"
                if tiempos_validos.size > 1
                else "N/D"
            )
            min_turnos = str(int(tiempos_validos.min()))
            max_turnos = str(int(tiempos_validos.max()))
        else:
            media_turnos = desv_estandar = min_turnos = max_turnos = "N/D"
        filas.append(
            (
                nombre_mapa,
                tipo.name,
                str(iteraciones),
                f"{supervivencia:.2f}%",
                str(tiempos_validos.size),
                media_turnos,
                desv_estandar,
                min_turnos,
                max_turnos,
                f"{tiempo_promedio:.6f}",
            )
        )

imprimir_tabla(filas)
