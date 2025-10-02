import pandas as pd
import os
import time
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso5_renombrado.csv')
REPORTS_DIR = os.path.join(BASE_DIR, 'docs', 'analysis_reports')
os.makedirs(REPORTS_DIR, exist_ok=True)
output_json_path = os.path.join(REPORTS_DIR, '07_diccionario_categoricas.json')
CHUNK_SIZE = 100000

# Columnas categóricas a investigar
CATEGORICAL_COLS = [
    'departamento_hecho', 'provincia_hecho', 'distrito_hecho',
    'tipo_hecho', 'materia_hecho', 'turno_hecho', 'es_delito_x',
    'macroregpol_hecho', 'regionpol_hecho', 'estado_coord'
]

# --- Inicio del Script ---
print("Iniciando Verificación de Valores Únicos para Columnas Categóricas.")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print("Columnas a analizar:", CATEGORICAL_COLS)
print("="*80)

start_time = time.time()

# Diccionario para almacenar los sets de valores únicos
col_uniques = {col: set() for col in CATEGORICAL_COLS}

try:
    # Usar un iterador de chunks para procesar el archivo grande
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, usecols=CATEGORICAL_COLS, low_memory=False)

    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")
        # Recolectar valores únicos para cada columna
        for col in CATEGORICAL_COLS:
            col_uniques[col].update(chunk[col].dropna().unique())

    end_time = time.time()
    duration = end_time - start_time

    # Convertir los sets a listas ordenadas para una salida consistente
    final_uniques_dict = {col: sorted(list(values)) for col, values in col_uniques.items()}

    # --- Imprimir Reporte ---
    print("\n" + "="*80)
    print("  Diccionario de Valores Únicos por Columna Categórica")
    print("="*80)
    print(f"Proceso completado en {duration:.2f} segundos.")

    # Imprimir el diccionario de una forma legible
    for col, values in final_uniques_dict.items():
        print(f"\n--- Columna: '{col}' ({len(values)} valores únicos) ---")
        # Imprimir solo algunos si la lista es muy larga
        if len(values) > 20:
            print(values[:10], "...")
        else:
            print(values)
            
    # Opcional: Guardar el diccionario completo a un archivo JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(final_uniques_dict, f, ensure_ascii=False, indent=4)
    print(f"\nDiccionario completo guardado en: {output_json_path}")


except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
