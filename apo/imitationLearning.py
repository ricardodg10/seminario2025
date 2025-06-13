#from utils import funcion_objetivo
#import random
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# cargar un modelo o entrenar uno
def cargar_o_entrenar_modelo(path_csv, path_modelo_pkl):
    if os.path.exists(path_modelo_pkl):
        print("Cargando modelo ya entrenado...")
        modelo = joblib.load(path_modelo_pkl)
    else:
        print("Entrenando modelo desde CSV...")
        df = pd.read_csv(path_csv)
        X = df[["grado"]]
        y = df["etiqueta"]

        modelo = RandomForestClassifier()
        modelo.fit(X, y)

        joblib.dump(modelo, path_modelo_pkl)
        print(f"Modelo entrenado y guardado en: {os.path.abspath(path_modelo_pkl)}")
    return modelo

# predice la solución binaria respecto a los grados de un nodo
def generar_solucion_inicial_il(modelo, grados_por_nodo):
    solucion = []
    for nodo_id in range(len(grados_por_nodo)):
        grado = grados_por_nodo[nodo_id]
        pred = modelo.predict(pd.DataFrame([[grado]], columns=["grado"]))[0]
        solucion.append(int(pred))
    return solucion

'''
def aplicar_imitacion_parcial(candidatos, g_best_bin, p=0.5):

    candidatos_nuevos = []

    for bin_sol, real_sol, _ in candidatos:
        nueva_bin = []

        for i in range(len(bin_sol)):
            if bin_sol[i] != g_best_bin[i]:
                if random.random() < p:
                    nueva_bin.append(g_best_bin[i])
                else:
                    nueva_bin.append(bin_sol[i])
            else:
                nueva_bin.append(bin_sol[i])

        nuevo_fitness = funcion_objetivo(nueva_bin)
        candidatos_nuevos.append((nueva_bin, real_sol, nuevo_fitness))

    return candidatos_nuevos

def aplicar_imitacion_parcial(candidatos, g_best, p=0.3):
    nuevos_candidatos = []
    for binario, real, fitness in candidatos:
        bin_modificado = []
        for i in range(len(binario)):
            if random.random() < p:
                bin_modificado.append(g_best[i])  # copia del experto
            else:
                bin_modificado.append(binario[i])  # deja el original
        nuevos_candidatos.append((bin_modificado, real, fitness))
    return nuevos_candidatos
'''