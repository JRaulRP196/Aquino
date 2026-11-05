import pandas as pd
import chardet
from Analyzer.cleaner import limpieza_general
from Analyzer.types_detector import detectar_tipos_datos
from Analyzer.stats import estadisticas_descriptivas



def detectarCodificacion(ruta):
    if(not ruta.exists()):
        print("Ruta no existe")
        return
    return chardet.detect(ruta.read_bytes())["encoding"]

def leerArchivo(ruta):
    tipo = ruta.suffix

    match tipo:
        case ".xlsx":
            print(leerExcel(ruta).head())
        case ".csv":
            print(leerCSV(ruta).head())
        case _:
            print("Tipo de archivo desconocido")


def leerCSV(path):
    # sep=None + engine="python" detecta el separador (coma, ;, tab...)
    df = pd.read_csv(path, encoding=detectarCodificacion(path),
                     sep=None, engine="python")
    df = limpieza_general(df)
    detectar_tipos_datos(df)
    estadisticas_descriptivas(df)
    return df

def leerExcel(path):
    hojas = pd.read_excel(path, sheet_name=None)
    df = pd.concat(hojas.values(), ignore_index=True)
    df = limpieza_general(df)
    detectar_tipos_datos(df)
    estadisticas_descriptivas(df)
    return df
