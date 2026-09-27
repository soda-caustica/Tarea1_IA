from __future__ import annotations

import os
from queue import Queue
from time import sleep

import numpy as np
from grafo import Cuadricula, Tablero, TipoCuadricula

from agentes import Agente, AgenteMuerto, AgenteTermino


class Juego:
    tablero: Tablero
    agentes: list[Agente]
    objetivo: tuple[int, int]
    fire_time: int
    fire_map: np.ndarray
    bfs_map: np.ndarray
    tiempo_global: int
    atochamiento_agentes: np.ndarray

    def agentesCorriendo(self) -> list[Agente]:
        return list(
            filter(
                lambda x: (
                    not isinstance(x.state, AgenteTermino)
                    and not isinstance(x.state, AgenteMuerto)
                ),
                self.agentes,
            )
        )

    def costo(self, pos: tuple[int, int]) -> int:
        return int(self.atochamiento_agentes[pos]) + 1

    def getCuadricula(self, pos: tuple[int, int]) -> Cuadricula:
        x, y = pos
        return self.tablero.tablero[x][y]

    def __init__(
        self,
        tablero: Tablero,
        obj: tuple[int, int],
        fire_time: int,
        agentes: list[Agente] | None = None,
    ):
        self.agentes = agentes if agentes is not None else []
        self.tablero = tablero
        self.fire_time = fire_time
        self.tiempo_global = 0

        try:
            x, y = obj
            self.objetivo = obj
            assert tablero.tablero[x][y].tipo == TipoCuadricula.SALIDA
        except Exception:
            raise ValueError("El objetivo entregado no es una salida en el tablero")
        self.fire_map = self._calcFireMap(self.tablero)
        self.bfs_map = self._calcBFS(self.tablero)
        self.atochamiento_agentes = np.zeros(tablero.size, dtype=np.int_)
        for agente in self.agentesCorriendo():
            self.atochamiento_agentes[agente.pos] += 1

    @classmethod
    def tableroVacio(
        cls,
        size: tuple[int, int],
        obj: tuple[int, int],
        fire_time: int,
        agentes: list[Agente] | None = None,
    ):
        return cls(
            Tablero.vacio(size, obj),
            obj,
            fire_time,
            agentes if agentes is not None else [],
        )

    @classmethod
    def fromMap(
        cls, mapa: np.ndarray, fire_time: int, agentes: list[Agente] | None = None
    ):
        filas, columnas = np.where(mapa == TipoCuadricula.SALIDA.value)
        if filas.size == 0:
            raise ValueError("El mapa no contiene una salida")
        return cls(Tablero.fromMap(mapa), (filas[0], columnas[0]), fire_time, agentes)

    def _calcBFS(self, tablero: Tablero) -> np.ndarray:
        bfs: np.ndarray = np.full(tablero.size, -1)  # pyright: ignore[reportUnknownVariableType]
        queue: Queue[tuple[Cuadricula, int]] = Queue()
        queue.put((self.getCuadricula(self.objetivo), 0))

        while not queue.empty():
            celda, n = queue.get()
            for vecino in celda.vecinos:
                if (
                    vecino is None
                    or bfs[vecino.pos] != -1
                    or vecino.tipo != TipoCuadricula.CAMINABLE
                ):
                    continue
                queue.put((vecino, n + 1))
                bfs[vecino.pos] = n + 1
        return bfs

    def _calcFireMap(self, tablero: Tablero) -> np.ndarray:
        mapa = tablero.tablero
        fire_map: np.ndarray = np.full(tablero.size, -1)
        queue: Queue[tuple[Cuadricula, int]] = Queue()
        for fila in mapa:
            for celda in fila:
                if celda.tipo == TipoCuadricula.FUEGO:
                    queue.put((celda, 0))
                    fire_map[celda.pos] = 0

        while not queue.empty():
            celda, n = queue.get()
            for vecino in celda.vecinos:
                if vecino is None or fire_map[vecino.pos] != -1:
                    continue
                queue.put((vecino, n + self.fire_time))
                fire_map[vecino.pos] = n + self.fire_time
        return fire_map  # pyright: ignore[reportUnknownVariableType]

    def step(self, imprimir: bool) -> tuple[int, int]:
        fuego = self.tiempo_global != 0 and self.tiempo_global % self.fire_time == 0
        if fuego:
            self.tablero.propagarFuego()
        for agente in self.agentes:
            prev_pos = agente.pos
            if self.getCuadricula(
                agente.pos
            ).tipo == TipoCuadricula.FUEGO and not isinstance(
                agente.state, AgenteMuerto
            ):
                agente.state = AgenteMuerto()
                self.atochamiento_agentes[prev_pos] -= 1
            if fuego:
                agente.recalc(self)
            agente.update(self)
            if prev_pos != agente.pos:
                self.atochamiento_agentes[prev_pos] -= 1
                if not isinstance(agente.state, (AgenteMuerto, AgenteTermino)):
                    self.atochamiento_agentes[agente.pos] += 1

        self.tiempo_global += 1
        if imprimir:
            self.imprimir()
        return len(self.agentesCorriendo()), len(
            list(filter(lambda x: isinstance(x.state, AgenteMuerto), self.agentes))
        )

    def imprimir(self):
        sleep(0.2)
        os.system("clear")
        for i in self.tablero.tablero:
            for j in i:
                if j.tipo == TipoCuadricula.SALIDA:
                    print("\033[48;2;0;255;0m!\033[0m", end=" ")
                    continue
                if j.tipo == TipoCuadricula.FUEGO:
                    print("\033[48;255;0;10;0mX\033[0m", end=" ")
                    continue
                if j.tipo == TipoCuadricula.MURO:
                    print("#", end=" ")
                    continue
                agentesEnCuadricula = list(
                    filter(lambda x: x.pos == j.pos, self.agentesCorriendo())
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
        print(f"Agentes restantes = {len(self.agentesCorriendo())}")
        print(
            f"Agentes finalizados = {len(self.agentes) - len(self.agentesCorriendo())}"
        )
