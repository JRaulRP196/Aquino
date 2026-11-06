import re
import pandas as pd


def detectar_tipos_datos(df):
    print("--- TIPOS DE DATOS DE LAS COLUMNAS ---")
    print(df.dtypes)

def columnas_textuales(df):
    textuales = df.select_dtypes(include="str").columns.tolist()
    return textuales

def columnas_numericas(df):
    numericas = df.select_dtypes(include="number").columns.tolist()
    return numericas

def columnas_fechas(df):
    fechas = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    return fechas

def columnas_identificadoras(df):
    ids = []
    for col in df.select_dtypes(include="integer").columns:
        por_nombre = re.search(r"(^|_)id(_|$)", str(col)) is not None
        es_indice = df[col].is_unique and df[col].is_monotonic_increasing
        if por_nombre or es_indice:
            ids.append(col)
    return ids