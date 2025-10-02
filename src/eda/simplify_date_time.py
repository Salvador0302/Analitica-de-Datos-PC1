#!/usr/bin/env python3
import os
import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import BASE_DIR

def simplify_date_time_columns(file_path):
    """Simplifica para mantener solo fecha_hecho y hora_hecho"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar y reemplazar el bloque complejo con uno simple
        old_block = """    # Convertir y separar fecha y hora
    if 'fecha_hora_hecho' in df_out.columns:
        df_out['fecha_hora_hecho'] = pd.to_datetime(df_out['fecha_hora_hecho'], unit='ms', errors='coerce')

        # Crear columnas separadas para fecha y hora
        df_out['fecha_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y')
        df_out['hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%H:%M:%S')
        df_out['dia_semana'] = df_out['fecha_hora_hecho'].dt.day_name()
        df_out['hora_numerica'] = df_out['fecha_hora_hecho'].dt.hour

        # Mantener también la fecha_hora completa como string legible
        df_out['fecha_hora_completa'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y %H:%M:%S')"""

        new_block = """    # Convertir y separar fecha y hora
    if 'fecha_hora_hecho' in df_out.columns:
        df_out['fecha_hora_hecho'] = pd.to_datetime(df_out['fecha_hora_hecho'], unit='ms', errors='coerce')

        # Crear solo fecha_hecho y hora_hecho
        df_out['fecha_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y')
        df_out['hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%H:%M:%S')"""

        if old_block in content:
            content = content.replace(old_block, new_block)
        else:
            print(f"[-] No se encontró el patrón completo en: {file_path}")
            return False

        # Simplificar la lista de columnas preferidas
        old_preferred = """    preferred = [
        "fecha_hecho", "hora_hecho", "fecha_hora_completa", "dia_semana", "hora_numerica",
        "anio_hecho", "mes_hecho", "dia_hecho", "fecha_hora_hecho",
        "departamento_hecho", "provincia_hecho", "distrito_hecho",
        "tipo_hecho", "id_tipo_hecho", "materia_hecho", "id_materia_hecho",
        "lat", "lon", "lat_hecho", "long_hecho"
    ]"""

        new_preferred = """    preferred = [
        "fecha_hecho", "hora_hecho", "fecha_hora_hecho",
        "anio_hecho", "mes_hecho", "dia_hecho",
        "departamento_hecho", "provincia_hecho", "distrito_hecho",
        "tipo_hecho", "id_tipo_hecho", "materia_hecho", "id_materia_hecho",
        "lat", "lon", "lat_hecho", "long_hecho"
    ]"""

        if old_preferred in content:
            content = content.replace(old_preferred, new_preferred)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Simplificado: {file_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Error en {file_path}: {e}")
        return False

def main():
    print("Simplificando columnas de fecha y hora...")
    print("Solo se mantendrán:")
    print("  - fecha_hecho: '15/03/2020'")
    print("  - hora_hecho: '14:30:25'")
    print("Removiendo: dia_semana, hora_numerica, fecha_hora_completa")
    print("=" * 60)

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

    files_to_fix = list(set(files_to_fix))
    files_to_fix.sort()

    if not files_to_fix:
        print("No se encontraron archivos para modificar.")
        return

    print(f"Archivos encontrados: {len(files_to_fix)}")
    print()

    modified_count = 0
    for file_path in files_to_fix:
        if simplify_date_time_columns(file_path):
            modified_count += 1

    print()
    print("=" * 60)
    print(f"Proceso completado:")
    print(f"- Archivos revisados: {len(files_to_fix)}")
    print(f"- Archivos modificados: {modified_count}")
    print(f"- Sin modificaciones: {len(files_to_fix) - modified_count}")
    print()
    print("Resultado en CSV:")
    print("  fecha_hecho  | hora_hecho")
    print("  15/03/2020   | 14:30:25")
    print("  16/03/2020   | 08:15:10")
    print("  16/03/2020   | 22:45:30")

if __name__ == "__main__":
    main()