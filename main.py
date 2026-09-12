from abc import abstractmethod
from typing import Deque, List
from enum import Enum
from random import randint
from collections import deque
import os
import time

class TipoCuadricula(Enum):
    CAMINABLE = 1
    MURO = 2
    FUEGO = 3

class Cuadricula:
    # IMPLEMENTACION SIN PESOS!!!
    tipo : TipoCuadricula
    pos : tuple[int,int]
    vecinos : tuple[Cuadricula | None, Cuadricula | None, Cuadricula | None, Cuadricula | None] # (N,S,E,W)

    def __init__(self,x,y,tipo = TipoCuadricula.CAMINABLE):
        self.tipo = tipo
        self.pos = (x,y)

class Tablero:
    tablero : List[List[Cuadricula]]
    size : tuple[int,int] 

    def __init__(self, size: tuple[int,int]):
        self.size = size
        x,y = self.size
        self.tablero = []
        for i in range(x):
            self.tablero.append([])
            for j in range(y):
                self.tablero[i].append(Cuadricula(i,j))

        for i in range(x):
            for j in range(y):
                cuadricula = self.tablero[i][j]
                N,S,E,W = (None,None,None,None)

                if i > 0:
                    W = self.tablero[i - 1][j]
                if i + 1 < x:
                    E = self.tablero[i + 1][j]
                if j > 0:
                    N = self.tablero[i][j - 1]

                if j + 1 < y:
                    S = self.tablero[i][j + 1]

                cuadricula.vecinos = (N, S, E, W)

class AgenteState: 
    #INTERFAZ, SOLO HEREDAR, NO IMPLEMENTAR
    @abstractmethod
    def update(self, agente: Agente, contexto : Juego):
        ""
    @abstractmethod
    def color(self) -> tuple[int,int,int]: #podriamos quitar esta funcion, solo la puse para tener una interfaz bkn
        ""

class AgenteRandom(AgenteState):

    def update(self,agente: Agente, contexto : Juego):
        mov = randint(0,3)
        x,y = agente.pos
        posibles = contexto.tablero.tablero[x][y].vecinos
        siguiente = posibles[mov]
        if siguiente is not None and siguiente.tipo == TipoCuadricula.CAMINABLE:
            agente.pos = siguiente.pos
        if agente.pos == contexto.objetivo : agente.state = AgenteTermino()
    def color(self): return (127,255,212)

class AgenteTermino(AgenteState): # indica que el agente dejó de actuar
    def update(self, agente, contexto):
        pass
    def color(self): return (255,0,0)

class Agente:
    pos : tuple[int,int] #(x,y)
    state : AgenteState

    def __init__(self,x,y, state : AgenteState = AgenteRandom()) -> None:
        self.pos = (x,y)
        self.state = state 

    def update(self,contexto : Juego) -> None:
        self.state.update(self,contexto)

    def color(self) -> tuple[int,int,int]:
        return self.state.color()

class AgenteBFS(AgenteState):

    def color(self): return (255,105,180)

    def update(self, agente: Agente, contexto: Juego):
        camino = self._buscar_camino(agente,contexto)

        if len(camino) >= 2 : agente.pos = camino[1].pos

        if agente.pos == contexto.objetivo:
            agente.state = AgenteTermino()

    def _buscar_camino(self, agente: Agente, contexto: Juego) -> List[Cuadricula]:
        inicio = contexto.tablero.tablero[agente.pos[0]][agente.pos[1]]
        objetivo = contexto.objetivo

        pila: Deque[List[Cuadricula]] = deque()
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
                if vecino.tipo is not TipoCuadricula.CAMINABLE:
                    continue
                if vecino.pos in visitados:
                    continue

                visitados.add(vecino.pos)
                nuevo_camino = camino + [vecino]
                pila.append(nuevo_camino)

        return []

class AgenteDFS(AgenteState):
    def __init__(self):
        self.camino: List[Cuadricula] = []
        self.camino_idx: int = 0

    def color(self) : return (255,255,0)

    def update(self, agente: Agente, contexto: Juego):
        if not self.camino:
            self.camino = self._buscar_camino(agente, contexto)
            self.camino_idx = 0

        if not self.camino:
            agente.state = AgenteTermino()
            return

        self.camino_idx += 1
        if self.camino_idx < len(self.camino):
            agente.pos = self.camino[self.camino_idx].pos

        if agente.pos == contexto.objetivo:
            agente.state = AgenteTermino()

    def _buscar_camino(self, agente: Agente, contexto: Juego) -> List[Cuadricula]:
        inicio = contexto.tablero.tablero[agente.pos[0]][agente.pos[1]]
        objetivo = contexto.objetivo

        pila: Deque[List[Cuadricula]] = deque()
        pila.append([inicio])
        visitados = {inicio.pos}

        while pila:
            camino = pila.pop()
            nodo = camino[-1]

            if nodo.pos == objetivo:
                return camino  

            for vecino in nodo.vecinos:
                if vecino is None:
                    continue
                if vecino.tipo is not TipoCuadricula.CAMINABLE:
                    continue
                if vecino.pos in visitados:
                    continue

                visitados.add(vecino.pos)
                nuevo_camino = camino + [vecino]
                pila.append(nuevo_camino)

        return []

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

x_size = 20
y_size = 20
def genPos(): return (randint(0,x_size-1),randint(0,y_size-1))

juego = Juego((x_size,y_size), genPos())

for i in range(3):
    x,y = genPos()
    juego.agentes.append(Agente(x,y))
x,y = genPos()
juego.agentes.append(Agente(x,y,AgenteDFS()))
x,y = genPos()
juego.agentes.append(Agente(x,y,AgenteBFS()))

while True:
    juego.step()
