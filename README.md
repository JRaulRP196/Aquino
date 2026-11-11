# Analizador de Datos

Aplicación de consola (con selector de archivos gráfico) que carga un archivo `.csv` o `.xlsx`, lo limpia, lo prepara y calcula estadísticas y relaciones entre sus variables.

## Instalación y ejecución

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cd src
python app.py
```

> Hay que ejecutar desde `src/` porque los imports son `from Analyzer.loader import ...`.

Archivos de ejemplo en `src/test/` (`winequality-red.csv`, `winequality-white.csv`, `datos_prueba.xlsx`).

## Estructura

```
src/
├── app.py                    # Menú principal y orquestación del flujo
├── Analyzer/
│   ├── loader.py             # Lectura de archivos
│   ├── cleaner.py            # Limpieza y transformación del DataFrame
│   ├── types_detector.py     # Detección de tipos de columnas
│   └── stats.py              # Estadísticas, correlación y eta²
└── test/                     # Datos de prueba
```

## Flujo del programa (`app.py`)

```
leerArchivo → limpieza_general → estadisticas_descriptivas
            → tratamiento_variables → eta2 → matriz_correlacion
```

1. El usuario elige "Analizar archivo" y selecciona el archivo en un diálogo.
2. `leerArchivo(path)` devuelve un `DataFrame`.
3. `limpieza_general(df)` lo limpia.
4. `estadisticas_descriptivas(df)` imprime el resumen (con los datos aún en su escala original).
5. `tratamiento_variables(df)` codifica categóricas y estandariza numéricas.
6. `eta2(df)` y `matriz_correlacion(df)` analizan las relaciones.

## Funciones clave por módulo

### `loader.py` — Lectura

| Función | Qué hace |
|---|---|
| `leerArchivo(ruta)` | Recibe un `Path`; según la extensión (`.csv`/`.xlsx`) delega a la función correcta. Devuelve un `DataFrame`. |
| `leerCSV(path)` | Detecta automáticamente la codificación (chardet) y el separador (`,`, `;`, tab…). |
| `leerExcel(path)` | Lee **todas** las hojas y las concatena en un solo `DataFrame`. |
| `detectarCodificacion(ruta)` | Devuelve la codificación del archivo con `chardet`. |

### `types_detector.py` — Tipos de columnas

Todas reciben un `df` y devuelven una **lista de nombres de columnas**:

| Función | Devuelve |
|---|---|
| `columnas_numericas(df)` | Columnas numéricas. |
| `columnas_textuales(df)` | Columnas de texto. |
| `columnas_fechas(df)` | Columnas datetime. |
| `columnas_identificadoras(df)` | Enteros que parecen ID (nombre `id`/`_id`/`id_` o índice único y creciente). |
| `detectar_tipos_datos(df)` | Imprime los `dtypes`. |

### `cleaner.py` — Limpieza y transformación

Hay dos etapas públicas:

**`limpieza_general(df)`** (antes de las estadísticas descriptivas):
- Normaliza nombres de columnas: minúsculas, sin espacios extremos, espacios → `_`.
- `eliminar_duplicados(df)`: quita filas duplicadas.
- `eliminar_nulos(df)`: trata `""`, `"N/A"`, `"NA"`, `"-"`, `"null"` como nulos y **elimina** esas filas.
- `convertir_fechas(df)`: por cada columna datetime crea `anio_de_X`, `mes_de_X`, `dia_de_X`.
- Guarda en `df.attrs["identificadoras"]` la lista de columnas ID.

**`tratamiento_variables(df)`** (preparación para el análisis):
- `convertir_categoricas(df, max)`: las columnas de texto con ≤ `max` valores distintos (10 por defecto en el flujo) se codifican a enteros con `LabelEncoder`.
- `estandarizacion(df)`: `StandardScaler` (media 0, desv. 1) sobre las numéricas.

### `stats.py` — Análisis

| Función | Qué hace |
|---|---|
| `estadisticas_descriptivas(df)` | Imprime `df.describe()` redondeado a 2 decimales. |
| `matriz_correlacion(df)` | Heatmap de correlación de Pearson. Excluye identificadores y categóricas. |
| `eta2(df)` | Calcula η² (relación categórica → numérica) para cada par. Devuelve la lista de relaciones fuertes (η² > 0.5) como `[(categoria, numerica, valor), ...]`. |
| `relaciones_fuertes(eta2, umbral=0.5)` | Filtra y ordena de mayor a menor los pares sobre el umbral. |

## Metadatos en `df.attrs` (importante para quien use el DataFrame)

El pipeline guarda información en `df.attrs`. Úsenla en vez de volver a detectarla:

| Clave | Contenido | La pone |
|---|---|---|
| `identificadoras` | Columnas ID (no analizar como numéricas). | `limpieza_general` |
| `categoricas` | Columnas de texto ya codificadas a enteros. | `convertir_categoricas` |
| `mapeos` | `{columna: {codigo: etiqueta_original}}` para decodificar. | `convertir_categoricas` |

Ejemplo: para mostrar el nombre original de una categoría, `df.attrs["mapeos"]["columna"][codigo]`.

## Cosas a tener en cuenta

- Los códigos de las categóricas (0, 1, 2…) son **etiquetas arbitrarias, no una escala**. No usarlas en Pearson ni como si fueran números; para eso existe η².
- `eta2(df)` y `matriz_correlacion(df)` requieren haber pasado antes por `limpieza_general` y `tratamiento_variables` (dependen de `df.attrs`). `eta2` lanza `KeyError` si falta `categoricas`.
- Tras `estandarizacion` los valores numéricos están **estandarizados**; si necesitan valores originales (p. ej. para gráficos), usen el DataFrame de después de `limpieza_general`.
- En `app.py`, el resultado de `eta2(df)` hoy **no se usa** (no se imprime ni se guarda): es el punto de enganche para la sección de *insights*.
- Solo se soportan `.csv` y `.xlsx`.
