import pandas as pd
import plotly.express as px
import os
from src.utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- CONFIGURACIÓN ---
# Rutas de entrada y salida usando el módulo de rutas
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'visualizations')
os.makedirs(REPORTS_DIR, exist_ok=True)

INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")
OUTPUT_HTML_PATH = os.path.join(REPORTS_DIR, "07_barras_apiladas_delito_turno.html")
TOP_N_DELITOS = 5

def generar_barras_apiladas():
    """
    Crea un gráfico de barras apiladas que muestra los principales tipos de delito por turno.
    """
    print(f"Leyendo datos desde: {INPUT_CSV_PATH}")
    try:
        df = pd.read_csv(INPUT_CSV_PATH, usecols=['tipo_hecho', 'turno_hecho'])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV: {INPUT_CSV_PATH}")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    print(f"Calculando el top {TOP_N_DELITOS} de tipos de hecho...")
    # Encontrar los N tipos de hechos más comunes
    top_delitos_lista = df['tipo_hecho'].value_counts().nlargest(TOP_N_DELITOS).index.tolist()
    
    # Filtrar el DataFrame para incluir solo esos tipos
    df_filtrado = df[df['tipo_hecho'].isin(top_delitos_lista)]

    print("Agrupando datos por tipo de hecho y turno...")
    conteo_agrupado = df_filtrado.groupby(['tipo_hecho', 'turno_hecho']).size().reset_index(name='conteo')

    # Ordenar los turnos de forma lógica
    orden_turnos = ['mañana', 'tarde', 'noche', 'madrugada']
    conteo_agrupado['turno_hecho'] = pd.Categorical(conteo_agrupado['turno_hecho'], categories=orden_turnos, ordered=True)
    conteo_agrupado = conteo_agrupado.sort_values('turno_hecho')

    print("Generando gráfico de barras apiladas...")
    fig = px.bar(
        conteo_agrupado,
        x='tipo_hecho',
        y='conteo',
        color='turno_hecho',
        title=f'Distribución por Turno de los {TOP_N_DELITOS} Tipos de Hecho más Comunes',
        labels={'tipo_hecho': 'Tipo de Hecho', 'conteo': 'Número de Denuncias', 'turno_hecho': 'Turno'}
    )
    
    fig.update_layout(title_x=0.5)

    print(f"Guardando gráfico en: {OUTPUT_HTML_PATH}")
    fig.write_html(OUTPUT_HTML_PATH)
    print("¡Gráfico de barras apiladas guardado exitosamente!")

if __name__ == '__main__':
    generar_barras_apiladas()
