from random import randint
from juego import Juego
from agentes import Agente, AgenteBFS, AgenteDFS

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
