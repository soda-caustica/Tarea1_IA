from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, override

from agente_state import AgenteState
from grafo import *

if TYPE_CHECKING:
    from agente import Agente
    from juego import Juego


class AgenteDijkstra(AgenteState):
    @override
    def color(self):
        return (0, 0, 255)

    def __init__(self):
        self.camino: list[Cuadricula] = []
        self.camino_idx: int = 0

    @override
    def update(self, agente: Agente, contexto: Juego, debeCaminar: bool):
        if not debeCaminar:
            return
        if not self.camino:
            self.camino = self._buscar_camino(agente, contexto)
            self.camino_idx = 0

        if not self.camino:
            return

        self.camino_idx += 1
        if self.camino_idx < len(self.camino):
            self.avanzar(agente, self.camino[self.camino_idx], contexto)

    @override
    def recalc(self, contexto: Juego):
        for c in self.camino:
            if (
                contexto.tablero.tablero[c.pos[0]][c.pos[1]].tipo
                == TipoCuadricula.FUEGO
            ):
                self.camino = []
                return

    def _buscar_camino(self, agente: Agente, contexto: Juego) -> list[Cuadricula]:
        inicio = contexto.tablero.tablero[agente.pos[0]][agente.pos[1]]
        objetivo = contexto.objetivo

        heap: list[tuple[int, int, tuple[int, int]]] = []
        heapq.heappush(heap, (0, 0, inicio.pos))
        mejor_coste = {inicio.pos: 0}
        anterior: dict[tuple[int, int], tuple[int, int]] = {}
        contador = 1

        while heap:
            coste_actual, _, posicion = heapq.heappop(heap)
            nodo = contexto.tablero.tablero[posicion[0]][posicion[1]]

            if coste_actual > mejor_coste.get(nodo.pos, float("inf")):
                continue

            if nodo.pos == objetivo:
                camino: list[Cuadricula] = []
                posicion_actual = objetivo
                while posicion_actual != inicio.pos:
                    camino.append(
                        contexto.tablero.tablero[
                            posicion_actual[0]
                        ][posicion_actual[1]]
                    )
                    posicion_actual = anterior[posicion_actual]
                camino.append(inicio)
                camino.reverse()
                return camino

            for vecino in nodo.vecinos:
                if vecino is None:
                    continue
                if vecino.tipo not in (TipoCuadricula.CAMINABLE, TipoCuadricula.SALIDA):
                    continue

                costo_vecino = coste_actual + contexto.costo(vecino.pos)
                if (
                    vecino.pos not in mejor_coste
                    or costo_vecino < mejor_coste[vecino.pos]
                ):
                    mejor_coste[vecino.pos] = costo_vecino
                    anterior[vecino.pos] = nodo.pos
                    heapq.heappush(heap, (costo_vecino, contador, vecino.pos))
                    contador += 1

        return []

