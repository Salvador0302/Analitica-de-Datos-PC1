import pandas as pd
import plotly.express as px
import os
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- CONFIGURACIÓN ---
# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")
OUTPUT_HTML_PATH = os.path.join(REPORTS_DIR, "06_torta_por_materia.html")

def generar_torta_por_materia():
    """
    Crea un gráfico de torta que muestra la distribución de denuncias por materia del hecho.
    """
    print(f"Leyendo datos desde: {INPUT_CSV_PATH}")
    try:
        df = pd.read_csv(INPUT_CSV_PATH, usecols=['materia_hecho'])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV: {INPUT_CSV_PATH}")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    print("Contando denuncias por materia...")
    conteo_por_materia = df['materia_hecho'].value_counts().reset_index()
    conteo_por_materia.columns = ['Materia del Hecho', 'Número de Denuncias']

    print("Generando gráfico de torta...")
    fig = px.pie(
        conteo_por_materia,
        names='Materia del Hecho',
        values='Número de Denuncias',
        title='Distribución de Denuncias por Materia del Hecho',
        hole=.3 # Estilo "donut"
    )
    
    fig.update_layout(title_x=0.5)

    print(f"Guardando gráfico en: {OUTPUT_HTML_PATH}")
    fig.write_html(OUTPUT_HTML_PATH)
    print("¡Gráfico de torta por materia guardado exitosamente!")

if __name__ == '__main__':
    generar_torta_por_materia()
