import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import os

    import numpy as np
    import pandas as pd
    import plotly.express as px
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    return KMeans, StandardScaler, np, os, pd, px


@app.cell
def _(os, urllib, zipfile):
    url = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"
    zip_path = "household_power_consumption.zip"
    txt_filename = "household_power_consumption.txt"

    # Descarga el dataset en caso de que no se encuentre en la carpeta
    if not os.path.exists(txt_filename):
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove(zip_path)
    return (txt_filename,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Descripción del Dataset: Individual Household Electric Power Consumption

    El conjunto de datos utilizado para este análisis proviene del **Repositorio de Aprendizaje Automático de la UCI (Machine Learning Repository)**. Contiene mediciones del consumo de energía eléctrica en un único hogar ubicado en Sceaux (Francia) con una tasa de muestreo de un minuto, abarcando un periodo histórico entre diciembre de 2006 y noviembre de 2010 (aproximadamente 47 meses).

    ### Resumen del Dataset

    * **Instancias Totales:** 2,075,259 mediciones registradas.
    * **Datos Faltantes:** Aproximadamente el 1.25% de las filas contienen valores nulos, los cuales corresponden a periodos donde el suministro o el sistema de medición local sufrieron caídas.
    * **Naturaleza del Análisis:** Al aplicar algoritmos de agrupamiento como $K$-Means sobre variables cuantitativas continuas, el objetivo primordial no es descubrir perfiles comunes de consumo, sino modelar la estructura normal de los datos para aislar los elementos menos parecidos al resto (*outliers*).

    ---

    ### Diccionario de Variables Seleccionadas

    Para cumplir con la detección de anomalías contextuales, el dataset se divide analíticamente en variables de comportamiento y variables de entorno o contexto:

    | Nombre de la Variable | Tipo de Dato | Rol Analítico | Descripción Técnica |
    | :--- | :--- | :--- | :--- |
    | **`Global_active_power`** | Cuantitativa Continua | Variable de Comportamiento | Potencia activa global consumida por el hogar (en kilovatios, kW). Representa la energía útil total demandada por los electrodomésticos activos en la vivienda. |
    | **`Voltage`** | Cuantitativa Continua | Variable Contextual | Voltaje promedio medido en la red eléctrica del hogar (en voltios, V). Funciona como el contexto de entorno. |
    """)
    return


@app.cell
def _(pd, txt_filename):
    # Cargar el dataset, limpieza y escalamiento
    df = pd.read_csv(txt_filename, sep=";", nrows=10000, low_memory=False)
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Escalamiento

    La potencia maneja magnitudes pequeñas (típicamente entre $0.1$ y $9$ kW), mientras que el voltaje oscila en rangos de magnitud mayores (alrededor de los $230$ a $250$ V). Si no se normalizan, la variable de voltaje dominará por completo el cálculo de la distancia euclidiana, anulando el impacto de la potencia en los clústeres.
    """)
    return


@app.cell
def _(StandardScaler, df, np):
    # Limpieza y escalamiento
    df_limpio = (
        df[["Global_active_power", "Voltage"]]
        .replace("?", np.nan)
        .dropna()
        .astype(float)
    )
    scaler = StandardScaler()

    df_scaled = scaler.fit_transform(df_limpio)
    return df_limpio, df_scaled


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Definición de Anomalías bajo esta Estructura

       **Atípicos Globales:** Registros donde la potencia útil (`Global_active_power`) alcanza magnitudes masivas, independientemente de las fluctuaciones del suministro eléctrico corporativo.

       **Atípicos Contextuales:** Registros donde un consumo ordinario (ej. $1.5$ kW) se combina de manera inusual con una caída severa de tensión en la red del vecindario (`Voltage` $< 233$ V), provocando que el registro se aleje críticamente del centro de masa de su grupo.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Uso del método k-medias para detectar datos atípicos
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ajuste de Hiperparámetros en Tiempo Real

    Modifica los valores para evaluar el impacto geométrico en el clustering:
    """)
    return


@app.cell
def _(mo):
    k = mo.ui.slider(start=2, stop=8, label="Número de Clusters (K)")
    return (k,)


@app.cell
def _(k, mo):
    mo.hstack([k, mo.md(f"Valor: {k.value}")])
    return


@app.cell
def _(mo):
    percentil_corte = mo.ui.slider(
        start=95.0, stop=99.9, step=0.1, value=99.0, label="Percentil de Corte (%)"
    )
    return (percentil_corte,)


@app.cell
def _(mo, percentil_corte):
    mo.hstack([percentil_corte, mo.md(f"Valor: {percentil_corte.value}")])
    return


@app.cell
def _(KMeans, df_limpio, df_scaled, k, np, percentil_corte):
    kmeans = KMeans(n_clusters=k.value, random_state=42)
    df_limpio["Cluster"] = kmeans.fit_predict(df_scaled)

    # Obtenemos las coordenadas de los centroides y calculamos la distancia de cada punto a su centroide correspondiente
    centroides = kmeans.cluster_centers_
    distancias = np.sqrt(
        np.sum((df_scaled - centroides[df_limpio["Cluster"]]) ** 2, axis=1)
    )

    # El porcentaje de los datos más lejanos a cualquier clúster se consideran atípicos
    umbral = np.percentile(distancias, percentil_corte.value)
    df_limpio["Es_Atipico"] = distancias > umbral

    df_nuevo = df_limpio.copy()
    return (df_nuevo,)


@app.cell
def _(df_nuevo, px):
    # Creamos una columna de texto para formatear las leyendas de forma clara
    df_grafico = df_nuevo.copy()
    df_grafico["Clasificación"] = df_grafico["Cluster"].astype(str)
    df_grafico.loc[df_grafico["Es_Atipico"], "Clasificación"] = "Atípico"

    # Mapa de colores: clústeres comunes y rojo para anomalías
    mapa_colores = {
        "0": "#1f77b4",  # Azul
        "1": "#2ca02c",  # Verde
        "2": "#9467bd",  # Morado
        "3": "#bcbd22",  # Amarillo
        "4": "#17becf",  # Cian
        "5": "#e377c2",  # Rosa
        "6": "#ff7f0e",  # Naranja
        "7": "#8c564b",  # Café
        "8": "#7f7f7f",  # Gris
        "9": "#ffbb78",  # Naranja claro
        "Atípico": "#d62728",  # Rojo para Outliers
    }

    # Construcción del scatter plot interactivo
    fig = px.scatter(
        df_grafico,
        x="Global_active_power",
        y="Voltage",
        color="Clasificación",
        color_discrete_map=mapa_colores,
        symbol="Clasificación",
        symbol_sequence=[
            "circle",
            "x",
        ],  # Los normales serán círculos y los atípicos serán 'X'
        opacity=0.6,
        title="Detección de Atípicos (K-Medias)",
        labels={
            "Global_active_power": "Potencia Activa Global (kW)",
            "Voltage": "Voltaje (V)",
        },
        hover_data={
            "Cluster": True,
            "Es_Atipico": False,
        },  # Muestra datos limpios al pasar el cursor
    )

    # Estilizado del lienzo
    fig.update_layout(
        template="plotly_dark",
        legend_title_text="Estructura del Dataset",
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return


if __name__ == "__main__":
    app.run()
