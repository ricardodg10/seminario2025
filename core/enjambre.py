from abc import ABC, abstractmethod

class Enjambre(ABC):
    def __init__(self, dimension, lower_bound, upper_bound, max_iter, num_individuos):
        self.dimension = dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_iter = max_iter
        self.num_individuos = num_individuos
        self.poblacion = []

    @abstractmethod
    def optimizar(self):
        pass
