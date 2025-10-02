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

CSV_FILE_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_final.csv")
OUTPUT_HTML_FILE = os.path.join(REPORTS_DIR, "heatmap_denuncias_lima.html")

# Filtros geográficos
DEPARTAMENTO_OBJETIVO = "LIMA"
PROVINCIA_OBJETIVO = "LIMA"

# --- INICIO DEL SCRIPT ---

def main():
    """
    Función principal para generar el mapa de calor (density map).
    """
    if not MAPBOX_TOKEN or MAPBOX_TOKEN == "TU_TOKEN_AQUI":
        print("Error: La llave de acceso de Mapbox no está configurada.")
        print("Por favor, crea un archivo .env, copia el contenido de .env.example y añade tu token.")
        return

    print(f"Paso 1: Leyendo el archivo de denuncias: {CSV_FILE_PATH}")
    try:
        df = pd.read_csv(
            CSV_FILE_PATH,
            usecols=['departamento_hecho', 'provincia_hecho', 'lat', 'lon'],
            dtype={'departamento_hecho': str, 'provincia_hecho': str}
        )
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en la ruta: {CSV_FILE_PATH}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
        return

    print(f"Paso 2: Filtrando denuncias para la provincia de '{PROVINCIA_OBJETIVO}'.")
    df_filtered = df[
        (df['departamento_hecho'] == DEPARTAMENTO_OBJETIVO) &
        (df['provincia_hecho'] == PROVINCIA_OBJETIVO)
    ].copy()
    df_filtered.dropna(subset=['lat', 'lon'], inplace=True)

    if df_filtered.empty:
        print(f"No se encontraron denuncias con coordenadas válidas para '{PROVINCIA_OBJETIVO}'.")
        return

    print("Paso 3: Agregando datos en una cuadrícula para optimizar memoria.")
    BINS = 500
    LIMA_BOUNDS = [[-12.3, -11.8], [-77.3, -76.8]]
    counts, y_bins, x_bins = np.histogram2d(
        df_filtered['lat'], df_filtered['lon'], bins=BINS, range=LIMA_BOUNDS
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

    print("Paso 4: Creando el mapa de burbujas interactivo...")
    fig = px.scatter_mapbox(
        df_agg,
        lat='lat',
        lon='lon',
        size='count',
        color='count',
        hover_data={'lat': False, 'lon': False, 'count': True}, # Muestra solo la cuenta al pasar el ratón
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=40,
        mapbox_style="mapbox://styles/mapbox/streets-v11", # Usar la URL completa del estilo
        zoom=9,
        center={"lat": -12.0464, "lon": -77.0428},
        opacity=0.7 # Un poco de transparencia
    )

    fig.update_layout(
        mapbox_accesstoken=MAPBOX_TOKEN, # Pasar el token directamente al layout
        title_text=f'<b>Mapa de Burbujas de Denuncias en {PROVINCIA_OBJETIVO.title()}</b>',
        title_x=0.5,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    print(f"Paso 5: Guardando el mapa en el archivo: {OUTPUT_HTML_FILE}")
    fig.write_html(OUTPUT_HTML_FILE)

    print("Paso 6: Abriendo el mapa en el navegador...")
    fig.show()

    print("\n¡Proceso completado!")

if __name__ == '__main__':
    main()
