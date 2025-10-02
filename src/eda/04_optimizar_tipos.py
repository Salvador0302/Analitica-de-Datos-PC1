import pandas as pd
import os
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso3_transformado.csv')
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso4_optimizado.csv')
CHUNK_SIZE = 50000

# Mapeo de tipos de datos basado en la verificación del dataset completo
DTYPE_MAPPING = {
    # Enteros a int8
    'mes_hecho': 'int8',
    'dia_hecho': 'int8',
    'id_materia_hecho': 'int8',
    'id_dpto_hecho': 'int8',
    'solo_denuncia': 'int8',
    'estado': 'int8',
    # Enteros a int16
    'ano_hecho': 'int16',
    'id_tipo_hecho': 'int16',
    # Floats a float32
    'lat': 'float32',
    'lon': 'float32',
    'lat_hecho': 'float32',
    'long_hecho': 'float32',
}

# --- Inicio del Script ---
print("Iniciando Paso 4: Optimización de Tipos de Datos (Numéricos).")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print(f"Archivo de salida: {os.path.basename(OUTPUT_FILE)}")
print("Aplicando las siguientes optimizaciones:")
for col, dtype in DTYPE_MAPPING.items():
    print(f"- Columna '{col}' -> {dtype}")
print("="*80)

start_time = time.time()

try:
    # Usar un iterador de chunks para procesar el archivo grande
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False, parse_dates=['fecha_hora_hecho'])

    is_first_chunk = True
    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")

        # Aplicar la conversión de tipos
        # Usamos un bucle con try-except por si alguna columna no existiera
        for col, dtype in DTYPE_MAPPING.items():
            if col in chunk.columns:
                try:
                    chunk[col] = chunk[col].astype(dtype)
                except Exception as e:
                    print(f"  - Advertencia: No se pudo convertir la columna '{col}' en el chunk {i+1}. Error: {e}")

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
    print(f"Se ha creado el archivo optimizado en: {OUTPUT_FILE}")
    print(f"Tiempo total de procesamiento: {duration:.2f} segundos.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
