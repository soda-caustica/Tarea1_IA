from __future__ import annotations

import os

import numpy as np

from agentes import Agente, AgenteTermino
from grafo import *


class Juego:
    tablero: Tablero
    agentes: list[Agente]
    objetivo: tuple[int, int]

    def costo(self, pos: tuple[int, int]) -> int:
        agentesCorriendo = filter(
            lambda x: not isinstance(x.state, AgenteTermino), self.agentes
        )
        agentesEnCuadricula = list(filter(lambda x: x.pos == pos, agentesCorriendo))
        return len(agentesEnCuadricula) + 1

    def getCuadricula(self, pos: tuple[int, int]) -> Cuadricula:
        x, y = pos
        return self.tablero.tablero[x][y]

    def __init__(
        self,
        tablero: Tablero,
        obj: tuple[int, int],
        agentes: list[Agente] | None = None,
    ):
        self.agentes = agentes if agentes is not None else []
        self.tablero = tablero

        try:
            x, y = obj
            self.objetivo = obj
            assert tablero.tablero[x][y].tipo == TipoCuadricula.SALIDA
        except Exception:
            raise ValueError("El objetivo entregado no es una salida en el tablero")

    @classmethod
    def tableroVacio(
        cls,
        size: tuple[int, int],
        obj: tuple[int, int],
        agentes: list[Agente] | None = None,
    ):
        return cls(
            Tablero.vacio(size, obj), obj, agentes if agentes is not None else []
        )

    @classmethod
    def fromMap(cls, mapa: np.ndarray, agentes: list[Agente] | None = None):
        filas, columnas = np.where(mapa == TipoCuadricula.SALIDA.value)
        if filas.size == 0:
            raise ValueError("El mapa no contiene una salida")
        return cls(Tablero.fromMap(mapa), (filas[0], columnas[0]), agentes)

    def step(self, imprimir: bool) -> int:
        for agente in self.agentes:
            agente.update(self)
        agentesCorriendo = list(
            filter(lambda x: not isinstance(x.state, AgenteTermino), self.agentes)
        )
        if imprimir:
            self.imprimir()
        return len(agentesCorriendo)

    def imprimir(self):
        os.system("clear")
        agentesCorriendo = list(
            filter(lambda x: not isinstance(x.state, AgenteTermino), self.agentes)
        )
        for i in self.tablero.tablero:
            for j in i:
                if j.tipo == TipoCuadricula.SALIDA:
                    print("\033[48;2;0;255;0mX\033[0m", end=" ")
                    continue
                if j.tipo == TipoCuadricula.MURO:
                    print("#", end=" ")
                    continue
                agentesEnCuadricula = list(
                    filter(lambda x: x.pos == j.pos, agentesCorriendo)
                )
                count = len(agentesEnCuadricula)
                color = agentesEnCuadricula[0].color() if count > 0 else (255, 255, 255)
                print(
                    "_"
                    if count == 0
                    else f"\033[48;2;{color[0]};{color[1]};{color[2]}m"
                    + str(count)
                    + "\033[0m",
                    end=" ",
                )
            print()
        print(f"Agentes restantes = {len(agentesCorriendo)}")
        print(f"Agentes listos = {len(self.agentes) - len(agentesCorriendo)}")
