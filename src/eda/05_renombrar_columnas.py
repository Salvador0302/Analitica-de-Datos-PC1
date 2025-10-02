import pandas as pd
import os
import time
import unicodedata
import re
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso4_optimizado.csv')
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso5_renombrado.csv')
CHUNK_SIZE = 50000

def normalize_column_name(name):
    """
    Normaliza un nombre de columna a formato snake_case.
    Ej: 'Año Hecho' -> 'ano_hecho'
    """
    # Transliterar caracteres con acentos y ñ
    nfkd_form = unicodedata.normalize('NFKD', name)
    name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    # Convertir a minúsculas
    name = name.lower()
    # Reemplazar caracteres no alfanuméricos con guion bajo
    name = re.sub(r'[^a-z0-9]+', '_', name)
    # Quitar guiones bajos al principio o final
    name = name.strip('_')
    return name

# --- Inicio del Script ---
print("Iniciando Paso 5: Renombrar y Estandarizar Nombres de Columnas.")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print(f"Archivo de salida: {os.path.basename(OUTPUT_FILE)}")
print("="*80)

start_time = time.time()

try:
    # Leer solo la cabecera para mostrar el antes y el después
    header_df = pd.read_csv(INPUT_FILE, nrows=0, low_memory=False)
    new_columns = {col: normalize_column_name(col) for col in header_df.columns}
    print("Se aplicarán los siguientes cambios en los nombres:")
    changed = False
    for old, new in new_columns.items():
        if old != new:
            print(f"- '{old}' -> '{new}'")
            changed = True
    if not changed:
        print("(No se encontraron columnas que necesiten cambios)")

    # Usar un iterador de chunks para procesar el archivo grande
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False)

    is_first_chunk = True
    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")

        # Renombrar las columnas del chunk actual
        chunk.rename(columns=new_columns, inplace=True)

        if is_first_chunk:
            chunk.to_csv(OUTPUT_FILE, index=False, mode='w')
            is_first_chunk = False
        else:
            chunk.to_csv(OUTPUT_FILE, index=False, mode='a', header=False)

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*80)
    print("Proceso completado.")
    print(f"Se ha creado el archivo con columnas renombradas en: {OUTPUT_FILE}")
    print(f"Tiempo total de procesamiento: {duration:.2f} segundos.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
