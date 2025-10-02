import pandas as pd
import plotly.express as px
import numpy as np
import os
from dotenv import load_dotenv
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# Cargar variables de entorno desde el archivo .env en la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# --- CONFIGURACIÓN ---
MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")
OUTPUT_HTML_PATH = os.path.join(REPORTS_DIR, "mapa_burbujas_lima_callao.html")

def generar_mapa_burbujas():
    """
    Genera un mapa de burbujas interactivo para Lima y Callao usando el CSV pre-filtrado.
    """
    if not MAPBOX_TOKEN or MAPBOX_TOKEN == "TU_TOKEN_AQUI":
        print("Error: La llave de acceso de Mapbox no está configurada.")
        print("Por favor, revisa tu archivo .env en la raíz del proyecto.")
        return

    print(f"Paso 1: Leyendo el archivo CSV optimizado: {INPUT_CSV_PATH}")
    try:
        df = pd.read_csv(INPUT_CSV_PATH)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en la ruta: {INPUT_CSV_PATH}")
        print("Asegúrate de haber ejecutado primero el script 'src/data_processing/01_filtrar_lima_callao.py'")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
        return

    print("Paso 2: Agregando datos en una cuadrícula para optimizar memoria.")
    df.dropna(subset=['lat', 'lon'], inplace=True)
    BINS = 500
    # Ajustar el bounding box para incluir Lima y Callao
    LIMA_CALLAO_BOUNDS = [[-12.3, -11.8], [-77.4, -76.8]]
    
    counts, y_bins, x_bins = np.histogram2d(
        df['lat'], df['lon'], bins=BINS, range=LIMA_CALLAO_BOUNDS
    )
    lat_centers = (y_bins[:-1] + y_bins[1:]) / 2
    lon_centers = (x_bins[:-1] + x_bins[1:]) / 2
    
    aggregated_data = []
    for i in range(len(lat_centers)):
        for j in range(len(lon_centers)):
            if counts[i, j] > 0:
                aggregated_data.append([lat_centers[i], lon_centers[j], counts[i, j]])
    
    df_agg = pd.DataFrame(aggregated_data, columns=['lat', 'lon', 'count'])
    print(f"Se han agregado los datos en {len(df_agg)} celdas con denuncias.")

    print("Paso 3: Creando el mapa de burbujas interactivo...")
    fig = px.scatter_mapbox(
        df_agg,
        lat='lat',
        lon='lon',
        size='count',
        color='count',
        hover_data={'lat': False, 'lon': False, 'count': True},
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=40,
        mapbox_style="mapbox://styles/mapbox/streets-v11",
        zoom=8.5, # Zoom out slightly to fit both
        center={"lat": -12.06, "lon": -77.08}, # Center between Lima and Callao
        opacity=0.7
    )

    fig.update_layout(
        mapbox_accesstoken=MAPBOX_TOKEN,
        title_text='<b>Mapa de Burbujas de Denuncias en Lima y Callao</b>',
        title_x=0.5,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    print(f"Paso 4: Guardando el mapa en el archivo: {OUTPUT_HTML_PATH}")
    fig.write_html(OUTPUT_HTML_PATH)
    print("¡Mapa de burbujas guardado exitosamente!")

if __name__ == '__main__':
    generar_mapa_burbujas()
