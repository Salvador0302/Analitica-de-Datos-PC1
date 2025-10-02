import pandas as pd
import plotly.express as px
import os
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- CONFIGURACIÓN ---
# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")
OUTPUT_HTML_PATH = os.path.join(REPORTS_DIR, "03_heatmap_hora_dia.html")

def generar_heatmap_hora_dia():
    """
    Crea un mapa de calor que muestra la concentración de denuncias por día de la semana y hora del día.
    """
    print(f"Leyendo datos desde: {INPUT_CSV_PATH}")
    try:
        df = pd.read_csv(INPUT_CSV_PATH, usecols=['fecha_hora_hecho'])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV: {INPUT_CSV_PATH}")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    print("Procesando fechas para extraer día y hora...")
    df['fecha'] = pd.to_datetime(df['fecha_hora_hecho'], errors='coerce')
    df.dropna(subset=['fecha'], inplace=True)

    # Extraer hora y día de la semana
    df['hora'] = df['fecha'].dt.hour
    df['dia_semana'] = df['fecha'].dt.day_name()

    # Ordenar los días de la semana
    dias_ordenados = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df['dia_semana'] = pd.Categorical(df['dia_semana'], categories=dias_ordenados, ordered=True)

    # Agrupar para obtener la matriz de calor
    heatmap_data = df.groupby(['dia_semana', 'hora']).size().reset_index(name='conteo')

    print("Generando mapa de calor...")
    fig = px.density_heatmap(
        heatmap_data,
        x="hora",
        y="dia_semana",
        z="conteo",
        title="Concentración de Denuncias por Hora y Día de la Semana",
        labels={'hora': 'Hora del Día', 'dia_semana': 'Día de la Semana', 'conteo': 'Número de Denuncias'}
    )
    
    fig.update_layout(title_x=0.5)

    print(f"Guardando gráfico en: {OUTPUT_HTML_PATH}")
    fig.write_html(OUTPUT_HTML_PATH)
    print("¡Mapa de calor guardado exitosamente!")

if __name__ == '__main__':
    generar_heatmap_hora_dia()
