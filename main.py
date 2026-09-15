from random import randint
from juego import Juego
from agentes import Agente, AgenteBFS, AgenteDFS
from mapas import *

x_size = 15
y_size = 15
def genPos(): return (randint(0,x_size-1),randint(0,y_size-1))

juego = Juego.fromMap(mapa_1)

for i in range(3):
    x,y = genPos()
    juego.agentes.append(Agente(x,y))
x,y = genPos()
juego.agentes.append(Agente(x,y,AgenteDFS()))
x,y = genPos()
juego.agentes.append(Agente(x,y,AgenteBFS()))

while True:
    juego.step()
