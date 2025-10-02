import pandas as pd
import plotly.express as px
import os
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- CONFIGURACIÓN ---
# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")
OUTPUT_HTML_PATH = os.path.join(REPORTS_DIR, "08_barras_top_distritos.html")
TOP_N = 15

def generar_barras_top_distritos():
    """
    Crea un gráfico de barras con los 15 distritos con más denuncias.
    """
    print(f"Leyendo datos desde: {INPUT_CSV_PATH}")
    try:
        df = pd.read_csv(INPUT_CSV_PATH, usecols=['distrito_hecho'])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV: {INPUT_CSV_PATH}")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    print(f"Contando los {TOP_N} distritos con más denuncias...")
    top_distritos = df['distrito_hecho'].value_counts().nlargest(TOP_N).reset_index()
    top_distritos.columns = ['Distrito', 'Número de Denuncias']

    print("Generando gráfico de barras...")
    fig = px.bar(
        top_distritos,
        x='Número de Denuncias',
        y='Distrito',
        orientation='h',
        title=f'Top {TOP_N} Distritos con Mayor Número de Denuncias'
    )
    
    # Invertir el eje Y para que el más común aparezca arriba
    fig.update_layout(
        title_x=0.5,
        yaxis={'categoryorder':'total ascending'}
    )

    print(f"Guardando gráfico en: {OUTPUT_HTML_PATH}")
    fig.write_html(OUTPUT_HTML_PATH)
    print("¡Gráfico de barras de top distritos guardado exitosamente!")

if __name__ == '__main__':
    generar_barras_top_distritos()
