from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, override

from agente_state import AgenteState
from grafo import *

if TYPE_CHECKING:
    from agente import Agente
    from juego import Juego


class AgenteBFS(AgenteState):
    @override
    def color(self):
        return (255, 105, 180)

    def __init__(self):
        self.camino: list[Cuadricula] = []
        self.camino_idx: int = 0

    @override
    def recalc(self, contexto: Juego):
        for c in self.camino:
            if (
                contexto.tablero.tablero[c.pos[0]][c.pos[1]].tipo
                == TipoCuadricula.FUEGO
            ):
                self.camino = []
                return

    @override
    def update(self, agente: Agente, contexto: Juego):
        if not self.camino:
            self.camino = self._buscar_camino(agente, contexto)
            self.camino_idx = 0

        if not self.camino:
            return

        self.camino_idx += 1
        if self.camino_idx < len(self.camino):
            self.avanzar(agente, self.camino[self.camino_idx], contexto)

    def _buscar_camino(self, agente: Agente, contexto: Juego) -> list[Cuadricula]:
        inicio = contexto.tablero.tablero[agente.pos[0]][agente.pos[1]]
        objetivo = contexto.objetivo

        pila: deque[list[Cuadricula]] = deque()
        pila.append([inicio])
        visitados = {inicio.pos}

        while pila:
            camino = pila.popleft()
            nodo = camino[-1]

            if nodo.pos == objetivo:
                return camino

            for vecino in nodo.vecinos:
                if vecino is None:
                    continue
                if vecino.tipo not in (TipoCuadricula.CAMINABLE, TipoCuadricula.SALIDA):
                    continue
                if vecino.pos in visitados:
                    continue

                visitados.add(vecino.pos)
                nuevo_camino = camino + [vecino]
                pila.append(nuevo_camino)

        return []