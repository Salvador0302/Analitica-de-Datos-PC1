import pandas as pd
import os
import time
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- Configuración ---
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso5_renombrado.csv')
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_paso7_codificado.csv')
REPORTS_DIR = os.path.join(BASE_DIR, 'docs', 'analysis_reports')
os.makedirs(REPORTS_DIR, exist_ok=True)
DICT_OUTPUT_FILE = os.path.join(REPORTS_DIR, '08_diccionario_codificacion.json')
CHUNK_SIZE = 50000

# --- Definición de Transformaciones y Diccionario de Datos ---

# 1. Limpieza para 'estado_coord'
estado_coord_replace_map = {
    'SIN COORDENADA XX': 'SIN COORDENADA',
    'SIN COORDENADA YY': 'SIN COORDENADA'
}

# 2. Codificación Ordinal para 'turno_hecho'
turno_hecho_encoding_map = {
    'madrugada': 0,
    'mañana': 1,
    'tarde': 2,
    'noche': 3
}

# 3. Binning para la hora del día
hour_bins = [-1, 5, 11, 17, 23]
hour_labels = ['Madrugada', 'Mañana', 'Tarde', 'Noche']

# 4. Codificación Binaria para 'tiene_coordenada'
tiene_coordenada_map = {
    'CON COORDENADA': 1,
    'SIN COORDENADA': 0
}

# --- Diccionario de Datos para Documentación ---
data_dictionary = {
    "estado_coord_cleaning": {
        "description": "Se unificaron valores en la columna 'estado_coord'.",
        "mapping": estado_coord_replace_map
    },
    "turno_hecho_encoding": {
        "description": "Codificación ordinal de la columna 'turno_hecho'.",
        "mapping": {
            "0": "madrugada",
            "1": "mañana",
            "2": "tarde",
            "3": "noche"
        }
    },
    "periodo_dia_binning": {
        "description": "Nueva columna creada agrupando la hora de 'fecha_hora_hecho'.",
        "bins": {
            "0-5": "Madrugada",
            "6-11": "Mañana",
            "12-17": "Tarde",
            "18-23": "Noche"
        }
    },
    "tiene_coordenada_encoding": {
        "description": "Codificación binaria (0/1) creada a partir de 'estado_coord' limpio.",
        "mapping": tiene_coordenada_map
    }
}


# --- Inicio del Script ---
print("Iniciando Paso 7: Codificación y Binning.")
print(f"Archivo de entrada: {os.path.basename(INPUT_FILE)}")
print(f"Archivo de salida: {os.path.basename(OUTPUT_FILE)}")
print(f"Diccionario de datos se guardará en: {os.path.basename(DICT_OUTPUT_FILE)}")
print("="*80)

start_time = time.time()

try:
    chunk_iter = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False, parse_dates=['fecha_hora_hecho'])

    is_first_chunk = True
    for i, chunk in enumerate(chunk_iter):
        print(f"Procesando chunk {i+1}...")

        # 1. Limpiar 'estado_coord'
        chunk['estado_coord'] = chunk['estado_coord'].replace(estado_coord_replace_map)

        # 2. Codificar 'turno_hecho'
        chunk['turno_hecho_cod'] = chunk['turno_hecho'].map(turno_hecho_encoding_map)

        # 3. Binning de la hora
        chunk['periodo_dia'] = pd.cut(chunk['fecha_hora_hecho'].dt.hour, bins=hour_bins, labels=hour_labels, right=True)

        # 4. Crear 'tiene_coordenada'
        chunk['tiene_coordenada'] = chunk['estado_coord'].map(tiene_coordenada_map)

        if is_first_chunk:
            chunk.to_csv(OUTPUT_FILE, index=False, mode='w')
            is_first_chunk = False
        else:
            chunk.to_csv(OUTPUT_FILE, index=False, mode='a', header=False)

    # Guardar el diccionario de datos
    with open(DICT_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_dictionary, f, ensure_ascii=False, indent=4)

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*80)
    print("Proceso completado.")
    print(f"Se ha creado el archivo transformado en: {OUTPUT_FILE}")
    print(f"Se ha guardado el diccionario de datos en: {DICT_OUTPUT_FILE}")
    print(f"Tiempo total de procesamiento: {duration:.2f} segundos.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo de entrada en la ruta especificada:\n{INPUT_FILE}")
except Exception as e:
    print(f"Ocurrió un error durante el procesamiento: {e}")
