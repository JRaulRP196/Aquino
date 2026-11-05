from tkinter import Tk, filedialog
from pathlib import Path
from Analyzer.loader import leerArchivo


while True:
    menu = """
    ---- OPCIONES ----REcuer
    1. Análizar Archivo
    2. Salir
    DIGITA UNA OPCIÓN VÁLIDA: """
    try:
        opt = int(input(menu))
        match opt:
            case 1:
                Tk().withdraw()
                ruta = filedialog.askopenfilename(
                    title="Elegí un archivo",
                    filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx")]
                )
                path= Path(ruta)
                leerArchivo(path)
            case 2:
                break
    except ValueError:
        print("La opción solo acepta números")


