import pandas as pd
import os
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_final.csv') # Usando el archivo unificado
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso2_sin_nulos.csv') # Nuevo nombre descriptivo
CHUNK_SIZE = 50000

# Columnas a eliminar basadas en el diagnóstico inicial (más de 95% de valores faltantes)
COLUMNS_TO_DROP = [
    'tipologias_ia',
    'cuadra_hecho',
    'barrio',
    'comisaria',
    'departamento',
    'provincia',
    'distrito',
    'indice_priorizacion',
    'fecha_inaguracion'
]

# --- Inicio del Script ---
print("Iniciando Paso 2: Manejo de valores faltantes (Eliminación de columnas).")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print(f"Archivo de salida: {os.path.basename(OUTPUT_FILE)}")
print(f"Columnas a eliminar: {COLUMNS_TO_DROP}")
print("="*80)

start_time = time.time()

try:
    # Usar un iterador de chunks para procesar el archivo grande
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False)

    is_first_chunk = True
    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")

        # Eliminar las columnas especificadas
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
    print(f"Se ha creado el archivo limpio en: {OUTPUT_FILE}")
    print(f"Tiempo total de procesamiento: {duration:.2f} segundos.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
