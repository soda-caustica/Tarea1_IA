from typing import TYPE_CHECKING, override

from agente import Agente
from agente_state import AgenteState
from grafo import TipoCuadricula

if TYPE_CHECKING:
    from juego import Juego


class AgenteGreedy(AgenteState):
    @override
    def update(self, agente: Agente, contexto: Juego, debeCaminar: bool):
        if not debeCaminar:
            return
        vecinos = [
            x
            for x in contexto.getCuadricula(agente.pos).vecinos
            if x is not None
            and x.tipo in (TipoCuadricula.SALIDA, TipoCuadricula.CAMINABLE)
        ]
        if vecinos:
            siguiente = min(vecinos, key=lambda x: contexto.heuristica[x.pos])
            self.avanzar(
                agente,
                siguiente,
                contexto,
            )

    @override
    def recalc(
        self, contexto: Juego
    ):  # greedy no planea a largo plazo, asi que no necesita recalcular en caso de fuego
        pass

    @override
    def color(self):
        return (123, 12, 222)
