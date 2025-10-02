import pandas as pd
import plotly.express as px
import os
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- CONFIGURACIÓN ---
# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")
OUTPUT_HTML_PATH = os.path.join(REPORTS_DIR, "02_linea_temporal.html")

def generar_linea_temporal():
    """
    Crea un gráfico de líneas que muestra la evolución de las denuncias a lo largo del tiempo.
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

    print("Procesando fechas...")
    # Convertir a datetime, los errores se convertirán en NaT (Not a Time)
    df['fecha'] = pd.to_datetime(df['fecha_hora_hecho'], errors='coerce')
    df.dropna(subset=['fecha'], inplace=True)

    # Agrupar por fecha y contar denuncias
    denuncias_por_dia = df.groupby(df['fecha'].dt.date).size().reset_index(name='conteo')
    denuncias_por_dia.rename(columns={'fecha': 'Fecha', 'conteo': 'Número de Denuncias'}, inplace=True)

    print("Generando gráfico de líneas...")
    fig = px.line(
        denuncias_por_dia,
        x='Fecha',
        y='Número de Denuncias',
        title='Evolución del Número de Denuncias a lo largo del Tiempo'
    )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Fecha",
        yaxis_title="Número de Denuncias Diarias"
    )

    print(f"Guardando gráfico en: {OUTPUT_HTML_PATH}")
    fig.write_html(OUTPUT_HTML_PATH)
    print("¡Gráfico de línea temporal guardado exitosamente!")

if __name__ == '__main__':
    generar_linea_temporal()
