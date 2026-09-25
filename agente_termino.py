from __future__ import annotations

from typing import TYPE_CHECKING, override

from agente_state import AgenteState

if TYPE_CHECKING:
    from agente import Agente
    from juego import Juego


class AgenteTermino(AgenteState):
    @override
    def update(self, agente: Agente, contexto: Juego):
        pass

    @override
    def color(self):
        return (255, 0, 0)

    @override
    def recalc(self, contexto: Juego):
        pass