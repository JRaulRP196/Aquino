import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Analyzer.types_detector import columnas_numericas



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
    plt.figure(figsize=(10,10))
    sns.heatmap(matriz, annot=True, fmt=".2f", cmap="coolwarm", linewidths=.5)
    plt.title("Matriz de correlación")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0) 
    plt.tight_layout()                    
    plt.show()

def eta2(df): #Usemosla para los insghts
    col_grupos = df.attrs["categoricas"]
    if len(col_grupos) < 1 : 
        print("No hay variables categoricas definidas para hacer un analisis de relacion de las mismas")
        return
    col_datos = [c for c in columnas_numericas(df) if c not in col_grupos]

    media_total = df[col_datos].mean()


    ss_total = ((df[col_datos]-media_total)**2).sum()
    resultados = {}
    for g in col_grupos:
        gb = df.groupby(g)[col_datos]
        ss_grupo = (gb.count() * (gb.mean() - media_total) ** 2).sum()
        resultados[g] = ss_grupo / ss_total

    eta2 = pd.DataFrame(resultados).T
    return relaciones_fuertes(eta2)

def relaciones_fuertes(eta2, umbral=0.5):
    """Devuelve (categoria, numerica, eta2) para los valores > umbral."""
    pares = eta2.stack()                  # Serie con índice (categoria, numerica)
    pares = pares[pares > umbral].sort_values(ascending=False)

    return [(cat, num, valor) for (cat, num), valor in pares.items()]