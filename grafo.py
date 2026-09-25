from enum import Enum

import numpy as np


class TipoCuadricula(Enum):
    CAMINABLE = 1
    MURO = 2
    SALIDA = 3
    FUEGO = 4


class Cuadricula:
    # IMPLEMENTACION SIN PESOS!!!
    tipo: TipoCuadricula
    pos: tuple[int, int]
    vecinos: tuple[
        Cuadricula | None, Cuadricula | None, Cuadricula | None, Cuadricula | None  # noqa: F821
    ]  # (N,S,E,W)

    def __init__(self, x: int, y: int, tipo: TipoCuadricula = TipoCuadricula.CAMINABLE):
        self.tipo = tipo
        self.pos = (x, y)
        self.vecinos = (None, None, None, None)


class Tablero:
    tablero: list[list[Cuadricula]]
    size: tuple[int, int]

    def __init__(self, tablero: list[list[Cuadricula]], size: tuple[int, int]) -> None:
        self.tablero = tablero
        self.size = size

    @classmethod
    def vacio(cls, size: tuple[int, int], obj: tuple[int, int]):
        mapa = np.full(size, TipoCuadricula.CAMINABLE.value)
        mapa[obj] = TipoCuadricula.SALIDA.value

        return cls.fromMap(mapa)

    @classmethod
    def fromMap(cls, mapa: np.ndarray):

        if mapa.ndim != 2:
            raise ValueError("Dimensiones incorrectas del mapa, esto no deberia pasar")
        x, y = (mapa.shape[0], mapa.shape[1])
        tablero: list[list[Cuadricula]] = []
        for i in range(x):
            tablero.append([])
            for j in range(y):
                tablero[i].append(Cuadricula(i, j, tipo=TipoCuadricula(mapa[i, j])))

        for i in range(x):
            for j in range(y):
                cuadricula = tablero[i][j]
                n, s, e, w = (None, None, None, None)

                if i > 0:
                    n = tablero[i - 1][j]
                if i + 1 < x:
                    s = tablero[i + 1][j]
                if j > 0:
                    w = tablero[i][j - 1]
                if j + 1 < y:
                    e = tablero[i][j + 1]

                cuadricula.vecinos = (n, s, e, w)

        return cls(tablero, (x, y))
