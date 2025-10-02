import pandas as pd
import os
import time
import numpy as np
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso3_transformado.csv')
CHUNK_SIZE = 50000

# Columnas a verificar
NUMERIC_COLS = [
    'mes_hecho', 'dia_hecho', 'id_tipo_hecho', 'id_materia_hecho',
    'ano_hecho', 'id_dpto_hecho', 'solo_denuncia', 'estado',
    'lat', 'lon', 'lat_hecho', 'long_hecho'
]
CATEGORICAL_COLS = [
    'departamento_hecho', 'provincia_hecho', 'distrito_hecho',
    'tipo_hecho', 'materia_hecho', 'turno_hecho', 'es_delito_x',
    'macroregpol_hecho', 'regionpol_hecho', 'estado_coord'
]

# --- Inicio del Script ---
print("Iniciando Paso Intermedio: Verificación de Tipos de Datos en todo el dataset.")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print("Esto puede tardar unos minutos...")
print("="*80)

start_time = time.time()

# Diccionarios para almacenar los resultados
col_ranges = {col: {'min': np.inf, 'max': -np.inf} for col in NUMERIC_COLS}
col_uniques = {col: set() for col in CATEGORICAL_COLS}

try:
    # Usar un iterador de chunks para procesar el archivo grande
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False)

    total_rows = 0
    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")
        total_rows += len(chunk)

        # Verificar rangos para columnas numéricas
        for col in NUMERIC_COLS:
            if col in chunk.columns:
                current_min = chunk[col].min()
                current_max = chunk[col].max()
                if current_min < col_ranges[col]['min']:
                    col_ranges[col]['min'] = current_min
                if current_max > col_ranges[col]['max']:
                    col_ranges[col]['max'] = current_max

        # Recolectar valores únicos para columnas categóricas
        for col in CATEGORICAL_COLS:
            if col in chunk.columns:
                col_uniques[col].update(chunk[col].dropna().unique())

    end_time = time.time()
    duration = end_time - start_time

    # --- Imprimir Reporte ---
    print("\n" + "="*80)
    print("  Reporte de Verificación de Tipos de Datos (Dataset Completo)")
    print("="*80)
    print(f"Proceso completado en {duration:.2f} segundos. Total de filas analizadas: {total_rows:,}")

    print("\n--- Rangos de Columnas Numéricas ---")
    print(f"{'Columna':<25} {'Min Real':<15} {'Max Real':<15}")
    print("-" * 60)
    for col, ranges in col_ranges.items():
        print(f"{col:<25} {ranges['min']:<15} {ranges['max']:<15}")

    print("\n--- Conteo de Valores Únicos (Categóricas) ---")
    print(f"{'Columna':<25} {'Valores Únicos':<15}")
    print("-" * 60)
    for col, uniques in col_uniques.items():
        print(f"{col:<25} {len(uniques):<15}")

    print("\n" + "="*80)
    print("Análisis completado. Ahora podemos tomar una decisión informada sobre la optimización.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
