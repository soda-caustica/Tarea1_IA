from __future__ import annotations

from abc import abstractmethod
import heapq
from typing import TYPE_CHECKING, Deque, List
from collections import deque
from random import randint
from grafo import *

if TYPE_CHECKING:
    from juego import Juego

class AgenteState: 
    #INTERFAZ, SOLO HEREDAR, NO IMPLEMENTAR
    @abstractmethod
    def update(self, agente: Agente, contexto : Juego):
        ""
    @abstractmethod
    def color(self) -> tuple[int,int,int]: #podriamos quitar esta funcion, solo la puse para tener una interfaz bkn
        ""

    def avanzar(self, agente: Agente, cuadricula: Cuadricula, contexto : Juego):
        if cuadricula not in contexto.getCuadricula(agente.pos).vecinos or cuadricula.tipo not in (TipoCuadricula.CAMINABLE,TipoCuadricula.SALIDA):
            return
        if cuadricula.tipo == TipoCuadricula.SALIDA:
            agente.state = AgenteTermino()
        agente.time_left += contexto.costo(cuadricula.pos)
        agente.pos = cuadricula.pos

class AgenteRandom(AgenteState):

    def update(self,agente: Agente, contexto : Juego):
        mov = randint(0,3)
        x,y = agente.pos
        posibles = contexto.tablero.tablero[x][y].vecinos
        siguiente = posibles[mov]
        if siguiente is None:
            return
        self.avanzar(agente,siguiente,contexto)

    def color(self): return (127,255,212)

class AgenteTermino(AgenteState): # indica que el agente dejó de actuar
    def update(self, agente, contexto):
        pass
    def color(self): return (255,0,0)

class Agente:
    pos : tuple[int,int] #(x,y)
    state : AgenteState
    time_left : int = 0 # Si un agente camina hacia una casilla con muchos agentes, tendra que esperar a poder pasar

    def __init__(self,x,y, state : AgenteState = AgenteRandom()) -> None:
        self.pos = (x,y)
        self.state = state 

    def update(self,contexto : Juego) -> None:
        self.time_left = max(self.time_left-1,0)
        if (self.time_left == 0):
            self.state.update(self,contexto)

    def color(self) -> tuple[int,int,int]:
        return self.state.color()

class AgenteDijkstra(AgenteState):

    def color(self): return (0,0,255)

    def update(self, agente: Agente, contexto: Juego):
        camino = self._buscar_camino(agente, contexto)

        if len(camino) >= 2:
            self.avanzar(agente, camino[1], contexto)

        if contexto.getCuadricula(agente.pos).tipo == TipoCuadricula.SALIDA:
            agente.state = AgenteTermino()

    def _buscar_camino(self, agente: Agente, contexto: Juego) -> List[Cuadricula]:
        inicio = contexto.tablero.tablero[agente.pos[0]][agente.pos[1]]
        objetivo = contexto.objetivo

        heap: List[tuple[int, int, List[Cuadricula]]] = []
        heapq.heappush(heap, (0, 0, [inicio]))
        mejor_coste = {inicio.pos: 0}
        contador = 1

        while heap:
            coste_actual, _, camino = heapq.heappop(heap)
            nodo = camino[-1]

            if coste_actual > mejor_coste.get(nodo.pos, float('inf')):
                continue

            if nodo.pos == objetivo:
                return camino

            for vecino in nodo.vecinos:
                if vecino is None:
                    continue
                if vecino.tipo not in (TipoCuadricula.CAMINABLE, TipoCuadricula.SALIDA):
                    continue

                costo_vecino = coste_actual + contexto.costo(vecino.pos)
                if vecino.pos not in mejor_coste or costo_vecino < mejor_coste[vecino.pos]:
                    mejor_coste[vecino.pos] = costo_vecino
                    heapq.heappush(heap, (costo_vecino, contador, camino + [vecino]))
                    contador += 1

        return []

class AgenteBFS(AgenteState):

    def color(self): return (255,105,180)

    def update(self, agente: Agente, contexto: Juego) -> None:
        camino = self._buscar_camino(agente,contexto)

        if len(camino) >= 2 : 
            self.avanzar(agente,camino[1],contexto)

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
                if vecino.tipo not in (TipoCuadricula.CAMINABLE, TipoCuadricula.SALIDA):
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
            return

        self.camino_idx += 1
        if self.camino_idx < len(self.camino):
            self.avanzar(agente,self.camino[self.camino_idx],contexto)

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
                if vecino.tipo not in (TipoCuadricula.CAMINABLE, TipoCuadricula.SALIDA):
                    continue
                if vecino.pos in visitados:
                    continue

                visitados.add(vecino.pos)
                nuevo_camino = camino + [vecino]
                pila.append(nuevo_camino)

        return []

