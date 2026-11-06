import pandas as pd
import chardet


def leerArchivo(ruta):
    tipo = ruta.suffix

    match tipo:
        case ".xlsx":
            return leerExcel(ruta)
        case ".csv":
            return leerCSV(ruta)
        case _:
            print("Tipo de archivo desconocido")



def detectarCodificacion(ruta):
    if(not ruta.exists()):
        print("Ruta no existe")
        return
    return chardet.detect(ruta.read_bytes())["encoding"]


def leerCSV(path):
    # sep=None + engine="python" detecta el separador (coma, ;, tab...)
    df = pd.read_csv(path, encoding=detectarCodificacion(path),
                     sep=None, engine="python")
    return df


def leerExcel(path):
    hojas = pd.read_excel(path, sheet_name=None)
    df = pd.concat(hojas.values(), ignore_index=True)
    return df

