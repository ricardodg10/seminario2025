from core.individuo import Individuo
import random
import math

from utils import binarizar_sigmoide

class PuffinBinario(Individuo):
    def __init__(self, dimension, LB, UB):
        super().__init__(dimension, LB, UB)

        self.setPosicionReal([random.uniform(LB, UB) for _ in range(dimension)])
        self.setPosicionBinaria([binarizar_sigmoide(v) for v in self.posicion_real])

        self.setBestReal(self.getPosicionReal())
        self.setBestBin(self.getPosicionBinaria())

        self.valor = float('inf')

    def evadir_aire(self, X_r, L, R):
        return [x_i + (x_i - x_r) * l + R for x_i, x_r, l in zip(self.posicion_real, X_r, L)]

    def dep_picada(self, Y, S):
        return [y * S for y in Y]

    def recoleccion(self, X2, X3, F, L1=None):
        if L1:
            return [x1 + F * l1 * (x2 - x3) for x1, x2, x3, l1 in zip(self.posicion_real, X2, X3, L1)]
        else:
            return [x1 + F * (x2 - x3) for x1, x2, x3 in zip(self.posicion_real, X2, X3)]

    def intensificar(self, W, f):
        return [w * (1 + f) for w in W]

    def evadir_agua(self, X_r1, X_r2, L=None, beta=None, F=0.5):
        if L:
            return [x1 + F * l * (x1 - x2) for x1, x2, l in zip(X_r1, X_r2, L)]
        else:
            return [x1 + beta * (x1 - x2) for x1, x2 in zip(X_r1, X_r2)]
