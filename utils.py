import random
import math
import pandas as pd

# funciones para extraer datos de los benchmarks
def leer_vertices(path):
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('%') or line.startswith('%%'):
                continue
            try:
                n, _, _ = map(int, line.strip().split())
                return n
            except ValueError:
                continue

def leer_aristas(path):
    aristas = []
    started = False
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('%') or line.startswith('%%'):
                continue
            elif not started:
                started = True
                continue
            else:
                v1, v2 = map(int, line.strip().split())
                aristas.append((v1, v2))
    return aristas

# calcular grados de los vértices
def calcular_grados(aristas, num_vertices):

    grados = {i: 0 for i in range(num_vertices)} 

    for u, v in aristas:
        grados[u - 1] += 1  
        grados[v - 1] += 1

    return grados

# para escribir en .txt
def guardar_convergencia_ejecucion(array_convergencia, ruta):
    with open(ruta, "w") as file:
        for valor in array_convergencia:
            file.write(f"{valor}\n")

def guardar_resultados(ruta, mejor_sol, tiempo_fitness, tiempo_ejecucion):
    with open(ruta, "a") as file:
        file.write(f'{mejor_sol} - {tiempo_fitness:.4f} - {tiempo_ejecucion:.4f}\n')


# función objetivo
def funcion_objetivo(solucion):
    return sum(solucion)  # se asume que la solución ya fue reparada

# reparación de solución para que sean factibles
def reparar_solucion(solucion, aristas):
    for v1, v2 in aristas:
        if solucion[v1 - 1] == 0 and solucion[v2 - 1] == 0:
            solucion[random.choice([v1 - 1, v2 - 1])] = 1
    return solucion

# sigmoide y binarización
def s1(x):

    a = 1
    try:
        return 1 / (1 + math.exp(-a*x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def binarizar_sigmoide(x):
    return 1 if random.random() <= s1(x) else 0

# para GA
def seleccion_ruleta(poblacion):
    total = sum(1.0 / cromosoma.fitness for cromosoma in poblacion)
    probabilidades = [(1.0 / cromosoma.fitness) / total for cromosoma in poblacion]
    return random.choices(poblacion, weights=probabilidades, k=2)
