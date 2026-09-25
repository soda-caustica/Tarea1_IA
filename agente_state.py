from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from grafo import *

if TYPE_CHECKING:
    from agente import Agente
    from juego import Juego


class AgenteState(ABC):
    @abstractmethod
    def update(self, agente: Agente, contexto: Juego):
        ""

    @abstractmethod
    def color(
        self,
    ) -> tuple[
        int, int, int
    ]:  # podriamos quitar esta funcion, solo la puse para tener una interfaz bkn
        ""

    def avanzar(self, agente: Agente, cuadricula: Cuadricula, contexto: Juego):
        if cuadricula not in contexto.getCuadricula(
            agente.pos
        ).vecinos or cuadricula.tipo not in (
            TipoCuadricula.CAMINABLE,
            TipoCuadricula.SALIDA,
        ):
            return
        if cuadricula.tipo == TipoCuadricula.SALIDA:
            from agente_termino import AgenteTermino

            agente.state = AgenteTermino()
        agente.time_left += contexto.costo(cuadricula.pos)
        agente.pos = cuadricula.pos

    @abstractmethod
    def recalc(self, contexto: Juego):
        ""