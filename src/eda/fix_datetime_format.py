#!/usr/bin/env python3
import os
import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import BASE_DIR

def fix_datetime_format(file_path):
    """Cambia el formato de fecha para conservar fecha y hora completa"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar y reemplazar la línea del strftime que solo guarda fecha
        old_line = "df_out['fecha_hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y')"
        new_line = "df_out['fecha_hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y %H:%M:%S')"

        if old_line in content:
            content = content.replace(old_line, new_line)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[OK] Actualizado: {file_path}")
            return True
        else:
            print(f"[-] Sin cambios necesarios: {file_path}")
            return False

    except Exception as e:
        print(f"[ERROR] Error en {file_path}: {e}")
        return False

def main():
    print("Corrigiendo formato de fecha y hora en todos los scripts...")
    print("Cambiando de '%d/%m/%Y' a '%d/%m/%Y %H:%M:%S'")
    print("=" * 60)

    # Construir la ruta al directorio de recolección de datos
    DATA_COLLECTION_DIR = os.path.join(BASE_DIR, 'src', 'data_collection')
    print(f"Buscando archivos en: {DATA_COLLECTION_DIR}")

    # Buscar todos los archivos Python de códigos
    patterns = [
        "codigo_*_S*_v2.py",
        "codigo_*_S*.py"
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
        if fix_datetime_format(file_path):
            modified_count += 1

    print()
    print("=" * 60)
    print(f"Proceso completado:")
    print(f"- Archivos revisados: {len(files_to_fix)}")
    print(f"- Archivos modificados: {modified_count}")
    print(f"- Sin modificaciones: {len(files_to_fix) - modified_count}")
    print()
    print("Cambio realizado:")
    print("  ANTES: '01/01/2020' (solo fecha)")
    print("  AHORA: '01/01/2020 14:30:25' (fecha + hora)")
    print()
    print("Los CSVs ahora conservarán la información de hora completa.")

if __name__ == "__main__":
    main()