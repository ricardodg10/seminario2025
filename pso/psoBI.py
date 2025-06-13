import time

from core.enjambre import Enjambre
from pso.particulaBI import ParticulaBinaria
from utils import funcion_objetivo

class PSOBinario(Enjambre):

    _instancia = None   # se guarda una única instancia

    def __init__(self, dimension, lower_bound, upper_bound, max_iter, num_particulas, w, c1, c2, aristas):

        # Singleton
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True

        super().__init__(dimension, lower_bound, upper_bound, max_iter, num_particulas)
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.aristas = aristas

        self.mejor_global = None
        self.mejor_valor = None
        self.iteracion_mejor = 0
        self.tiempo_mejor = 0
        self.historial_convergencia = []

    def optimizar(self):
        self.poblacion = [ParticulaBinaria(self.dimension, self.lower_bound, self.upper_bound, self.aristas) for _ in range(self.num_individuos)]

        self.mejor_global = self.poblacion[0].posicion_binaria[:]
        self.mejor_valor = funcion_objetivo(self.mejor_global)
        tiempo_inicio = time.time()

        for t in range(1, self.max_iter + 1):
            for p in self.poblacion:
                valor = p.evaluar()

                if valor < p.mejor_fitness:
                    p.mejor_fitness = valor
                    p.mejor_personal = p.posicion_binaria[:]

                if valor < self.mejor_valor:
                    self.mejor_valor = valor
                    self.mejor_global = p.posicion_binaria[:]
                    self.iteracion_mejor = t
                    self.tiempo_mejor = time.time() - tiempo_inicio

            for p in self.poblacion:
                p.actualizar_velocidad(self.mejor_global, self.w, self.c1, self.c2)
                p.actualizar_posicion()

            self.historial_convergencia.append(self.mejor_valor)
            print(f"Iteración {t} - Vértices cubiertos: {sum(self.mejor_global)}")

        return self.mejor_global, self.mejor_valor, time.time() - tiempo_inicio
