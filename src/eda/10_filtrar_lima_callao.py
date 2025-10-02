import pandas as pd
import os
from src.utils.paths import PROCESSED_DATA_DIR

# Rutas de entrada y salida utilizando el módulo de rutas centralizado
INPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_final.csv")
OUTPUT_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "denuncias_lima_callao.csv")

PROVINCIAS_OBJETIVO = ["LIMA", "CALLAO"]

# --- INICIO DEL SCRIPT ---

def filtrar_csv_por_provincia():
    """
    Lee el CSV completo, filtra por las provincias objetivo y guarda el resultado
    en un nuevo archivo CSV.
    """
    print(f"Paso 1: Leyendo el archivo CSV completo: {INPUT_CSV_PATH}")
    try:
        df = pd.read_csv(INPUT_CSV_PATH)
        print(f"Lectura completada. El archivo tiene {len(df)} filas.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en la ruta: {INPUT_CSV_PATH}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
        return

    print(f"Paso 2: Filtrando denuncias para las provincias: {', '.join(PROVINCIAS_OBJETIVO)}")
    
    # Asegurarse de que la columna existe
    if 'provincia_hecho' not in df.columns:
        print("Error: La columna 'provincia_hecho' no se encuentra en el CSV.")
        return

    df_filtrado = df[df['provincia_hecho'].isin(PROVINCIAS_OBJETIVO)].copy()
    
    num_filas_filtradas = len(df_filtrado)
    print(f"Filtrado completado. Se encontraron {num_filas_filtradas} filas para Lima y Callao.")

    if num_filas_filtradas == 0:
        print("No se encontraron datos para las provincias especificadas. No se generará el archivo.")
        return

    print(f"Paso 3: Guardando el nuevo archivo CSV en: {OUTPUT_CSV_PATH}")
    try:
        df_filtrado.to_csv(OUTPUT_CSV_PATH, index=False)
        print("¡Archivo guardado exitosamente!")
    except Exception as e:
        print(f"Ocurrió un error al guardar el nuevo archivo CSV: {e}")
        return

if __name__ == '__main__':
    filtrar_csv_por_provincia()
