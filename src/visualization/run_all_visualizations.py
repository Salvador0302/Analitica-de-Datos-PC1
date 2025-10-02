import sys
import os

# Añadir el directorio 'src' al path para permitir importaciones absolutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar las funciones principales de cada script de visualización
from visualization.vis_01_mapa_burbujas_lima_callao import generar_mapa_burbujas
from visualization.vis_02_linea_temporal import generar_linea_temporal
from visualization.vis_03_heatmap_hora_dia import generar_heatmap_hora_dia
from visualization.vis_04_barras_por_turno import generar_barras_por_turno
from visualization.vis_05_barras_top_delitos import generar_barras_top_delitos
from visualization.vis_06_torta_por_materia import generar_torta_por_materia
from visualization.vis_07_barras_apiladas_delito_turno import generar_barras_apiladas_delito_turno
from visualization.vis_08_barras_top_distritos import generar_barras_top_distritos

# Lista de tuplas con el nombre de la visualización y la función que la genera
visualizaciones = [
    ("Mapa de Burbujas", generar_mapa_burbujas),
    ("Línea Temporal", generar_linea_temporal),
    ("Heatmap Hora/Día", generar_heatmap_hora_dia),
    ("Barras por Turno", generar_barras_por_turno),
    ("Barras Top Delitos", generar_barras_top_delitos),
    ("Torta por Materia", generar_torta_por_materia),
    ("Barras Apiladas Delito/Turno", generar_barras_apiladas_delito_turno),
    ("Barras Top Distritos", generar_barras_top_distritos),
]

def ejecutar_todas():
    """
    Ejecuta todas las funciones de generación de visualizaciones de forma secuencial.
    """
    print("--- Iniciando la generación de todas las visualizaciones ---")
    total = len(visualizaciones)
    for i, (nombre, funcion) in enumerate(visualizaciones):
        print(f"\n[{i+1}/{total}] Generando: {nombre}")
        try:
            funcion()
        except Exception as e:
            print(f"--- ERROR al generar '{nombre}': {e}. Abortando. ---")
            # Considerar si se debe continuar o abortar. Por ahora, abortamos.
            break
    else:
        print("\n--- ¡Todas las visualizaciones han sido generadas exitosamente! ---")

if __name__ == "__main__":
    ejecutar_todas()