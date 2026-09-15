from __future__ import annotations

import os
import time
import numpy as np
from grafo import *
from agentes import Agente, AgenteTermino

class Juego:
    tablero : Tablero
    agentes : List[Agente]
    objetivo : tuple[int,int]


    def costo(self, pos: tuple[int,int]) -> float:
        agentesCorriendo = filter(lambda x: not isinstance(x.state,AgenteTermino),self.agentes)
        agentesEnCuadricula = list(filter(lambda x: x.pos == pos, agentesCorriendo))
        return len(agentesEnCuadricula) + 1


    def getCuadricula(self, pos : tuple[int,int]) -> Cuadricula:
        x,y = pos
        return self.tablero.tablero[x][y]

    def __init__(self, tablero : Tablero, obj : tuple[int,int], agentes : List[Agente] = [],):
        self.tablero = tablero
        self.agentes = agentes

        try:
            x,y = obj
            self.objetivo = obj
            print(f'obj = {obj}')
            assert tablero.tablero[x][y].tipo == TipoCuadricula.SALIDA
        except Exception:
            raise ValueError("El objetivo entregado no es una salida en el tablero")

    @classmethod
    def tableroVacio(cls, size: tuple[int,int], obj: tuple[int,int], agentes : List[Agente] = []):
        return cls(Tablero.vacio(size,obj),obj, agentes)

    @classmethod
    def fromMap(cls, mapa: np.ndarray, agentes : List[Agente] = []):
        filas, columnas = np.where(mapa == TipoCuadricula.SALIDA.value)
        if filas.size == 0:
            raise ValueError("El mapa no contiene una salida")
        return cls(Tablero.fromMap(mapa),(filas[0], columnas[0]),agentes)

    def step(self):
        os.system('clear')
        for agente in self.agentes:
            agente.update(self)
        agentesCorriendo = list(filter(lambda x: not isinstance(x.state,AgenteTermino),self.agentes))
        # La seccion de abajo imprime los agentes en pantalla, es re innecesaria
        for i in self.tablero.tablero:
            for j in i:
                if j.tipo == TipoCuadricula.SALIDA:
                    print("\033[48;2;0;255;0mX\033[0m", end = ' ')
                    continue
                agentesEnCuadricula = list(filter(lambda x: x.pos == j.pos, agentesCorriendo))
                count = len(agentesEnCuadricula)
                color =  agentesEnCuadricula[0].color() if count > 0 else (255,255,255)
                print('_' if count == 0 else f"\033[48;2;{color[0]};{color[1]};{color[2]}m" + str(count) + "\033[0m",end=' ')
            print()
        print(f"Agentes restantes = {len(agentesCorriendo)}")
        print(f"Agentes listos = {len(self.agentes) - len(agentesCorriendo)}")
        time.sleep(0.2)
#        input()

