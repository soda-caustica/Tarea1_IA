from __future__ import annotations

import os
import time
from grafo import *
from agentes import Agente, AgenteTermino

class Juego:
    tablero : Tablero
    agentes : List[Agente]
    objetivo : tuple[int,int]

    def __init__(self, pos: tuple[int,int], obj: tuple[int,int]):
        self.tablero = Tablero(pos)
        self.agentes = []
        self.objetivo = obj

    def step(self):
        os.system('clear')
        for agente in self.agentes:
            agente.update(self)
        agentesCorriendo = list(filter(lambda x: not isinstance(x.state,AgenteTermino),self.agentes))
        # La seccion de abajo imprime los agentes en pantalla, es re innecesaria
        for i in self.tablero.tablero:
            for j in i:
                if j.pos == self.objetivo:
                    print("\033[48;2;0;255;0mX\033[0m", end = ' ')
                    continue
                agentesEnCuadricula = list(filter(lambda x: x.pos is j.pos, agentesCorriendo))
                count = len(agentesEnCuadricula)
                color =  agentesEnCuadricula[0].color() if count > 0 else (255,255,255)
                print('_' if count == 0 else f"\033[48;2;{color[0]};{color[1]};{color[2]}m" + str(count) + "\033[0m",end=' ')
            print()
        print(f"Agentes restantes = {len(agentesCorriendo)}")
        print(f"Agentes listos = {len(self.agentes) - len(agentesCorriendo)}")
        time.sleep(0.2)
#        input()

