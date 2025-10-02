import pandas as pd
import plotly.express as px
import os
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- CONFIGURACIÓN ---
# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")
OUTPUT_HTML_PATH = os.path.join(REPORTS_DIR, "04_barras_por_turno.html")

def generar_barras_por_turno():
    """
    Crea un gráfico de barras que muestra el número de denuncias por turno.
    """
    print(f"Leyendo datos desde: {INPUT_CSV_PATH}")
    try:
        df = pd.read_csv(INPUT_CSV_PATH, usecols=['turno_hecho'])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV: {INPUT_CSV_PATH}")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    print("Contando denuncias por turno...")
    conteo_por_turno = df['turno_hecho'].value_counts().reset_index()
    conteo_por_turno.columns = ['Turno', 'Número de Denuncias']

    # Ordenar por un orden lógico en lugar de por conteo
    orden_turnos = ['mañana', 'tarde', 'noche', 'madrugada']
    conteo_por_turno['Turno'] = pd.Categorical(conteo_por_turno['Turno'], categories=orden_turnos, ordered=True)
    conteo_por_turno = conteo_por_turno.sort_values('Turno')

    print("Generando gráfico de barras...")
    fig = px.bar(
        conteo_por_turno,
        x='Turno',
        y='Número de Denuncias',
        title='Número de Denuncias por Turno del Día',
        labels={'Turno': 'Turno del Día', 'Número de Denuncias': 'Total de Denuncias'}
    )
    
    fig.update_layout(title_x=0.5)

    print(f"Guardando gráfico en: {OUTPUT_HTML_PATH}")
    fig.write_html(OUTPUT_HTML_PATH)
    print("¡Gráfico de barras por turno guardado exitosamente!")

if __name__ == '__main__':
    generar_barras_por_turno()
