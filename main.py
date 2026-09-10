from typing import Deque, List
from enum import Enum
from random import randint
from collections import deque

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
    def update(self, agente: Agente, contexto : Juego):
        "XDE"

class AgenteRandom(AgenteState):
    def update(self,agente: Agente, contexto : Juego):
        mov = randint(0,3)
        x,y = agente.pos
        posibles = contexto.tablero.tablero[x][y].vecinos
        siguiente = posibles[mov]
        if siguiente is not None and siguiente.tipo is TipoCuadricula.CAMINABLE:
            agente.pos = siguiente.pos
        if agente.pos == contexto.objetivo : agente.state = AgenteTermino()

class AgenteDFS(AgenteState):
    def update(self, agente: Agente, contexto: Juego):
        cola : Deque[List[Cuadricula]]
        cola = deque()
        x,y = agente.pos
        cola.append([contexto.tablero.tablero[x][y]])
        caminoFinal = []
        while cola:
            camino = cola.pop()
            nodo = camino[-1] ## el ultimo nodo en el camino es el actual
            for vecino in nodo.vecinos:
                if vecino is None or vecino.tipo is not TipoCuadricula.CAMINABLE: continue
                if vecino.pos is juego.objetivo:
                    camino.append(nodo)
                    caminoFinal = camino
                    break
                nuevoCamino = camino.copy()
                nuevoCamino.append(nodo)
                cola.appendleft(nuevoCamino)
            if caminoFinal is not None: break
        if caminoFinal is not None and len(caminoFinal) >= 2: agente.pos = caminoFinal[1].pos
        if agente.pos is juego.objetivo: agente.state = AgenteTermino()

class AgenteTermino(AgenteState): # indica que el agente dejó de actuar
    def update(self, agente, contexto):
        pass

class Agente:
    pos : tuple[int,int] #(x,y)
    state : AgenteState

    def __init__(self,x,y, state = AgenteRandom()) -> None:
        self.pos = (x,y)
        self.state = state

    def update(self,contexto : Juego):
        self.state.update(self,contexto)

class Juego:
    tablero : Tablero
    agentes : List[Agente]
    objetivo : tuple[int,int]

    def __init__(self, pos: tuple[int,int], obj: tuple[int,int]):
        self.tablero = Tablero(pos)
        self.agentes = []
        self.objetivo = obj

    def step(self):
        for agente in self.agentes:
            agente.update(self)
        for i in self.tablero.tablero:
            for j in i:
                count = len(list(filter(lambda x: x.pos is j.pos, self.agentes)))
                print('_' if count is 0 else count ,end=' ')
                
            print()
        agentesListos = len(list(filter(lambda x: isinstance(x.state,AgenteTermino),self.agentes)))
        print(f"Agentes listos = {agentesListos}")
        input()

juego = Juego((5,5), (1,0))

for i in range(3):
    x = randint(0,4)
    y = randint(0,4)
    juego.agentes.append(Agente(x,y))

while True:
    juego.step()
