import random
from enum import Enum
from typing import TYPE_CHECKING, override

from agente import Agente
from agente_state import AgenteState, TipoCuadricula
from grafo import Cuadricula

if TYPE_CHECKING:
    from juego import Juego


class Acciones(Enum):
    ARRIBA = (0,)
    ABAJO = (1,)
    IZQUIERDA = (2,)
    DERECHA = (3,)
    WAIT = (4,)


Candidato = list[Acciones]


class AgenteGenetico(AgenteState):
    pop_size: int = 0
    pop: list[Candidato]
    mejor: Candidato
    horizonte: int = 4
    t: int = 0
    generaciones: int
    tasa_mutacion: float = 0.5

    def __init__(self, pop_size: int = 30, horizonte: int = 6, generaciones: int = 12):
        self.pop = []
        self.mejor = []
        self.pop_size = pop_size
        self.horizonte = horizonte
        self.generaciones = generaciones
        self.t = 0

    @override
    def update(self, agente: Agente, contexto: Juego, debeCaminar: bool):
        if not self.mejor or self.t == self.horizonte:
            self.buscar_camino(agente, contexto)
        if debeCaminar:
            nueva = contexto.getCuadricula(
                self._exec_action(
                    contexto.getCuadricula(agente.pos), self.mejor[self.t]
                )
            )
            self.avanzar(agente, nueva, contexto)
        self.t += 1

    def buscar_camino(self, agente: Agente, contexto: Juego):
        self.pop = []
        self.mejor = []
        self.t = 0
        self.pop_init()
        for i in range(self.generaciones):
            self._selection(agente, contexto)
            self._crossover()
            self._mutate()
        self.mejor = max(self.pop, key=lambda x: self._fitness(x, agente, contexto))

    def pop_init(self):
        for _ in range(self.pop_size):
            self.pop.append(self.pop_create())

    def pop_create(self) -> Candidato:
        candidato: Candidato = random.choices([e for e in Acciones], k=self.horizonte)
        assert len(candidato) == self.horizonte
        return candidato

    def _exec_action(self, cuadricula: Cuadricula, accion: Acciones) -> tuple[int, int]:
        if accion == Acciones.WAIT:
            return cuadricula.pos

        vecino = None
        if accion == Acciones.ARRIBA:
            vecino = cuadricula.vecinos[0]
        elif accion == Acciones.ABAJO:
            vecino = cuadricula.vecinos[1]
        elif accion == Acciones.DERECHA:
            vecino = cuadricula.vecinos[2]
        elif accion == Acciones.IZQUIERDA:
            vecino = cuadricula.vecinos[3]

        return vecino.pos if vecino is not None else cuadricula.pos

    # Esta funcion revisa si el camino es viable
    def _check_camino(
        self, candidato: Candidato, inicio: tuple[int, int], contexto: Juego
    ) -> bool:
        pos_actual = contexto.getCuadricula(inicio)
        for i, accion in enumerate(candidato):
            nueva_pos = self._exec_action(pos_actual, accion)
            siguiente = contexto.getCuadricula(nueva_pos)
            if (
                siguiente.tipo == TipoCuadricula.MURO
                or contexto.fire_map[siguiente.pos] <= contexto.tiempo_global + i
            ):  # el segundo check revisa si esta caminando a una casilla donde ya hay fuego
                return False
            pos_actual = siguiente
        return True

    def _fitness(self, candidato: Candidato, agente: Agente, contexto: Juego) -> int:
        pos_actual = agente.pos
        costo_minimo_salida = self._heuristica(pos_actual, contexto)

        penalizacion_trafico = 0.0
        penalizacion_espera = 0.0
        consecutive_waits = 0
        pasos_validos = 0

        for t, accion in enumerate(candidato):
            tiempo_simulado = contexto.tiempo_global + t

            # Esta parte maneja las esperas, castigando a los agentes que esperan mucho
            if accion == Acciones.WAIT:
                consecutive_waits += 1

                penalizacion_espera += 5.0

                if consecutive_waits >= 2:
                    penalizacion_espera += 15.0 * (2 ** (consecutive_waits - 1))

                # Castigamos si espera cuando el fuego ya viene, ya que probablemente va a verse forzado a elegir algo suboptimo
                margen_fuego = contexto.fire_map[pos_actual] - tiempo_simulado
                if margen_fuego <= 2:
                    return -900 + (t * 10)

                nueva_pos = pos_actual
            else:
                consecutive_waits = 0
                nueva_pos = self._exec_action(
                    contexto.getCuadricula(pos_actual), accion
                )

            if contexto.getCuadricula(nueva_pos).tipo in (
                TipoCuadricula.FUEGO,
                TipoCuadricula.MURO,
            ):
                return -1000 + (t * 10)

            if tiempo_simulado >= contexto.fire_map[nueva_pos]:
                return -800 + (t * 10)

            costo = contexto.costo(nueva_pos)
            factor_descuento = (
                0.7**t
            )  # Estimamos que las casillas a futuro tendran menos gente que ahora, para que el agente se anime a caminar

            # Castigamos quedarse en una casilla con mucha gente, para que aproveche otras casillas mas vacias
            # Y castigamos moverse a casillas con mucha gente
            if accion == Acciones.WAIT:
                if costo > 1:
                    penalizacion_trafico += (costo * 20.0) * factor_descuento
            else:
                penalizacion_trafico += (costo * 25.0) * factor_descuento

            pos_actual = nueva_pos
            pasos_validos += 1

            dist_meta = self._heuristica(pos_actual, contexto)
            costo_minimo_salida = min(
                costo_minimo_salida, dist_meta
            )  # Este costo sirve para recompensar agentes que avanzaron hacia la meta, pero retrocedieron, estos agentes son utiles en el crossover asi que queremos que sobrevivan

            if contexto.getCuadricula(pos_actual).tipo == TipoCuadricula.SALIDA:
                return int(
                    2000
                    + (len(candidato) - t) * 50
                    - penalizacion_trafico
                    - penalizacion_espera
                )

        delta_progreso = self._heuristica(agente.pos, contexto) - costo_minimo_salida
        puntuacion = (
            (delta_progreso * 30.0) - penalizacion_trafico - penalizacion_espera
        )

        # Castigamos los agentes que no se movieron
        if pos_actual == agente.pos and delta_progreso == 0:
            puntuacion -= 150.0

        return int(puntuacion)

    def _heuristica(self, p1: tuple[int, int], contexto: Juego):
        return contexto.bfs_map[p1]

    def _selection(self, agente: Agente, contexto: Juego):
        new_pop = []
        fitnessList = [self._fitness(x, agente, contexto) for x in self.pop]

        # Seleccionamos los 3 mejores para que pasen directo a la población
        # Antes de hacer crossover y mutacion tenemos que ignorarlos
        e1, e2, e3 = 0, 0, 0  # e1 >= e2 >= e3
        for _ in range(3):
            for j, fitness in enumerate(fitnessList):
                if fitnessList[e1] < fitness:
                    e3 = e2
                    e2 = e1
                    e1 = j
                    continue
                if fitnessList[e2] < fitness:
                    e3 = e2
                    e2 = j
                    continue
                if fitnessList[e3] < fitness:
                    e3 = j
                    continue

        new_pop.append(self.pop[e1])
        new_pop.append(self.pop[e2])
        new_pop.append(self.pop[e3])

        while len(new_pop) < self.pop_size:
            competidores = random.sample(range(self.pop_size), 2)
            mejor = max(competidores, key=lambda idx: fitnessList[idx])
            new_pop.append(self.pop[mejor])

        self.pop = new_pop

    def _crossover(self):
        punto_corte = int(self.horizonte / 3)

        for j in range(3, self.pop_size - 1, 2):
            padre1 = self.pop[j]
            padre2 = self.pop[j + 1]

            # Combine prefix of one with suffix of the other
            hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
            hijo2 = padre2[:punto_corte] + padre1[punto_corte:]

            self.pop[j] = hijo1
            self.pop[j + 1] = hijo2

    def _mutate(self):
        for i in range(3, self.pop_size):
            for j in range(self.horizonte):
                if random.random() < self.tasa_mutacion:
                    prev = self.pop[i][j]
                    self.pop[i][j] = random.choice([e for e in Acciones if e != prev])

    @override
    def color(self):
        return (255, 165, 0)

    @override
    def recalc(self, contexto: Juego):
        pass
