
import pandas as pd
import plotly.express as px
import json
import requests
import os
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- CONFIGURACIÓN ---

# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

CSV_FILE_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_final.csv")

# URL del archivo GeoJSON con los límites de las provincias de Perú
GEOJSON_URL = "https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_provincial_simple.geojson"

# Nombre del archivo de salida HTML
OUTPUT_HTML_FILE = os.path.join(REPORTS_DIR, "mapa_denuncias_lima.html")

# Departamento que queremos visualizar
DEPARTAMENTO_OBJETIVO = "LIMA"

# --- INICIO DEL SCRIPT ---

def main():
    """
    Función principal para generar el mapa de coropletas de las provincias de Lima.
    """
    print(f"Paso 1: Leyendo el archivo de denuncias: {CSV_FILE_PATH}")
    try:
        # Lee solo las columnas necesarias para optimizar la memoria.
        df = pd.read_csv(CSV_FILE_PATH, usecols=['departamento_hecho', 'provincia_hecho'], dtype=str)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en la ruta: {CSV_FILE_PATH}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
        return

    print(f"Paso 2: Filtrando denuncias para el departamento de '{DEPARTAMENTO_OBJETIVO}'.")
    df_lima = df[df['departamento_hecho'] == DEPARTAMENTO_OBJETIVO].copy()

    if df_lima.empty:
        print(f"No se encontraron denuncias para el departamento '{DEPARTAMENTO_OBJETIVO}'. No se puede generar el mapa.")
        return

    print("Paso 3: Contando las denuncias por provincia...")
    denuncias_por_prov = df_lima['provincia_hecho'].value_counts().reset_index()
    denuncias_por_prov.columns = ['provincia', 'cantidad_denuncias']
    print("Conteo finalizado:")
    print(denuncias_por_prov)

    print(f"Paso 4: Descargando y filtrando el archivo GeoJSON para '{DEPARTAMENTO_OBJETIVO}'.")
    try:
        response = requests.get(GEOJSON_URL)
        response.raise_for_status()
        geojson_full = response.json()

        # Filtra el GeoJSON para mantener solo las provincias del departamento objetivo.
        lima_features = [
            feature for feature in geojson_full['features'] 
            if feature['properties']['FIRST_NOMB'] == DEPARTAMENTO_OBJETIVO
        ]
        
        if not lima_features:
            print(f"Error: No se encontraron provincias para '{DEPARTAMENTO_OBJETIVO}' en el archivo GeoJSON.")
            return

        geojson_lima = {"type": "FeatureCollection", "features": lima_features}
        print("GeoJSON filtrado exitosamente.")

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar o procesar el GeoJSON: {e}")
        return

    print("Paso 5: Creando el mapa de coropletas para las provincias de Lima...")
    fig = px.choropleth_mapbox(
        denuncias_por_prov,
        geojson=geojson_lima,
        locations='provincia',
        featureidkey="properties.NOMBPROV", # Propiedad en GeoJSON para el nombre de la provincia
        color='cantidad_denuncias',
        color_continuous_scale="Cividis",
        mapbox_style="carto-positron",
        zoom=7, # Aumentamos el zoom para enfocar en Lima
        center={"lat": -12.0464, "lon": -76.5}, # Centramos el mapa en Lima
        opacity=0.7,
        labels={'cantidad_denuncias': 'Número de Denuncias'}
    )

    fig.update_layout(
        title_text=f'<b>Número de Denuncias por Provincia en {DEPARTAMENTO_OBJETIVO.title()}</b>',
        title_x=0.5,
        margin={"r":0,"t":40,"l":0,"b":0}
    )

    print(f"Paso 6: Guardando el mapa en el archivo: {OUTPUT_HTML_FILE}")
    fig.write_html(OUTPUT_HTML_FILE)
    print("\n¡Proceso completado!")
    print(f"Puedes abrir el archivo '{OUTPUT_HTML_FILE}' en tu navegador.")

if __name__ == '__main__':
    # Las librerías necesarias (pandas, plotly, requests) ya deberían estar instaladas.
    main()
