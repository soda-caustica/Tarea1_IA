import heapq
from typing import TYPE_CHECKING, override

from grafo import TipoCuadricula
from agente_state import AgenteState

if TYPE_CHECKING:
    from agente import Agente
    from juego import Juego

Coord = tuple[int, int]

# Implementamos una version online de Beam Search


class AgenteBeam(AgenteState):
    depth: int = 5  # lo haremos local para ser mejor
    beam_length: int = 7

    def __init__(self, depth: int = 5, beam_length: int = 7):
        super().__init__()
        self.depth = depth
        self.beam_length = beam_length
        self.camino: list[Coord] = []
        self.idx: int = 1

    @override
    def color(self) -> tuple[int, int, int]:
        return (10, 10, 122)

    def _buscar_camino(self, agente: Agente, contexto: Juego):
        objetivo = contexto.objetivo
        if agente.pos == objetivo:
            self.camino = [agente.pos]
            return

        h_inicial = int(contexto.heuristica[agente.pos])
        if h_inicial < 0:
            self.camino = [agente.pos]
            return

        beam: list[tuple[int, int, list[Coord]]] = [(h_inicial, 0, [agente.pos])]

        for _ in range(self.depth):
            candidatos: dict[Coord, tuple[int, int, list[Coord]]] = {}
            caminos_meta: list[tuple[int, list[Coord]]] = []

            for _, g, camino in beam:
                actual = camino[-1]

                casilla = contexto.getCuadricula(actual)

                for vecino in casilla.vecinos:
                    if vecino is None or vecino.tipo not in (
                        TipoCuadricula.CAMINABLE,
                        TipoCuadricula.SALIDA,
                    ):
                        continue

                    pos_vecino = vecino.pos
                    if pos_vecino in camino:
                        continue

                    nuevo_g = g + contexto.costo(pos_vecino)
                    nuevo_camino = camino + [pos_vecino]
                    if pos_vecino == objetivo:
                        caminos_meta.append((nuevo_g, nuevo_camino))
                        continue

                    h = int(contexto.heuristica[pos_vecino])
                    if h < 0:
                        continue

                    candidato = (nuevo_g + h, nuevo_g, nuevo_camino)
                    previo = candidatos.get(pos_vecino)
                    if previo is None or candidato[:2] < previo[:2]:
                        candidatos[pos_vecino] = candidato

            if caminos_meta:
                self.camino = min(caminos_meta, key=lambda x: x[0])[1]
                return

            if not candidatos:
                break

            beam = heapq.nsmallest(
                self.beam_length,
                candidatos.values(),
                key=lambda x: (
                    x[0],
                    int(contexto.heuristica[x[2][-1]]),
                    x[1],
                ),
            )

        if beam:
            _, _, mejor_camino = min(
                beam,
                key=lambda x: (
                    x[0],
                    int(contexto.heuristica[x[2][-1]]),
                    x[1],
                ),
            )
            self.camino = mejor_camino
        else:
            self.camino = [agente.pos]

    @override
    def update(self, agente: Agente, contexto: Juego, debeCaminar: bool):
        if not debeCaminar:
            return

        if not self.camino or self.idx >= len(self.camino):
            self._buscar_camino(agente, contexto)
            self.idx = 1

        if self.idx >= len(self.camino):
            return

        self.avanzar(agente, contexto.getCuadricula(self.camino[self.idx]), contexto)
        self.idx += 1

    @override
    def recalc(self, contexto: Juego):
        self.camino = []
        self.idx = 1
