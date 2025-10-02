import pandas as pd
import os
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso5_renombrado.csv')
CHUNK_SIZE = 100000
COLUMN_TO_CHECK = 'objectid'

# --- Inicio del Script ---
print(f"Iniciando Verificación de Unicidad para la columna '{COLUMN_TO_CHECK}'.")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print("Esto puede tardar unos minutos...")
print("="*80)

start_time = time.time()

seen_ids = set()
total_rows = 0
duplicate_count = 0

try:
    # Usar un iterador de chunks para procesar el archivo grande
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, usecols=[COLUMN_TO_CHECK], low_memory=False)

    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")
        total_rows += len(chunk)
        # Contar duplicados dentro del chunk y con los ya vistos
        chunk_uniques = chunk[COLUMN_TO_CHECK].nunique()
        if chunk_uniques < len(chunk):
            duplicate_count += len(chunk) - chunk_uniques
        
        # Contar duplicados entre chunks
        new_ids = set(chunk[COLUMN_TO_CHECK])
        duplicates_with_seen = len(new_ids.intersection(seen_ids))
        duplicate_count += duplicates_with_seen
        seen_ids.update(new_ids)

    end_time = time.time()
    duration = end_time - start_time

    unique_count = len(seen_ids)

    # --- Imprimir Reporte ---
    print("\n" + "="*80)
    print("  Reporte de Verificación de Unicidad")
    print("="*80)
    print(f"Proceso completado en {duration:.2f} segundos.")
    print(f"Columna analizada: '{COLUMN_TO_CHECK}'")
    print(f"Total de filas analizadas: {total_rows:,}")
    print(f"Valores únicos encontrados: {unique_count:,}")
    
    print("\n--- Conclusión ---")
    if total_rows == unique_count:
        print("(OK) ¡Confirmado! La columna es un identificador único. No hay duplicados.")
    else:
        # El cálculo de duplicados es complejo en chunks, una simple resta es más clara
        calculated_duplicates = total_rows - unique_count
        print(f"(ERROR) ¡Atención! La columna NO es un identificador único.")
        print(f"   Se encontraron {calculated_duplicates:,} filas duplicadas basadas en '{COLUMN_TO_CHECK}'.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
