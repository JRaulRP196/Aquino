import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from Analyzer.types_detector import columnas_textuales, columnas_numericas, columnas_identificadoras, columnas_fechas

def limpieza_general(df):
    #Limpiamos nombres de columnas
    df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_"))
    
    df = eliminar_duplicados(df)
    df = eliminar_nulos(df)
    df = convertir_fechas(df)
    df.attrs["identificadoras"] = columnas_identificadoras(df)
    return df

def tratamiento_variables(df):
    df = convertir_categoricas(df, 10)
    df = estandarizacion(df)
    return df

def eliminar_nulos(df):
    df = df.replace(r"^\s*$", np.nan, regex=True)# vacíos y espacios
    df = df.replace(["N/A", "NA", "-", "null"], np.nan)
    print("Filas con nulos a eliminar: ", df.isna().any(axis=1).sum())

    df = df.dropna()
    return df

def eliminar_duplicados(df):
    df.duplicated().sum()
    df = df.drop_duplicates()
    return df

def convertir_fechas(df):
    fechas = columnas_fechas(df)
    for col in fechas:
        df[f"anio_de_{col}"] = df[col].dt.year
        df[f"mes_de_{col}"] = df[col].dt.month
        df[f"dia_de_{col}"] = df[col].dt.day
    return df

def convertir_categoricas(df, cant_categorias_maximas):
    columnas_str = columnas_textuales(df)
    le = LabelEncoder()
    codificadas = []
    mapeos = {}
    for columna in columnas_str:
        if(df[columna].nunique() <= cant_categorias_maximas):
            df[columna] = df[columna].astype("category")
            df[columna] = le.fit_transform(df[columna])
            mapeos[columna] = dict(enumerate(le.classes_))
            codificadas.append(columna)
    # Los códigos 0,1,2... son etiquetas arbitrarias, no una escala: se
    # registran para no tratarlas como numéricas en correlaciones de Pearson
    df.attrs["categoricas"] = codificadas
    df.attrs["mapeos"] = mapeos
    return df

def estandarizacion(df):
    scaler = StandardScaler()
    col_numericas = columnas_numericas(df)
    df[col_numericas] = scaler.fit_transform(df[col_numericas])
    return df
