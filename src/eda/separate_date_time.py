#!/usr/bin/env python3
import os
import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import BASE_DIR

def separate_date_time_columns(file_path):
    """Modifica el script para separar fecha_hora_hecho en columnas independientes"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar la sección de procesamiento de fecha
        old_block = """    # Convertir y formatear la fecha
    if 'fecha_hora_hecho' in df_out.columns:
        df_out['fecha_hora_hecho'] = pd.to_datetime(df_out['fecha_hora_hecho'], unit='ms', errors='coerce')
        df_out['fecha_hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y %H:%M:%S')"""

        new_block = """    # Convertir y separar fecha y hora
    if 'fecha_hora_hecho' in df_out.columns:
        df_out['fecha_hora_hecho'] = pd.to_datetime(df_out['fecha_hora_hecho'], unit='ms', errors='coerce')

        # Crear columnas separadas para fecha y hora
        df_out['fecha_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y')
        df_out['hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%H:%M:%S')
        df_out['dia_semana'] = df_out['fecha_hora_hecho'].dt.day_name()
        df_out['hora_numerica'] = df_out['fecha_hora_hecho'].dt.hour

        # Mantener también la fecha_hora completa como string legible
        df_out['fecha_hora_completa'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y %H:%M:%S')"""

        if old_block in content:
            content = content.replace(old_block, new_block)
        else:
            # Buscar variantes del bloque
            old_block_v2 = """    if 'fecha_hora_hecho' in df_out.columns:
        df_out['fecha_hora_hecho'] = pd.to_datetime(df_out['fecha_hora_hecho'], unit='ms', errors='coerce')
        df_out['fecha_hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y %H:%M:%S')"""

            if old_block_v2 in content:
                content = content.replace(old_block_v2, new_block)
            else:
                print(f"[-] No se encontró el patrón en: {file_path}")
                return False

        # Actualizar la lista de columnas preferidas para incluir las nuevas
        old_preferred = """    preferred = [
        "fecha_hora_hecho", "anio_hecho", "mes_hecho", "dia_hecho",
        "departamento_hecho", "provincia_hecho", "distrito_hecho",
        "tipo_hecho", "id_tipo_hecho", "materia_hecho", "id_materia_hecho",
        "lat", "lon", "lat_hecho", "long_hecho"
    ]"""

        new_preferred = """    preferred = [
        "fecha_hecho", "hora_hecho", "fecha_hora_completa", "dia_semana", "hora_numerica",
        "anio_hecho", "mes_hecho", "dia_hecho", "fecha_hora_hecho",
        "departamento_hecho", "provincia_hecho", "distrito_hecho",
        "tipo_hecho", "id_tipo_hecho", "materia_hecho", "id_materia_hecho",
        "lat", "lon", "lat_hecho", "long_hecho"
    ]"""

        if old_preferred in content:
            content = content.replace(old_preferred, new_preferred)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Actualizado: {file_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Error en {file_path}: {e}")
        return False

def main():
    print("Separando fecha_hora_hecho en columnas independientes...")
    print("Nuevas columnas que se crearán:")
    print("  - fecha_hecho: '15/03/2020' (DD/MM/YYYY)")
    print("  - hora_hecho: '14:30:25' (HH:MM:SS)")
    print("  - dia_semana: 'Sunday', 'Monday', etc.")
    print("  - hora_numerica: 14 (para análisis numérico)")
    print("  - fecha_hora_completa: '15/03/2020 14:30:25' (legible)")
    print("=" * 70)

    # Construir la ruta al directorio de recolección de datos
    DATA_COLLECTION_DIR = os.path.join(BASE_DIR, 'src', 'data_collection')
    print(f"Buscando archivos en: {DATA_COLLECTION_DIR}")

    # Buscar todos los archivos Python de códigos
    patterns = [
        "codigo_*_S*_v2.py",
        "codigo_*_S*.py",
        "codigo.py",
        "codigo_v2.py"
    ]

    files_to_fix = []
    for pattern in patterns:
        search_path = os.path.join(DATA_COLLECTION_DIR, pattern)
        files_to_fix.extend(glob.glob(search_path))

    files_to_fix = list(set(files_to_fix))  # Remover duplicados
    files_to_fix.sort()

    if not files_to_fix:
        print("No se encontraron archivos para modificar.")
        return

    print(f"Archivos encontrados: {len(files_to_fix)}")
    print()

    modified_count = 0
    for file_path in files_to_fix:
        if separate_date_time_columns(file_path):
            modified_count += 1

    print()
    print("=" * 70)
    print(f"Proceso completado:")
    print(f"- Archivos revisados: {len(files_to_fix)}")
    print(f"- Archivos modificados: {modified_count}")
    print(f"- Sin modificaciones: {len(files_to_fix) - modified_count}")
    print()
    print("📊 Columnas en CSV resultante:")
    print("  fecha_hecho       | hora_hecho | dia_semana | hora_numerica")
    print("  15/03/2020       | 14:30:25   | Sunday     | 14")
    print("  16/03/2020       | 08:15:10   | Monday     | 8")
    print("  16/03/2020       | 22:45:30   | Monday     | 22")
    print()
    print("✅ Beneficios para análisis:")
    print("  - Filtrar por días de la semana")
    print("  - Análisis por franjas horarias")
    print("  - Agrupaciones por fecha específica")
    print("  - Patrones de criminalidad por hora")

if __name__ == "__main__":
    main()