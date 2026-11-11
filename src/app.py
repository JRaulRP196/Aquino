from tkinter import Tk, filedialog
from pathlib import Path
from Analyzer.loader import leerArchivo
from Analyzer.cleaner import limpieza_general, tratamiento_variables
from Analyzer.stats import estadisticas_descriptivas, matriz_correlacion, eta2

while True:
    menu = """
    ---- OPCIONES ----
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
                if(ruta != "") : 
                    path= Path(ruta)

                    #Tratamiento de Dataframe
                    df = leerArchivo(path)
                    df = limpieza_general(df)
                    print(df)
                    estadisticas_descriptivas(df)

                    #Análisis
                    df = tratamiento_variables(df)
                    eta2(df)
                    matriz_correlacion(df)


            case 2:
                break


    except ValueError:

        print("La opción solo acepta números")


