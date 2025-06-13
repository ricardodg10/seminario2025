from utils import funcion_objetivo

class Individuo:
    def __init__(self, dimension, lower_bound, upper_bound):
        self.dimension = dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        self.posicion_real = []
        self.posicion_binaria = []

        self.realPbest = []
        self.binPbest = []
        self.binPbestValor = float('inf')

    # posiciones actuales
    def getPosicionReal(self):
        return self.posicion_real
    
    def setPosicionReal(self, pReal):
        self.posicion_real = pReal

    def getPosicionBinaria(self):
        return self.posicion_binaria
    
    def setPosicionBinaria(self, pBin):
        self.posicion_binaria = pBin
    
    # mejores posiciones
    def getRealPbest(self):
        return self.realPbest

    def setBestReal(self, pReal):
        self.posicion_real = pReal

    def getBinPbest(self):
        return self.binPbest

    def setBestBin(self, pBin):
        self.posicion_binaria = pBin

    # valor binario (cobertura)
    def getValorPbest(self):
        return self.binPbestValor
    
    def setValorPBest(self, pBestValor):
        self.binPbestValor = pBestValor

    # evaluar la posicion actual en la función objetivo
    def evaluar(self):
        return funcion_objetivo(self.getPosicionBinaria())

    # actualizar
    def actualizarActual(self, actualBin, actualReal):
        self.setPosicionBinaria(actualBin)
        self.setPosicionReal(actualReal)

    def actualizarMejorP(self, pBestReal, pBestBin, pBestValorBin):
        self.setBestBin(pBestBin)
        self.setBestReal(pBestReal)


    




