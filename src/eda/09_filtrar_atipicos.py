import pandas as pd
import os
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso7_codificado.csv')
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_final.csv')
CHUNK_SIZE = 50000

# --- Límites Geográficos de Perú (en Grados Decimales) ---
# Latitud Sur es negativa, Longitud Oeste es negativa.
# Se usa un pequeño margen para seguridad.
LAT_MIN = -18.4
LAT_MAX = 0
LON_MIN = -81.4
LON_MAX = -68.6

# --- Inicio del Script ---
print("Iniciando Paso 8: Filtrado de Valores Atípicos (Geográficos).")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print(f"Archivo de salida: {os.path.basename(OUTPUT_FILE)}")
print(f"Límites de Latitud: {LAT_MIN} a {LAT_MAX}")
print(f"Límites de Longitud: {LON_MIN} a {LON_MAX}")
print("="*80)

start_time = time.time()
total_rows = 0
outlier_rows = 0

try:
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False, parse_dates=['fecha_hora_hecho'])

    is_first_chunk = True
    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")
        rows_before = len(chunk)
        total_rows += rows_before

        # Filtrar outliers
        chunk_filtered = chunk[
            (chunk['lat'].between(LAT_MIN, LAT_MAX)) &
            (chunk['lon'].between(LON_MIN, LON_MAX))
        ]
        
        rows_after = len(chunk_filtered)
        outlier_rows += (rows_before - rows_after)

        if is_first_chunk:
            # Solo escribir si el chunk filtrado no está vacío
            if not chunk_filtered.empty:
                chunk_filtered.to_csv(OUTPUT_FILE, index=False, mode='w')
                is_first_chunk = False
        else:
            if not chunk_filtered.empty:
                chunk_filtered.to_csv(OUTPUT_FILE, index=False, mode='a', header=False)

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*80)
    print("Proceso de filtrado completado.")
    print(f"Total de filas procesadas: {total_rows:,}")
    print(f"Filas eliminadas como outliers: {outlier_rows:,}")
    print(f"Filas en el archivo final: {(total_rows - outlier_rows):,}")
    print(f"Se ha creado el archivo final limpio en: {OUTPUT_FILE}")
    print(f"Tiempo total de procesamiento: {duration:.2f} segundos.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
