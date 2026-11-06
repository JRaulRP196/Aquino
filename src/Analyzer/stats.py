import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def estadisticas_descriptivas(df):
    print(" --- ESTADISTICAS DESCRIPTIVAS --- ")
    print(df.describe().round(2))

def matriz_correlacion(df_cleaned):
    ids = df_cleaned.attrs.get("identificadoras", [])
    categoricas = df_cleaned.attrs.get("categoricas", [])
    if ids:
        print("Excluidas de la correlación (identificadores):", ids)
    if categoricas:
        print("Excluidas de la correlación (categóricas, Pearson no aplica):", categoricas)

    numerico = df_cleaned.select_dtypes(include="number").drop(
        columns=ids + categoricas, errors="ignore")
    if numerico.shape[1] < 2:
        print("No hay suficientes columnas numéricas para la matriz de correlación")
        return
    matriz = numerico.corr(method='pearson')
    plt.figure(figsize=(15,15))
    sns.heatmap(matriz, annot=True, fmt=".2f", cmap="coolwarm", linewidths=.5)
    plt.title("Matriz de correlación")
    plt.show()