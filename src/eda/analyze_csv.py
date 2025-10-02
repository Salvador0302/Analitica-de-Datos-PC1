
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR

# Construir la ruta al archivo CSV grande
file_path = os.path.join(PROCESSED_DATA_DIR, 'denuncias_final.csv')

try:
    # Leer solo una pequeña parte del archivo (chunk) para obtener la estructura
    # Esto es muy eficiente en memoria
    chunk = next(pd.read_csv(file_path, chunksize=1000, on_bad_lines='warn'))

    print("Análisis de columnas y tipos de datos del archivo CSV:")
    print("="*50)

    # Obtener nombres de columnas y tipos de datos inferidos por pandas
    column_info = pd.DataFrame({
        'Tipo de Dato Inferido': chunk.dtypes,
        'Ejemplo de Dato': chunk.iloc[0] # Muestra el primer valor no nulo de cada columna
    }).reset_index().rename(columns={'index': 'Nombre de Columna'})


    print(column_info.to_string())
    print("\n" + "="*50)
    print(f"El archivo tiene {len(chunk.columns)} columnas.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo en la ruta especificada:\n{file_path}")
except Exception as e:
    print(f"Ocurrió un error al procesar el archivo: {e}")

