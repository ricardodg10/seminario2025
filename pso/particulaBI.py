from core.individuo import Individuo
import random
import math

from utils import reparar_solucion, binarizar_sigmoide

class ParticulaBinaria(Individuo):
    def __init__(self, dimension, lower_bound, upper_bound, aristas):
        
        super().__init__(dimension, lower_bound, upper_bound)
        self.aristas = aristas

        self.posicion_real = [random.uniform(lower_bound, upper_bound) for _ in range(dimension)]
        self.velocidad = [random.uniform(lower_bound, upper_bound) for _ in range(dimension)]
        self.posicion_binaria = reparar_solucion([binarizar_sigmoide(x) for x in self.posicion_real], self.aristas)

        self.fitness = self.evaluar()
        self.mejor_personal = self.posicion_binaria[:]
        self.mejor_fitness = self.fitness

    def actualizar_velocidad(self, g_best, w, c1, c2):
        for i in range(self.dimension):
            r1 = random.random()
            r2 = random.random()
            cognitiva = c1 * r1 * (self.mejor_personal[i] - self.posicion_binaria[i])
            social = c2 * r2 * (g_best[i] - self.posicion_binaria[i])
            self.velocidad[i] = w * self.velocidad[i] + cognitiva + social

    def actualizar_posicion(self):
        for i in range(self.dimension):
            self.posicion_real[i] += self.velocidad[i]
            self.posicion_real[i] = max(self.lower_bound, min(self.posicion_real[i], self.upper_bound))
        self.posicion_binaria = reparar_solucion([binarizar_sigmoide(x) for x in self.posicion_real], self.aristas)

