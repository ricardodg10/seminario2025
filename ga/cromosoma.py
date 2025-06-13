import random

class Cromosoma:
    def __init__(self, dimension):
        self.dimension = dimension
        self.genotipo = [random.randint(0, 1) for _ in range(dimension)]
        self.fitness = None

