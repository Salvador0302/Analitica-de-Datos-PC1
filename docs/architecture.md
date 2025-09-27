# Arquitectura (Borrador)

## Capas
1. Ingesta / Scraping (`src/data_collection`)
2. Procesamiento y Limpieza / EDA (`src/eda`)
3. Presentación / App (`src/app` + `src/main.py`)

## Flujo de Datos
raw -> interim -> processed -> (app / análisis)
