from typing import List
from enum import Enum
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

                N = None
                S = None
                E = None
                W = None

                # Oeste
                if i > 0:
                    W = self.tablero[i - 1][j]

                # Este
                if i + 1 < x:
                    E = self.tablero[i + 1][j]

                # Norte
                if j > 0:
                    N = self.tablero[i][j - 1]

                # Sur
                if j + 1 < y:
                    S = self.tablero[i][j + 1]

                cuadricula.vecinos = (N, S, E, W)


