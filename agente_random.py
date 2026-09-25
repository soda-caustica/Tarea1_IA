from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, override

from agente_state import AgenteState

if TYPE_CHECKING:
    from agente import Agente
    from juego import Juego


class AgenteRandom(AgenteState):
    @override
    def update(self, agente: Agente, contexto: Juego):
        mov = randint(0, 3)
        x, y = agente.pos
        posibles = contexto.tablero.tablero[x][y].vecinos
        siguiente = posibles[mov]
        if siguiente is None:
            return
        self.avanzar(agente, siguiente, contexto)

    @override
    def color(self):
        return (127, 255, 212)

    @override
    def recalc(self, contexto: Juego):
        pass