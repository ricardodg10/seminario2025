import pandas as pd
import matplotlib.pyplot as plt
import os

# DESCRIBE LOS DATOS

def describir_resultados_txt(path_txt, nombre_algoritmo):
    fitness = []
    tiempos_parciales = []
    tiempos_totales = []

    with open(path_txt, 'r') as file:
        for line in file:
            if line.startswith('%'):
                continue
            partes = line.strip().split('-')
            if len(partes) != 3:
                continue
            try:
                fit = int(partes[0].strip())
                t_parcial = float(partes[1].strip())
                t_total = float(partes[2].strip())

                fitness.append(fit)
                tiempos_parciales.append(t_parcial)
                tiempos_totales.append(t_total)
            except ValueError:
                continue

    def resumen_descriptivo(datos):
        serie = pd.Series(datos)
        q1 = serie.quantile(0.25)
        q2 = serie.quantile(0.50)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1
        return {
            "Promedio": round(serie.mean(), 2),
            "Mínimo": serie.min(),
            "Q1 (25%)": q1,
            "Q2 (50%)": q2,
            "Q3 (75%)": q3,
            "Máximo": serie.max(),
            "Desviación Estándar": round(serie.std(), 2),
            "IQR": iqr
        }

    resumen_fitness = resumen_descriptivo(fitness)
    resumen_parcial = resumen_descriptivo(tiempos_parciales)
    resumen_total = resumen_descriptivo(tiempos_totales)

    df_fitness = pd.DataFrame([resumen_fitness], index=[f"{nombre_algoritmo} - Fitness"])
    df_parcial = pd.DataFrame([resumen_parcial], index=[f"{nombre_algoritmo} - Tiempo Parcial"])
    df_total = pd.DataFrame([resumen_total], index=[f"{nombre_algoritmo} - Tiempo Total"])

    return pd.concat([df_fitness, df_parcial, df_total])

# GRAFICA LAS CONVERGENCIAS
def graficar_convergencia_multiple(paths_dict, benchmark="Benchmark", ruta_guardado=None):
    """
    paths_dict: {'PSO': path1, 'GA': path2, 'APO': path3, ...}
    """
    # Estilos por algoritmo (color + línea)
    estilos = {
        "PSO": {"color": "blue", "linestyle": "-", "label": "PSO"},
        "GA": {"color": "green", "linestyle": "--", "label": "GA"},
        "APO": {"color": "red", "linestyle": "-.", "label": "APO"},
        "APO+IL": {"color": "purple", "linestyle": ":", "label": "APO+IL"}
    }

    plt.figure(figsize=(9, 6))

    for nombre, path in paths_dict.items():
        datos = []
        with open(path, 'r') as file:
            for linea in file:
                if linea.startswith('%'):
                    continue
                try:
                    valor = int(linea.strip())
                    datos.append(valor)
                except ValueError:
                    continue

        estilo = estilos.get(nombre, {"color": "black", "linestyle": "-", "label": nombre})
        plt.plot(range(1, len(datos) + 1), datos,
                 color=estilo["color"],
                 linestyle=estilo["linestyle"],
                 linewidth=2,
                 label=estilo["label"])

    plt.xlabel("Iteraciones")
    plt.ylabel("Fitness")
    plt.title(f"Convergencia de los Algoritmos en el Benchmark {benchmark}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Guardar si se especificó la ruta
    if ruta_guardado:
        plt.savefig(ruta_guardado, dpi=300)
        print(f"[✅] Imagen guardada en: {ruta_guardado}")

    plt.show()

def graficar_boxplots_resultados(archivos_dict, benchmark="Benchmark",
                                  ruta_fitness=None,
                                  ruta_parcial=None,
                                  ruta_total=None):

    fitness_dict = {}
    tiempo_parcial_dict = {}
    tiempo_total_dict = {}

    for nombre_algoritmo, path in archivos_dict.items():
        fitness_list = []
        parcial_list = []
        total_list = []

        with open(path, 'r') as f:
            for linea in f:
                if linea.startswith('%'):
                    continue
                try:
                    partes = linea.strip().split('-')
                    if len(partes) != 3:
                        continue
                    fit = int(partes[0].strip())
                    t_parcial = float(partes[1].strip())
                    t_total = float(partes[2].strip())

                    fitness_list.append(fit)
                    parcial_list.append(t_parcial)
                    total_list.append(t_total)
                except ValueError:
                    continue

        fitness_dict[nombre_algoritmo] = fitness_list
        tiempo_parcial_dict[nombre_algoritmo] = parcial_list
        tiempo_total_dict[nombre_algoritmo] = total_list

    # === BOXPLOT FITNESS ===
    plt.figure(figsize=(10, 5))
    plt.boxplot([fitness_dict[k] for k in fitness_dict], labels=fitness_dict.keys())
    plt.title(f"Distribución del Fitness encontrado [{benchmark}]")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.tight_layout()
    if ruta_fitness:
        plt.savefig(ruta_fitness, dpi=300)
        print(f"[✅] Gráfico guardado en: {ruta_fitness}")
    plt.show()

    # === BOXPLOT TIEMPO PARCIAL ===
    plt.figure(figsize=(10, 5))
    plt.boxplot([tiempo_parcial_dict[k] for k in tiempo_parcial_dict], labels=tiempo_parcial_dict.keys())
    plt.title(f"Distribución del Tiempo para encontrar el Fitness [{benchmark}]")
    plt.ylabel("Tiempo (s)")
    plt.grid(True)
    plt.tight_layout()
    if ruta_parcial:
        plt.savefig(ruta_parcial, dpi=300)
        print(f"[✅] Gráfico guardado en: {ruta_parcial}")
    plt.show()

    # === BOXPLOT TIEMPO TOTAL ===
    plt.figure(figsize=(10, 5))
    plt.boxplot([tiempo_total_dict[k] for k in tiempo_total_dict], labels=tiempo_total_dict.keys())
    plt.title(f"Distribución del Tiempo total de ejecución del algoritmo [{benchmark}]")
    plt.ylabel("Tiempo (s)")
    plt.grid(True)
    plt.tight_layout()
    if ruta_total:
        plt.savefig(ruta_total, dpi=300)
        print(f"[✅] Gráfico guardado en: {ruta_total}")
    plt.show()

if __name__ =="__main__":

    mostrar = 1 # 1: describe; 2: grafico convergencia; 3: boxplots

    if(mostrar==1):
        name =  "KELLER5"
        alg = ["pso", "ga", "apo", "apo-il"]

        for algoritmo in alg:
            tabla = describir_resultados_txt(f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/{algoritmo}/ejecuciones{name}.txt", nombre_algoritmo=algoritmo.upper())
            print(tabla)
    elif(mostrar==2):

        benchmark = "KELLER5" #path
        name = "keller5"
        graficar_convergencia_multiple({
            "PSO": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/pso/convEjec{benchmark}.txt",
            "GA": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/ga/convEjec{benchmark}.txt",
            "APO": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo/convEjec{benchmark}.txt",
            "APO+IL": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo-il/convEjec{benchmark}.txt"
        }, benchmark=name, 
        ruta_guardado=f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/convergencia_{benchmark}.png")
    else:
        benchmark = "KELLER5" #path
        name = "keller5"
        graficar_boxplots_resultados({
            "PSO": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/pso/ejecuciones{benchmark}.txt",
            "GA": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/ga/ejecuciones{benchmark}.txt",
            "APO": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo/ejecuciones{benchmark}.txt",
            "APO+IL": f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/apo-il/ejecuciones{benchmark}.txt"
        }, benchmark=name,
        ruta_fitness=f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/boxplotFitness_{benchmark}.png",
        ruta_parcial=f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/boxplotTfitness_{benchmark}.png",
        ruta_total=f"C:/Users/ricar/OneDrive/Escritorio/algBINARIOS/resultados/boxplotTtotal_{benchmark}.png")