from __future__ import annotations

from typing import TYPE_CHECKING

from agente_random import AgenteRandom
from agente_state import AgenteState

if TYPE_CHECKING:
    from juego import Juego


class Agente:
    pos: tuple[int, int]
    state: AgenteState
    time_left: int = 0

    def __init__(self, x: int, y: int, state: AgenteState | None = None) -> None:
        self.pos = (x, y)
        self.state = state if state is not None else AgenteRandom()

    def update(self, contexto: Juego) -> None:
        self.time_left = max(self.time_left - 1, 0)
        if self.time_left == 0:
            self.state.update(self, contexto)

    def color(self) -> tuple[int, int, int]:
        return self.state.color()