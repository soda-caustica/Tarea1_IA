from typing import List
from enum import Enum
from random import randint
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
    # x,y
    def __init__(self, x : int,y : int):
        self.size = (x,y)
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
        if siguiente is not None and siguiente.tipo == TipoCuadricula.CAMINABLE:
            agente.pos = siguiente.pos

class Agente:
    pos : tuple[int,int] #(x,y)
    state : AgenteState

    def __init__(self,x,y, state = AgenteRandom()) -> None:
        self.pos = (x,y)
        self.state = state

    def update(self,juego : Juego):
        self.state.update(self,juego)

class Juego:
    tablero : Tablero
    agentes : List[Agente]

    def __init__(self, x: int, y: int):
        self.tablero = Tablero(x,y)
        self.agentes = []

    def step(self):
        for agente in self.agentes:
            agente.update(self)
        for i in self.tablero.tablero:
            for j in i:
                count = len(list(filter(lambda x: x.pos == j.pos, self.agentes)))
                print('_' if count == 0 else count ,end=' ')
            print()
        input()

juego = Juego(5,5)

for i in range(3):
    x = randint(0,4)
    y = randint(0,4)
    juego.agentes.append(Agente(x,y))

while True:
    juego.step()
