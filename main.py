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
        if siguiente is not None and siguiente.tipo == TipoCuadricula.CAMINABLE:
            agente.pos = siguiente.pos
        if agente.pos == contexto.objetivo : agente.state = AgenteTermino()

class AgenteDFS(AgenteState):
    def __init__(self):
        self.camino: List[Cuadricula] = []
        self.camino_idx: int = 0

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

class AgenteTermino(AgenteState): # indica que el agente dejó de actuar
    def update(self, agente, contexto):
        pass

class Agente:
    pos : tuple[int,int] #(x,y)
    state : AgenteState

    def __init__(self,x,y, state : AgenteState = AgenteRandom()) -> None:
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
        print(f"Agentes restantes = {len(self.agentes) - agentesListos}")
        print(f"Posicion DFS = {list(filter(lambda x: isinstance(x.state,AgenteDFS),self.agentes)).pop().pos}")
        input()

juego = Juego((5,5), (1,0))

for i in range(3):
    x = randint(0,4)
    y = randint(0,4)
    juego.agentes.append(Agente(x,y))
juego.agentes.append(Agente(randint(0,4),randint(0,4),AgenteDFS()))

while True:
    juego.step()
