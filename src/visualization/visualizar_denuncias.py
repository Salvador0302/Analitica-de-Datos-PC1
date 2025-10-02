
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

# URL del archivo GeoJSON con los límites de los departamentos de Perú
GEOJSON_URL = "https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_departamental_simple.geojson"

# Nombre del archivo de salida HTML
OUTPUT_HTML_FILE = os.path.join(REPORTS_DIR, "mapa_denuncias_por_region.html")

# --- INICIO DEL SCRIPT ---

def main():
    """
    Función principal para generar el mapa de coropletas.
    """
    print(f"Paso 1: Leyendo el archivo de denuncias: {CSV_FILE_PATH}")
    try:
        # Lee el archivo CSV. Especificamos el tipo de 'departamento_hecho' como string.
        df = pd.read_csv(CSV_FILE_PATH, usecols=['departamento_hecho'], dtype={'departamento_hecho': str})
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en la ruta: {CSV_FILE_PATH}")
        print("Asegúrate de que el archivo exista y la ruta sea correcta.")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
        return

    print("Paso 2: Contando las denuncias por departamento...")
    # Agrupa por departamento y cuenta el número de denuncias.
    # reset_index() convierte el resultado de nuevo en un DataFrame.
    denuncias_por_dpto = df['departamento_hecho'].value_counts().reset_index()
    # Renombra las columnas para que sean más claras.
    denuncias_por_dpto.columns = ['departamento', 'cantidad_denuncias']
    print("Conteo finalizado:")
    print(denuncias_por_dpto)

    print(f"Paso 3: Descargando el archivo GeoJSON desde {GEOJSON_URL}")
    try:
        # Realiza una petición GET para obtener el GeoJSON.
        response = requests.get(GEOJSON_URL)
        response.raise_for_status()  # Lanza un error si la petición falla.
        geojson_data = response.json()
        print("GeoJSON descargado exitosamente.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el GeoJSON: {e}")
        return

    print("Paso 4: Creando el mapa de coropletas con Plotly...")
    # Crea la figura del mapa.
    fig = px.choropleth_mapbox(
        denuncias_por_dpto,
        geojson=geojson_data,
        locations='departamento',         # Columna del DataFrame que coincide con las regiones.
        featureidkey="properties.NOMBDEP",# Ruta a la propiedad en el GeoJSON que contiene el nombre del departamento.
        color='cantidad_denuncias',       # Columna que define el color de la región.
        color_continuous_scale="Viridis", # Esquema de color.
        mapbox_style="carto-positron",    # Estilo del mapa base.
        zoom=4,                           # Nivel de zoom inicial.
        center={"lat": -9.19, "lon": -75.01}, # Centro del mapa en Perú.
        opacity=0.6,
        labels={'cantidad_denuncias': 'Número de Denuncias'} # Etiqueta para la barra de color.
    )

    # Actualiza el diseño del mapa para añadir un título.
    fig.update_layout(
        title_text='<b>Número de Denuncias por Departamento en Perú</b>',
        title_x=0.5, # Centrar el título
        margin={"r":0,"t":40,"l":0,"b":0}
    )

    print(f"Paso 5: Guardando el mapa en el archivo: {OUTPUT_HTML_FILE}")
    # Guarda la figura en un archivo HTML.
    fig.write_html(OUTPUT_HTML_FILE)
    print("\n¡Proceso completado!")
    print(f"Puedes abrir el archivo '{OUTPUT_HTML_FILE}' en tu navegador para ver el mapa interactivo.")

if __name__ == '__main__':
    # Asegúrate de tener las librerías necesarias instaladas:
    # pip install pandas plotly requests
    main()
