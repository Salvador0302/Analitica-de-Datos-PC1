@echo off
echo =====================================
echo    DESCARGA PARALELA DE DENUNCIAS
echo    Ejecutando 12 scripts simultaneos
echo =====================================
echo.

REM Crear directorio de datos si no existe
if not exist "data" mkdir data

REM Ejecutar todos los scripts en paralelo
echo [INFO] Iniciando descarga paralela por semestres...
echo [INFO] Scripts ejecutandose en segundo plano...
echo.

start /B python codigo_2020_S1.py
start /B python codigo_2020_S2.py
start /B python codigo_2021_S1.py
start /B python codigo_2021_S2.py
start /B python codigo_2022_S1.py
start /B python codigo_2022_S2.py
start /B python codigo_2023_S1.py
start /B python codigo_2023_S2.py
start /B python codigo_2024_S1.py
start /B python codigo_2024_S2.py
start /B python codigo_2025_S1.py
start /B python codigo_2025_S2.py

echo [INFO] 12 procesos iniciados exitosamente
echo [INFO] Monitorea el progreso en las ventanas abiertas
echo [INFO] Los archivos CSV se guardaran en: data\
echo.
echo [ARCHIVOS ESPERADOS:]
echo   - denuncias_2020_S1.csv
echo   - denuncias_2020_S2.csv
echo   - denuncias_2021_S1.csv
echo   - denuncias_2021_S2.csv
echo   - denuncias_2022_S1.csv
echo   - denuncias_2022_S2.csv
echo   - denuncias_2023_S1.csv
echo   - denuncias_2023_S2.csv
echo   - denuncias_2024_S1.csv
echo   - denuncias_2024_S2.csv
echo   - denuncias_2025_S1.csv
echo   - denuncias_2025_S2.csv
echo.
echo [INFO] Presiona cualquier tecla para salir...
pause >nul