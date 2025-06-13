import random
import time
from ga.cromosoma import Cromosoma

from utils import seleccion_ruleta, reparar_solucion, funcion_objetivo

class GABinario:
    def __init__(self, funcion_objetivo, dimension, max_iter, tamanio_poblacion, prob_cruce, prob_mutacion, aristas):
        self.funcion_objetivo = funcion_objetivo
        self.dimension = dimension
        self.max_iter = max_iter
        self.tamanio_poblacion = tamanio_poblacion
        self.prob_cruce = prob_cruce
        self.prob_mutacion = prob_mutacion
        self.aristas = aristas
        self.poblacion = []

        self.mejor_individuo = None
        self.mejor_valor = float('inf')
        self.iteracion_mejor = None
        self.tiempo_mejor = None
        self.historial_convergencia = []

    def inicializar_poblacion(self):
        self.poblacion = []
        for _ in range(self.tamanio_poblacion):
            individuo = Cromosoma(self.dimension)

            individuo.genotipo = reparar_solucion(individuo.genotipo, self.aristas)

            individuo.fitness = funcion_objetivo(individuo.genotipo)
            self.poblacion.append(individuo)

    def cruzar(self, padre1, padre2):
        punto = random.randint(1, self.dimension - 1)
        hijo1 = Cromosoma(self.dimension)
        hijo2 = Cromosoma(self.dimension)
        hijo1.genotipo = padre1.genotipo[:punto] + padre2.genotipo[punto:]
        hijo2.genotipo = padre2.genotipo[:punto] + padre1.genotipo[punto:]
        return hijo1, hijo2

    def mutar(self, individuo):
        i1, i2 = random.sample(range(self.dimension), 2)
        individuo.genotipo[i1] ^= 1
        individuo.genotipo[i2] ^= 1

    def optimizar(self):
        print("\nEjecución GA\n")
        self.inicializar_poblacion()
        self.mejor_individuo = min(self.poblacion, key=lambda ind: ind.fitness)
        tiempo_inicio = time.time()

        for t in range(1, self.max_iter + 1):
            nueva_poblacion = []

            while len(nueva_poblacion) < self.tamanio_poblacion:
                p1, p2 = seleccion_ruleta(self.poblacion)
                if random.random() < self.prob_cruce:
                    h1, h2 = self.cruzar(p1, p2)
                    nueva_poblacion.extend([h1, h2])
                else:
                    nueva_poblacion.extend([p1, p2])

            nueva_poblacion = nueva_poblacion[:self.tamanio_poblacion]

            for ind in nueva_poblacion:
                if random.random() < self.prob_mutacion:
                    self.mutar(ind)
                ind.genotipo = reparar_solucion(ind.genotipo, self.aristas)
                ind.fitness = funcion_objetivo(ind.genotipo)

            self.poblacion = nueva_poblacion
            mejor_generacion = min(self.poblacion, key=lambda ind: ind.fitness)

            if mejor_generacion.fitness < self.mejor_valor:
                self.mejor_individuo = mejor_generacion
                self.mejor_valor = mejor_generacion.fitness
                self.iteracion_mejor = t
                self.tiempo_mejor = time.time() - tiempo_inicio

            self.historial_convergencia.append(self.mejor_valor)
            print(f"Iteración {t} - Vértices cubiertos: {self.mejor_valor}")

        return self.mejor_individuo.genotipo, self.mejor_valor, time.time() - tiempo_inicio
