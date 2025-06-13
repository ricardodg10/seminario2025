import random
import math
import time

from core.enjambre import Enjambre
from apo.puffinBI import PuffinBinario
from utils import binarizar_sigmoide, reparar_solucion, funcion_objetivo

from apo.imitationLearning import cargar_o_entrenar_modelo, generar_solucion_inicial_il
from utils import calcular_grados 


class APOBinario(Enjambre):

    _instancia = None   # se guarda una única instancia

    def __init__(self, dimension, lower_bound, upper_bound, max_iter, num_puffins, aristas, betha_levy, F, imitation):

        # Singleton
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True

        super().__init__(dimension, lower_bound, upper_bound, max_iter, num_puffins)
        self.g_best_binario = [0] * dimension
        self.g_best_real = [0] * dimension

        self.aristas = aristas
        self.betha_levy = betha_levy
        self.F = F
        self.imitation = imitation

        self.mejor_valor = float('inf')
        self.iteracion_mejor = 0.0
        self.tiempo_mejor = 0.0
        self.historial_convergencia = []

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = cls(*args, **kwargs)
        return cls._instancia
    
    def levy_flight(self):
        beta = self.betha_levy
        sigma_u = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) /
                (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        sigma_v = 1
        U = [random.gauss(0, sigma_u) for _ in range(self.dimension)]
        V = [random.gauss(0, sigma_v) for _ in range(self.dimension)]
        
        return [u / abs(v)**(1 / beta) for u, v in zip(U, V)]

    def optimizar(self):
        
        modelo_il = None
        grados = None

        nombre_benchmark = "Keller5" #cambiar nombre para cargar o entrenar un modelo
        if self.imitation:
            modelo_il = cargar_o_entrenar_modelo(
                path_csv= f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/pso/paraIL/dataset{nombre_benchmark}.csv",
                path_modelo_pkl=f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/modelos/modelo_il_pso_{nombre_benchmark}.pkl"
            )
            grados = calcular_grados(self.aristas, self.dimension)

        self.poblacion = []
        for _ in range(self.num_individuos):
            puffin = PuffinBinario(self.dimension, self.lower_bound, self.upper_bound)

            if self.imitation and modelo_il and grados:
                solucion_il = generar_solucion_inicial_il(modelo_il, grados)
                solucion_il = reparar_solucion(solucion_il, self.aristas)
                puffin.setPosicionBinaria(solucion_il)

            self.poblacion.append(puffin)

        tiempo_inicio = time.time()

        for t in range(1, self.max_iter + 1):
            B = 2 * math.log(1 / random.random()) * (1 - (t / self.max_iter))
            C = 0.5
            candidatos = []

            if B > C:
                for i, puffin in enumerate(self.poblacion):
                    r = random.choice([j for j in range(self.num_individuos) if j != i])
                    X_r = self.poblacion[r].posicion_real
                    L = self.levy_flight()
                    alpha = random.gauss(0, 1)
                    R = round(0.5 * (0.5 + random.random()) * alpha)

                    Y = puffin.evadir_aire(X_r, L, R)
                    S = math.tan((random.random() - 0.5) * math.pi)
                    Z = puffin.dep_picada(Y, S)

                    Y_bin = reparar_solucion([binarizar_sigmoide(y) for y in Y], self.aristas)
                    Z_bin = reparar_solucion([binarizar_sigmoide(z) for z in Z], self.aristas)

                    candidatos += [(Y_bin, Y, funcion_objetivo(Y_bin)),
                                   (Z_bin, Z, funcion_objetivo(Z_bin))]

            else:
                for i in range(self.num_individuos):
                    r2, r3 = random.sample([j for j in range(self.num_individuos) if j != i], 2)
                    X_r2 = self.poblacion[r2].posicion_real
                    X_r3 = self.poblacion[r3].posicion_real

                    if random.random() >= 0.5:
                        L1 = self.levy_flight()
                        W = self.poblacion[i].recoleccion(X_r2, X_r3, self.F, L1)
                    else:
                        W = self.poblacion[i].recoleccion(X_r2, X_r3, self.F)

                    f = 0.1 * (random.random() - 1) * (1 - (t / self.max_iter))
                    Y = self.poblacion[i].intensificar(W, f)

                    r4, r5 = random.sample([j for j in range(self.num_individuos) if j != i], 2)
                    X_r4, X_r5 = self.poblacion[r4].posicion_real, self.poblacion[r5].posicion_real

                    if random.random() >= 0.5:
                        L2 = self.levy_flight()
                        Z = self.poblacion[i].evadir_agua(X_r4, X_r5, L=L2)
                    else:
                        beta = random.uniform(0, 1)
                        Z = self.poblacion[i].evadir_agua(X_r4, X_r5, beta=beta)

                    W_bin = reparar_solucion([binarizar_sigmoide(w) for w in W], self.aristas)
                    Y_bin = reparar_solucion([binarizar_sigmoide(y) for y in Y], self.aristas)
                    Z_bin = reparar_solucion([binarizar_sigmoide(z) for z in Z], self.aristas)

                    candidatos += [
                        (W_bin, W, funcion_objetivo(W)),
                        (Y_bin, Y, funcion_objetivo(Y)),
                        (Z_bin, Z, funcion_objetivo(Z))
                    ]

            '''if self.imitation and t != 1:
                candidatos = aplicar_imitacion_parcial(candidatos, self.g_best_binario, p=0.3)

            if(self.imitation == True and t !=1):
                candidatos = aplicar_imitacion_parcial(candidatos, self.g_best_binario, p=0.5)
            #print(candidatos)'''

            candidatos.sort(key=lambda x: x[2])
            for i in range(self.num_individuos):
                self.poblacion[i].setPosicionBinaria(candidatos[i][0])
                self.poblacion[i].setPosicionReal(candidatos[i][1])


            for puffin in self.poblacion:

                valor = puffin.evaluar()

                if valor < self.mejor_valor:
                    self.mejor_valor = valor
                    self.g_best_binario = puffin.posicion_binaria[:]
                    self.g_best_real = puffin.posicion_real[:]
                    self.iteracion_mejor = t
                    self.tiempo_mejor = time.time() - tiempo_inicio

            self.historial_convergencia.append(self.mejor_valor)
            print(f"Iteración {t} - Vértices cubiertos: {sum(self.g_best_binario)}")

        return self.g_best_binario, self.mejor_valor, time.time() - tiempo_inicio
