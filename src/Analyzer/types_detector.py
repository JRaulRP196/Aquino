import pandas as pd


def detectar_tipos_datos(df):
    print("--- TIPOS DE DATOS DE LAS COLUMNAS ---")
    print(df.dtypes)

def columnas_textuales(df):
    textuales = df.select_dtypes(include="str").columns.tolist()
    return textuales
