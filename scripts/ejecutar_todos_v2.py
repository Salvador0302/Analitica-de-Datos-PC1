#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import threading
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from datetime import datetime
import queue

def run_script_with_live_output(script_name):
    """Ejecuta un script individual mostrando output en tiempo real"""
    try:
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [INFO] Iniciando {script_name}...")

        # Ejecutar con output en tiempo real - sin buffering
        process = subprocess.Popen(
            [sys.executable, "-u", script_name],  # -u para unbuffered
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,  # Sin buffer
            universal_newlines=True,
            env={**os.environ, "PYTHONUNBUFFERED": "1"}  # Forzar sin buffer
        )

        # Leer output línea por línea con flush inmediato
        while True:
            line = process.stdout.readline()
            if not line:
                break
            if line.strip():
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] [{script_name}] {line.strip()}", flush=True)

        process.stdout.close()
        return_code = process.wait()

        timestamp = datetime.now().strftime('%H:%M:%S')
        if return_code == 0:
            print(f"[{timestamp}] [ÉXITO] {script_name} completado exitosamente", flush=True)
            return f"{script_name}: ÉXITO"
        else:
            print(f"[{timestamp}] [ERROR] {script_name} terminó con código {return_code}", flush=True)
            return f"{script_name}: ERROR - código {return_code}"

    except Exception as e:
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [ERROR] Excepción en {script_name}: {e}", flush=True)
        return f"{script_name}: EXCEPCIÓN - {str(e)}"

def monitor_progress_v2():
    """Monitorea el progreso de los archivos CSV v2 generados"""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [MONITOR-V2] Iniciando monitoreo de progreso...", flush=True)

    last_count = 0
    while True:
        try:
            if os.path.exists("data_v2"):
                csv_files = [f for f in os.listdir("data_v2") if f.endswith(".csv")]
                current_count = len(csv_files)

                if current_count > last_count or current_count > 0:
                    total_size = sum(os.path.getsize(os.path.join("data_v2", f)) for f in csv_files) / (1024 * 1024)
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] [MONITOR-V2] Archivos completados: {current_count}/12 | Tamaño total: {total_size:.2f} MB", flush=True)
                    last_count = current_count

                    if current_count >= 12:
                        print(f"[{timestamp}] [MONITOR-V2] ¡Todos los archivos completados!", flush=True)
                        break

                elif current_count == 0:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] [MONITOR-V2] Esperando primeros archivos...", flush=True)

            time.sleep(15)  # Monitorear cada 15 segundos

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [MONITOR-V2] Error: {e}", flush=True)
            break

def main():
    print("=" * 80)
    print("    DESCARGA PARALELA DE DENUNCIAS - VERSIÓN 2")
    print("    Método: ThreadPoolExecutor + POST con ObjectIDs")
    print("    Ejecutando 12 scripts simultáneos")
    print("=" * 80)
    print()

    # Crear directorio de datos si no existe
    os.makedirs("data_v2", exist_ok=True)

    # Lista de scripts v2 a ejecutar
    scripts = [
        "codigo_2020_S1_v2.py", "codigo_2020_S2_v2.py",
        "codigo_2021_S1_v2.py", "codigo_2021_S2_v2.py"
    ]

    # Verificar que todos los scripts existen
    missing_scripts = [s for s in scripts if not os.path.exists(s)]
    if missing_scripts:
        print(f"[ERROR] Scripts faltantes: {missing_scripts}")
        print("Ejecuta 'python generar_scripts_v2.py' para crearlos.")
        return

    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [INFO] Ejecutando {len(scripts)} scripts v2 en paralelo...")
    print(f"[{timestamp}] [INFO] CPU cores disponibles: {multiprocessing.cpu_count()}")
    print(f"[{timestamp}] [INFO] Workers máximos: 6")
    print(f"[{timestamp}] [INFO] Método de descarga: ThreadPoolExecutor (interno) + POST")
    print(f"[{timestamp}] [INFO] Directorio de salida: data_v2/")
    print()

    start_time = time.time()

    # Iniciar monitor de progreso en hilo separado
    monitor_thread = threading.Thread(target=monitor_progress_v2, daemon=True)
    monitor_thread.start()

    # Ejecutar scripts en paralelo con output en tiempo real
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [INFO] Iniciando ejecución paralela...")
    print("=" * 80)

    results = []
    with ProcessPoolExecutor(max_workers=6) as executor:
        # Enviar todos los trabajos
        future_to_script = {executor.submit(run_script_with_live_output, script): script for script in scripts}

        # Procesar resultados conforme se completan
        for future in as_completed(future_to_script):
            script = future_to_script[future]
            try:
                result = future.result()
                results.append(result)
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"\n[{timestamp}] [COMPLETADO] {script} - {len(results)}/{len(scripts)} scripts terminados")
                print("-" * 80)
            except Exception as exc:
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] [ERROR] {script} generó excepción: {exc}")
                results.append(f"{script}: EXCEPCIÓN - {exc}")

    end_time = time.time()

    print("\n" + "=" * 80)
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [INFO] Todas las ejecuciones completadas")

    print("\n" + "=" * 80)
    print("RESUMEN FINAL DE EJECUCIÓN - VERSIÓN 2:")
    print("=" * 80)

    successful = [r for r in results if "ÉXITO" in r]
    failed = [r for r in results if "ÉXITO" not in r]

    print(f"\n✅ Scripts exitosos: {len(successful)}/{len(scripts)}")
    for result in successful:
        print(f"  ✓ {result}")

    if failed:
        print(f"\n❌ Scripts fallidos: {len(failed)}")
        for result in failed:
            print(f"  ✗ {result}")

    duration_mins = (end_time - start_time) / 60
    print(f"\n⏱️  Tiempo total: {duration_mins:.1f} minutos ({end_time - start_time:.1f} segundos)")
    print(f"📁 Directorio de salida: data_v2/")

    # Listar archivos CSV generados con estadísticas detalladas
    if os.path.exists("data_v2"):
        csv_files = [f for f in os.listdir("data_v2") if f.endswith(".csv")]
        if csv_files:
            total_size = 0
            total_rows = 0
            print(f"\n📊 Archivos CSV v2 generados: {len(csv_files)}/12")
            print("-" * 70)
            print(f"{'Archivo':<25} {'Tamaño':<10} {'Filas':<10} {'Estado'}")
            print("-" * 70)

            for csv_file in sorted(csv_files):
                file_path = os.path.join("data_v2", csv_file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                total_size += size_mb

                # Contar filas (aproximado)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        rows = sum(1 for line in f) - 1  # -1 para header
                    total_rows += rows
                    status = "✅ OK"
                except:
                    rows = 0
                    status = "❌ Error"

                print(f"{csv_file:<25} {size_mb:>7.1f}MB {rows:>8,} {status}")

            print("-" * 70)
            print(f"{'TOTAL':<25} {total_size:>7.1f}MB {total_rows:>8,}")

            # Comparar con versión 1 si existe
            if os.path.exists("data"):
                v1_files = [f for f in os.listdir("data") if f.endswith(".csv")]
                if v1_files:
                    v1_total_size = sum(os.path.getsize(os.path.join("data", f)) for f in v1_files) / (1024 * 1024)
                    print(f"\n📈 Comparación con versión 1:")
                    print(f"   V1 (data/):    {len(v1_files)} archivos, {v1_total_size:.1f}MB")
                    print(f"   V2 (data_v2/): {len(csv_files)} archivos, {total_size:.1f}MB")
                    if total_size > v1_total_size:
                        print(f"   📈 V2 obtuvo {((total_size/v1_total_size-1)*100):+.1f}% más datos")
                    elif total_size < v1_total_size:
                        print(f"   📉 V2 obtuvo {((total_size/v1_total_size-1)*100):+.1f}% menos datos")
                    else:
                        print(f"   📊 Ambas versiones obtuvieron datos similares")

        else:
            print("\n⚠️  [ADVERTENCIA] No se encontraron archivos CSV en data_v2/")
    else:
        print("\n⚠️  [ADVERTENCIA] Directorio data_v2/ no existe")

    print("\n" + "=" * 80)
    print("CARACTERÍSTICAS DE LA VERSIÓN 2:")
    print("- Descarga paralela con ThreadPoolExecutor (interno)")
    print("- Método POST con objectIds en chunks de 1000")
    print("- Filtros por año y semestre específicos")
    print("- Máximo 6 workers por script + 6 scripts paralelos")
    print("- Fallback automático GeoJSON → JSON")
    print("- Timeout de 120 segundos por request")
    print("=" * 80)

    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [FINALIZADO] Proceso de descarga v2 completado")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [INFO] Proceso interrumpido por usuario")
    except Exception as e:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [ERROR] Error inesperado: {e}")
    finally:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [INFO] Finalizando...")
        input("\nPresiona Enter para salir...")