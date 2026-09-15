from typing import List
from enum import Enum
import numpy as np

class TipoCuadricula(Enum):
    CAMINABLE = 1
    MURO = 2
    SALIDA = 3
    FUEGO = 4

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

    def __init__(self, tablero, size) -> None:
        self.tablero = tablero
        self.size = size

    @classmethod
    def fromMap(cls, mapa : np.ndarray):

        if mapa.ndim != 2:
            raise ValueError("Dimensiones incorrectas del mapa, esto no deberia pasar")
        x,y = (mapa.shape[0],mapa.shape[1])
        tablero : List[List[Cuadricula]] = []
        for i in range(x):
            tablero.append([])
            for j in range(y):
                tablero[i].append(Cuadricula(i,j,tipo= TipoCuadricula(mapa[i,j])))

        for i in range(x):
            for j in range(y):
                cuadricula = tablero[i][j]
                N,S,E,W = (None,None,None,None)

                if i > 0:
                    N = tablero[i - 1][j]
                if i + 1 < x:
                    S = tablero[i + 1][j]
                if j > 0:
                    W = tablero[i][j - 1]
                if j + 1 < y:
                    E = tablero[i][j + 1]

                cuadricula.vecinos = (N, S, E, W)

        return cls(tablero,(x,y))

    @classmethod
    def vacio(cls, size: tuple[int,int], obj: tuple[int,int]) -> Tablero:
        mapa = np.full(size,TipoCuadricula.CAMINABLE.value)
        mapa[obj] = TipoCuadricula.SALIDA.value

        print(mapa[obj])
        print(mapa)
        return cls.fromMap(mapa)

