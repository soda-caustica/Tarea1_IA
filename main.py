from random import randint
from juego import Juego
from agentes import Agente, AgenteBFS, AgenteDFS, AgenteDijkstra, AgenteRandom
from mapas import *
import time

x_size = 15
y_size = 15
def genPos(): return (randint(0,x_size-1),randint(0,y_size-1))
mapa = mapa_2
salida = np.where(mapa == TipoCuadricula.SALIDA.value)

def func() :
    juego = Juego.fromMap(mapa)
    i = 0
    for i in range(50):
        x,y = genPos()
        while (x,y) == salida : x,y = genPos()
        juego.agentes.append(Agente(x,y,AgenteDFS()))
    while True:
        i += 1
        restantes = juego.step()
        if restantes == 0: break
    return i

avg = 0
a = 0

for k in range(25):
    a += 1
    avg += func()
    print(f'terminado {a}/25')

print(f'En promedio el agente de este tipo demoró {avg/50} turnos en encontrar la salida')
