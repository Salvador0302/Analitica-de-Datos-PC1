#!/usr/bin/env python3
import os
import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.paths import BASE_DIR

def fix_print_statements(file_path):
    """Agrega flush=True a todos los print statements en un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Reemplazar print statements que no tienen flush=True
        lines = content.split('\n')
        modified_lines = []

        for line in lines:
            # Si la línea contiene print( pero no flush=True, agregar flush=True
            if 'print(' in line and 'flush=' not in line and not line.strip().startswith('#'):
                # Encontrar el último paréntesis de cierre del print
                if line.rstrip().endswith(')'):
                    # Insertar flush=True antes del último paréntesis
                    line = line.rstrip()[:-1] + ', flush=True)'
                elif line.rstrip().endswith('")'):
                    line = line.rstrip()[:-2] + '", flush=True)'
                elif line.rstrip().endswith("')"):
                    line = line.rstrip()[:-2] + "', flush=True)"

            modified_lines.append(line)

        modified_content = '\n'.join(modified_lines)

        # Solo escribir si hay cambios
        if modified_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"[OK] Actualizado: {file_path}")
            return True
        else:
            print(f"[-] Sin cambios: {file_path}")
            return False

    except Exception as e:
        print(f"[ERROR] Error en {file_path}: {e}")
        return False

def main():
    print("Arreglando buffering en todos los scripts...")
    print("Agregando flush=True a los print statements")
    print("=" * 50)

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
        if fix_print_statements(file_path):
            modified_count += 1

    print()
    print("=" * 50)
    print(f"Proceso completado:")
    print(f"- Archivos revisados: {len(files_to_fix)}")
    print(f"- Archivos modificados: {modified_count}")
    print(f"- Sin modificaciones: {len(files_to_fix) - modified_count}")
    print()
    print("Ahora los scripts mostrarán output en tiempo real sin buffering.")

if __name__ == "__main__":
    main()