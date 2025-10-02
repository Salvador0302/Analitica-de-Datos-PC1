import pandas as pd
import os
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso2_sin_nulos.csv')
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso3_transformado.csv')
CHUNK_SIZE = 50000

# Columnas a eliminar que son redundantes después de la conversión
COLUMNS_TO_DROP = [
    'fecha_hecho',
    'hora_hecho'
]

# --- Inicio del Script ---
print("Iniciando Paso 3: Transformación de Columnas (Fechas).")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print(f"Archivo de salida: {os.path.basename(OUTPUT_FILE)}")
print("="*80)

start_time = time.time()

try:
    # Usar un iterador de chunks para procesar el archivo grande
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False)

    is_first_chunk = True
    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")

        # 1. Convertir 'fecha_hora_hecho' a datetime
        # errors='coerce' convertirá las fechas no válidas en NaT (Not a Time)
        chunk['fecha_hora_hecho'] = pd.to_datetime(chunk['fecha_hora_hecho'], errors='coerce')

        # 2. Eliminar columnas de fecha/hora redundantes
        chunk.drop(columns=COLUMNS_TO_DROP, inplace=True, errors='ignore')

        if is_first_chunk:
            # Para el primer chunk, escribir con encabezado
            chunk.to_csv(OUTPUT_FILE, index=False, mode='w')
            is_first_chunk = False
        else:
            # Para los siguientes, añadir sin encabezado
            chunk.to_csv(OUTPUT_FILE, index=False, mode='a', header=False)
    
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*80)
    print("Proceso completado.")
    print(f"Se ha creado el archivo con fechas transformadas en: {OUTPUT_FILE}")
    print(f"Tiempo total de procesamiento: {duration:.2f} segundos.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
