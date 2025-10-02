import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import PROCESSED_DATA_DIR, BASE_DIR

# --- Configuración ---
SAMPLE_SIZE = 100000
INPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'denuncias_final.csv') # Asumiendo que este es el archivo a analizar
REPORTS_DIR = os.path.join(BASE_DIR, 'docs', 'analysis_reports')
os.makedirs(REPORTS_DIR, exist_ok=True)
OUTPUT_MD = os.path.join(REPORTS_DIR, '01_diagnostico_inicial.md')

# --- Inicio del Script ---
print(f"Iniciando el diagnóstico inicial del archivo CSV...")
print(f"Se analizará una muestra de las primeras {SAMPLE_SIZE:,} filas.")
print(f"El reporte se guardará en: {OUTPUT_MD}")
print("="*80)

try:
    # Leer una muestra del CSV
    df_sample = pd.read_csv(FILE_PATH, nrows=SAMPLE_SIZE, on_bad_lines='warn', low_memory=False)

    # Abrir archivo markdown para escribir el reporte
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# Paso 1: Diagnóstico Inicial de Datos\n\n")
        f.write(f"Este documento resume el primer análisis exploratorio realizado sobre el conjunto de datos de denuncias.\n")
        f.write(f"El análisis se realizó sobre una muestra de las primeras **{SAMPLE_SIZE:,} filas** para garantizar la eficiencia.\n\n")
        f.write("---\n\n")

        # --- 1. Información General ---
        f.write("## 1. Información General y Tipos de Datos\n\n")
        f.write(f"*   **Total de filas en la muestra**: {len(df_sample):,}\n")
        f.write(f"*   **Uso de memoria en la muestra**: {df_sample.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n\n")

        info_df = pd.DataFrame({
            "Valores No Nulos": df_sample.count(),
            "Tipo de Dato": df_sample.dtypes
        }).reset_index().rename(columns={'index': 'Columna'})
        
        # Usar to_markdown() para una tabla bien formateada
        f.write(info_df.to_markdown(index=False))
        f.write("\n\n---\n\n")

        # --- 2. Resumen de Valores Faltantes ---
        f.write("## 2. Resumen de Valores Faltantes\n\n")
        missing_values = df_sample.isnull().sum()
        missing_percentage = (missing_values / len(df_sample)) * 100
        missing_df = pd.DataFrame({
            'Valores Faltantes': missing_values,
            '% Faltante': missing_percentage
        }).reset_index().rename(columns={'index': 'Columna'})
        
        missing_df_sorted = missing_df[missing_df['Valores Faltantes'] > 0].sort_values(by='% Faltante', ascending=False)
        f.write(missing_df_sorted.to_markdown(index=False))
        f.write("\n\n---\n\n")

        # --- 3. Estadísticas Descriptivas (Numéricas) ---
        f.write("## 3. Estadísticas Descriptivas (Numéricas)\n\n")
        f.write("```\n")
        f.write(df_sample.describe().T.to_string())
        f.write("\n```\n\n")
        f.write("---\n\n")

        # --- 4. Estadísticas Descriptivas (Categóricas) ---
        f.write("## 4. Estadísticas Descriptivas (Categóricas)\n\n")
        f.write("```\n")
        f.write(df_sample.describe(include=['object']).T.to_string())
        f.write("\n```\n\n")
        f.write("---\n\n")

        # --- 5. Distribución de Valores para Columnas Clave ---
        f.write("## 5. Distribución para Categorías Clave (Top 10)\n\n")
        key_cols = ['departamento_hecho', 'tipo_hecho', 'turno_hecho', 'ano_hecho', 'mes_hecho']
        for col in key_cols:
            if col in df_sample.columns:
                f.write(f"### Distribución para '{col}' (% sobre la muestra)\n")
                f.write("```\n")
                value_counts_perc = (df_sample[col].value_counts(normalize=True).head(10) * 100)
                f.write(value_counts_perc.to_string())
                f.write("\n```\n\n")

    print("Diagnóstico inicial completado y reporte guardado.")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo en la ruta especificada:\n{FILE_PATH}")
except Exception as e:
    print(f"Ocurrió un error al procesar el archivo: {e}")