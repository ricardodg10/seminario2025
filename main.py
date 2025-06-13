import matplotlib.pyplot as plt

from pso.psoBI import PSOBinario
from apo.apoBI import APOBinario
from ga.gaBI import GABinario

from utils import funcion_objetivo, leer_vertices, leer_aristas, guardar_convergencia_ejecucion, guardar_resultados

if __name__ == "__main__":

    # elección de benchmark y algoritmmo
    benchmark_var = 3 # 1: C125-9; 2: keller4; 3: keller5
    usar = 3 # 1: pso; 2: ga; 3: apo

    # para utilizar Imitation Learning (solo se usa son APO: usar = 3)
    imitation = True

    if benchmark_var == 1:
        ruta_mtx = "C:/Users/ricar/OneDrive/Escritorio/seminario/benchmark/C125-9.mtx"
    elif benchmark_var == 2:
        ruta_mtx = "C:/Users/ricar/OneDrive/Escritorio/seminario/benchmark/keller4.mtx"
    else:
        ruta_mtx = "C:/Users/ricar/OneDrive/Escritorio/seminario/benchmark/keller5.mtx"

    num_vertices = leer_vertices(ruta_mtx)
    aristas = leer_aristas(ruta_mtx)

    # parámetros en común
    dimension = num_vertices
    lower_bound = 0
    upper_bound = 1
    max_iter = 100
    num_individuos = 10

    # pso
    if usar == 1:
        pso = PSOBinario(
            dimension=dimension,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            max_iter=max_iter,
            num_particulas=num_individuos,
            w=0.5,
            c1=2,
            c2=2,
            aristas=aristas
            
        )
        mejor_sol, mejor_valor, tiempo = pso.optimizar()
        seleccionados = [i + 1 for i, v in enumerate(mejor_sol) if v == 1]
        iteracion_mejor = pso.iteracion_mejor
        tiempo_mejor = pso.tiempo_mejor
        convergencia = pso.historial_convergencia
        algoritmo="pso"

        #guardar nodos seleccionados CAMBIAR NOMBRE DE LA RUTA PARA EL BENCHMARK
        #guardar_nodos(seleccionados, "C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/pso/paraILKELLER5.txt")

        #para guardar el historial (grafico de convergencia)
        #guardar_convergencia_ejecucion(convergencia, "C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/pso/convEjecKELLER5.txt")

        #guardar 30 ejecuciones
        #guardar_resultados("C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/pso/ejecucionesK5.txt", mejor_valor, tiempo_mejor, tiempo)

    # ga
    elif usar == 2:
        ga = GABinario(
            funcion_objetivo=funcion_objetivo,
            dimension=dimension,
            max_iter=max_iter,
            tamanio_poblacion=num_individuos,
            prob_cruce=0.8,
            prob_mutacion=0.3,
            aristas=aristas
        )
        mejor_sol, mejor_valor, tiempo = ga.optimizar()
        seleccionados = [i + 1 for i, v in enumerate(mejor_sol) if v == 1]
        iteracion_mejor = ga.iteracion_mejor
        tiempo_mejor = ga.tiempo_mejor
        convergencia = ga.historial_convergencia
        algoritmo = "ga"

        #para guardar el historial (grafico de convergencia)
        #guardar_convergencia_ejecucion(convergencia, "C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/ga/convEjecKELLER5.txt")

        #guardar 30 ejecuciones
        #guardar_resultados("C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/ga/ejecucionesK5.txt", mejor_valor, tiempo_mejor, tiempo)

    
    # apo
    else:
        apo = APOBinario.get_instance(
            dimension=dimension,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            max_iter=max_iter,
            num_puffins=num_individuos,
            aristas=aristas,
            betha_levy=1.5,                     # controla qué tan grandes son los pasos aleatorios (literatura: 1.5 → equilibra exploración y explotación)
            F=0.5,                              # factor cooperativo (literatura: 0.5)
            imitation = imitation
        )
        mejor_sol, mejor_valor, tiempo = apo.optimizar()
        seleccionados = [i + 1 for i, v in enumerate(mejor_sol) if v == 1]
        iteracion_mejor = apo.iteracion_mejor
        tiempo_mejor = apo.tiempo_mejor
        convergencia = apo.historial_convergencia
        if(apo.imitation==True):
            algoritmo = "apo+il"
            #para guardar el historial (grafico de convergencia)
            guardar_convergencia_ejecucion(convergencia, "C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo-il/convEjecKELLER5.txt")

            #guardar 30 ejecuciones
            #guardar_resultados("C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo-il/ejecucionesKELLER5.txt", mejor_valor, tiempo_mejor, tiempo)

        else:
            algoritmo = "apo"

            #para guardar el historial (grafico de convergencia)
            #guardar_convergencia_ejecucion(convergencia, "C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo/convEjecKELLER5.txt")

            #guardar 30 ejecuciones
            #guardar_resultados("C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo/ejecucionesK5.txt", mejor_valor, tiempo_mejor, tiempo)


    # resultados en pantalla
    print("\nMejor solución encontrada:", mejor_sol)
    print("Vértices seleccionados:", seleccionados)
    print("Cobertura de vértices:", mejor_valor)
    print(f"\nMejor encontrada en iteración {iteracion_mejor}, tiempo parcial: {tiempo_mejor:.4f} s")
    print("Tiempo total:", tiempo, "[s]")

    
    '''
    #gráfica de convergencia (ejecución actual)
    plt.plot(range(1, max_iter + 1), convergencia)
    plt.title(f'Convergencia del algoritmo {algoritmo.upper()}')
    plt.xlabel('Iteraciones')
    plt.ylabel('Valor de la función objetivo')
    plt.grid(True)
    plt.show()
    '''
    
